import sublime
import sublime_plugin
import subprocess
import re
import os

class MochaTestRunnerCommand(sublime_plugin.TextCommand):

  state = {}

  def clear_test_view(self):
    self.output_view.set_read_only(False)
    edit = self.edit
    self.output_view.erase(edit, sublime.Region(0, self.output_view.size()))
    self.output_view.set_read_only(True)

  def show_tests_panel(self):
    if not hasattr(self, 'output_view'):
      hasattr(self, 'output_view')

    self.output_view = self.view.window().get_output_panel('mocha_tests')
    self.clear_test_view()
    self.view.window().run_command('show_panel', {'panel': 'output.mocha_tests'})

  def append_data(self, data):
    self.output_view.set_read_only(False)
    edit = self.edit
    self.output_view.insert(edit, self.output_view.size(), data)
    self.output_view.set_read_only(True)

  def run(self, edit, **args):
    self.edit = edit
    selection = self.view.sel()[0]
    line = self.view.line(selection.b)
    line_text = self.view.substr(line)
    mocha_command = 'mocha --exit'

    filename = os.path.basename(self.view.file_name())
    dirname = os.path.dirname(self.view.file_name())
    if 'previous' in args:
      mocha_command = MochaTestRunnerCommand.state.get(self.view.window().id(), {}).get('command')
    elif 'all_tests' in args:
      mocha_command = 'cd ' + dirname + ';' + mocha_command + ' ' + filename
    elif line_text.find('describe') != -1 or line_text.find('it') != -1:
      mocha_command = 'cd ' + dirname + ';' + mocha_command + ' --grep ' + re.search("'(.*)'", line_text).group() + ' ' + filename
    else:
      mocha_command = 'cd ' + dirname + ';' + mocha_command + ' ' + filename

    self.show_tests_panel()
    print('Running ' + mocha_command)
    output = subprocess.getoutput(mocha_command)
    MochaTestRunnerCommand.state.setdefault(self.view.window().id(), {})['command'] = mocha_command
    self.append_data(output)
