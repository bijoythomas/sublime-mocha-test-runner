Sublime Mocha Test Runner
=========================
Runs mocha tests with the option to run specific tests or all tests in a file.
Inspired by the mocha test runner plugin for Atom [https://github.com/TabDigital/atom-mocha-test-runner]

Requirements
============
The mocha command should be available in the PATH. The plugin has been tested against python 2.7

Installation
------------
To install it **manually with Git:** Clone the repository in your Sublime Text 2 Packages directory:

    git clone https://github.com/bijoythomas/sublime-mocha-test-runner.git "Mocha Test Runner"


The "Packages" directory should be located at:

* OS X:

    ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/

* Linux:

    ~/.Sublime\ Text\ 2/Packages/  
    or  
    ~/.config/sublime-text-2/Packages/

* Windows:

    %APPDATA%/Sublime Text 2/Packages/


The plugin should be picked up automatically. If not, restart Sublime Text.

Usage
-----
The plugin adds the following commands to the Sublime Command Palette

```Run Tests```
This will run all the tests in the file that is active

```Run previous test```
The plugin remembers the last run test. If you are swithcing back and forth between code and the test code, this command will run the tests regardless of the active file for fast TDD feedback loops

```Show output panel```
Brings up the output panel with the tests results. This comes up automatically after the tests are run. But you can bring it up again if you closed it.

You can bring up the sublime console Ctrl+` and see the command that the plugin invoked to run the tests.

The plugin adds the following key bindings. The key bindings provide the ability to run a specific test in a file or all tests.

```
[
  {
    "keys": ["ctrl+alt+m"], "command": "mocha_test_runner"
  },
  {
    "keys": ["ctrl+shift+alt+m"], "command": "mocha_test_runner", "args": {"previous": true}
  }
]
```

- `ctrl-alt-m` runs either:
  - the current test file
  - or a single `it` / `describe` if the cursor is on that line

- `ctrl-alt-shift-m` re-runs the last test selection
  - even if you switched to another file

The plugin invokes mocha with the --grep option to run specific test in a file

Reporting
=========
The output of the mocha command is made available in a panel which comes up after the mocha command is run. Because the standard panel supports only ascii characters, the mocha command is run with the TAP reporting option.
