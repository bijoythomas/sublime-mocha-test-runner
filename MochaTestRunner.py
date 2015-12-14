import sublime
import sublime_plugin
import subprocess
import thread
import os
import functools
import re

class MochaTestRunnerCommand(sublime_plugin.TextCommand):

  state = {}

  def clear_test_view(self):
    self.output_view.set_read_only(False)
    edit = self.output_view.begin_edit()
    self.output_view.erase(edit, sublime.Region(0, self.output_view.size()))
    self.output_view.end_edit(edit)
    self.output_view.set_read_only(True)

  def show_tests_panel(self):
    if not hasattr(self, 'output_view'):
      hasattr(self, 'output_view')
      self.output_view = self.view.window().get_output_panel('mocha_tests')

    self.clear_test_view()
    self.view.window().run_command('show_panel', {'panel': 'output.mocha_tests'})

  def read_stdout(self):
    while True:
      data = os.read(self.proc.stdout.fileno(), 32768)
      if data != '':
        sublime.set_timeout(functools.partial(self.append_data, self.proc, data), 0)
        continue
      else:
        self.proc.stdout.close()
        break

  def append_data(self, proc, data):
    self.output_view.set_read_only(False)
    edit = self.output_view.begin_edit()
    self.output_view.insert(edit, self.output_view.size(), data)
    self.output_view.end_edit(edit)
    self.output_view.set_read_only(True)

  def run(self, edit, **args):
    selection = self.view.sel()[0]
    line = self.view.line(selection.b)
    line_text = self.view.substr(line)
    mocha_command = 'mocha -R tap'

    if 'previous' in args:
      print 'Using previous command'
      mocha_command = MochaTestRunnerCommand.state.get(self.view.window().id(), {}).get('command')
    elif 'all_tests' in args:
      mocha_command = mocha_command + ' ' + self.view.file_name()
    elif line_text.find('describe') != -1 or line_text.find('it') != -1:
      mocha_command = mocha_command + ' --grep ' + re.search("'(.*)'", line_text).group() + ' ' + self.view.file_name()
    else:
      mocha_command = mocha_command + ' ' + self.view.file_name()

    print 'Running ' + mocha_command
    MochaTestRunnerCommand.state.setdefault(self.view.window().id(), {})['command'] = mocha_command
    self.show_tests_panel()
    self.proc = subprocess.Popen(mocha_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    thread.start_new_thread(self.read_stdout, ())
