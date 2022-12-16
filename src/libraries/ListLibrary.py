from unittest.mock import Mock

import sys
sys.path.append(sys.path[0] + "/..")

from entities.reference import Reference
from commands.edit import Edit
from commands.l     ist import List

class EditLibrary:
    def __init__(self):
        self.db_model = []
        self.inputs = []
        self.repository_mock = Mock()
        self.io_mock = Mock()

        def post(tag=None):
            for e in self.inputs:
                if tag != None:
                    e = e + tag
                self.db_model.append(e)
        def put():
            return self.inputs[0] == self.db_model[0]

        self.io_mock.read.side_effect = self.inputs
        self.repository_mock.post.side_effect = post
        self.repository_mock.put.side_effect = put


    def input_text(self, text):
        self.inputs.append(text)

    def reset_input(self):
        self.inputs = []

    def add_inputs(self, tag=None):
        self.repository_mock.post(tag)

    def should_list_correctly(self, expected):
        try:
            edit = List(self.repository_mock, self.io_mock)
            edit.run()
        except StopIteration:
            return "Wrong parameters"

        output = self.io_mock.write.call_args_list[-1].args[0]

        if expected not in output:
            raise AssertionError(
                f"{expected} was not in command output {output}")
