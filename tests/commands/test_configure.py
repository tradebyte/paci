"""Tests for our `configure` command."""

import unittest
from unittest.mock import patch, mock_open
from docopt import docopt
from io import StringIO
import paci.cli as paci
from paci.commands.configure import Configure

doc = paci.__doc__


class TestConfigure(unittest.TestCase):

    def test_prints_the_welcome_msg(self):
        configure = Configure(["test"])

        with patch('sys.stdout', new_callable=StringIO) as sysout:
            with patch("paci.commands.configure.input", return_value=False) as m:
                configure.run()

        self.assertIn('Lets configure a new settings.yml for paci!', sysout.getvalue())

    def test_asks_for_basedir(self):
        configure = Configure(["test"])

        with patch('sys.stdout', new_callable=StringIO) as sysout:
            with patch('sys.stdin', new_callable=StringIO) as sysin:
                configure.run()

        self.assertIn('basedir (defaults to', sysin.getvalue())
