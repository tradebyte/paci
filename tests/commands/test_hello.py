"""Tests for our `hello` command."""

import unittest
from unittest.mock import patch
from docopt import docopt
from io import StringIO
import paci.cli as paci
from paci.commands.hello import Hello

doc = paci.__doc__

class TestHello(unittest.TestCase):
    def test_args_hello_world(self):
        args = docopt(doc, ["hello"])
        self.assertEqual(args["hello"], True)

@unittest.mock.patch('sys.stdout', new_callable=StringIO)
def test_prints_hello_world_args(mock_stdout):
    hello = Hello(["test"])
    hello.run()
    assert 'Hello, world!\nYou supplied the following options: [\n  "test"\n]\n' == mock_stdout.getvalue()
