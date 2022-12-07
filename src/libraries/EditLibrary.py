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
        self.repository_mock = Mock()
        self.io_mock = Mock()

    def input_text(self, text):
        self.inputs.append(text)

    def reset_input(self):
        self.inputs = []

    def add_inputs(self):
        self.repository_mock.post()

    def output_contains(self, expected):
        self.io_mock.read.side_effect = self.inputs

        def post():
            for e in self.inputs:
                self.db_model.append(e)
        def put():
            return self.inputs[0] == self.db_model[0]

        self.repository_mock.post.side_effect = post
        self.repository_mock.put.side_effect = put

        try:
            edit = Edit(self.repository_mock, self.io_mock)
            edit.run()
        except StopIteration:
            return "Wrong parameters"

        output = self.io_mock.write.call_args_list[-1].args[0]

        if expected not in output:
            raise AssertionError(
                f"{expected} was not in command output {output}")

    def reference_should_edited_correctly(self):
        repository_mock = Mock()
        io_mock = Mock()
        self.io_mock.read.side_effect = self.inputs
        def post():
            for e in self.inputs:
                self.db_model.append(e)

        def put(input):
            return input.reference_id == self.db_model[0]

        self.repository_mock.post.side_effect = post
        self.repository_mock.put.side_effect = put
        io_mock.read.side_effect = self.inputs
        add = Add(repository_mock, io_mock)

        try:
            edit = Edit(self.repository_mock, self.io_mock)
            edit.run()
        except StopIteration:
            return "Wrong parameters"


        repository_mock.put.assert_called_with(Reference(
            reference_id=add.generate_ref_id([self.inputs[1]], int(self.inputs[2])),
            title=self.inputs[0],
            authors=[self.inputs[1]],
            year=int(self.inputs[2]),
            publisher=self.inputs[3],
            tags=[self.inputs[4]]
        ))

