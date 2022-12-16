from unittest.mock import Mock

import sys
sys.path.append(sys.path[0] + "/..")

from entities.reference import Reference
from commands.edit import Edit
from commands.add import Add

class EditLibrary:
    def __init__(self):
        self.db_model = []
        self.inputs = []
        self.service_mock = Mock()
        self.io_mock = Mock()

        def post():
            pass

        def put(input):
            self.db_model = self.inputs
            return

        def id_exists(id):
            return len(self.db_model) != 0

        self.io_mock.read.side_effect = self.inputs
        self.service_mock.post.side_effect = post
        self.service_mock.put.side_effect = put
        self.service_mock.id_exists.side_effect = id_exists

    def add_id(self, id):
        self.ids.append(id)

    def input_text(self, text):
        self.inputs.append(text)

    def reset_input(self):
        self.inputs = []

    def add_inputs(self):
        for e in self.inputs:
            self.db_model.append(e)

    def set_type(self, type):
        self.service_mock.get_type.return_value = type

    def output_contains(self, expected):
        try:
            edit = Edit(self.service_mock, self.io_mock)
            edit.run()
        except StopIteration:
            return "Wrong parameters"

        output = self.io_mock.write.call_args_list[-1].args[0]

        if expected not in output:
            raise AssertionError(
                f"{expected} was not in command output {output}")


