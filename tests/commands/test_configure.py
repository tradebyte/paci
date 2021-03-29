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
        configure = Configure({'configure': True, '--no-choice': False, '--silent': True, '--main-registry': False, '--fallback-registry': False})

        with patch('sys.stdout', new_callable=StringIO) as sysout:
            with patch("paci.helpers.display_helper.std_input", return_value='') as m:
                configure.run()

        self.assertIn('Lets configure a new settings.yml for paci!', sysout.getvalue())

if __name__ == '__main__':
    unittest.main()
