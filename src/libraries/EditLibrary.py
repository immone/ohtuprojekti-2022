from unittest.mock import Mock

import sys
sys.path.append(sys.path[0] + "/..")

from services.reference_service import ReferenceService
from entities.reference import Reference
from commands.edit import Edit
from commands.add import Add

class EditLibrary:
    def __init__(self):
        self.db_model = []
        self.inputs = []
        self.repository_mock = Mock()
        self.service_mock = Mock()
        self.io_mock = Mock()

        def post():
            for e in self.inputs:
                self.db_model.append(e)

        def put(input):
            self.db_model = self.inputs
            return

        def id_exists(id):
            return len(self.db_model) != 0 and self.db_model == self.inputs

        self.io_mock.read.side_effect = self.inputs
        self.repository_mock.post.side_effect = post
        self.repository_mock.put.side_effect = put
        self.repository_mock.id_exists.side_effect = id_exists

    def input_text(self, text):
        self.inputs.append(text)

    def reset_input(self):
        self.inputs = []

    def add_inputs(self):
        self.repository_mock.post()

    def set_type(self, type):
        self.service_mock.get_type.return_value = type

    def output_contains(self, expected):
        try:
            edit = Edit(self.repository_mock, self.io_mock)
            edit.run()
        except StopIteration:
            return "Wrong parameters"

        output = self.io_mock.write.call_args_list[-1].args[0]

        if expected not in output:
            raise AssertionError(
                f"{expected} was not in command output {output}")

    def book_reference_should_be_edited_correctly(self):
        add = Add(self.repository_mock, self.io_mock)
        try:
            edit = Edit(self.repository_mock, self.io_mock)
            edit.run()
        except StopIteration:
            return "Wrong parameters"

        self.repository_mock.put.assert_called_with(
            Reference(
            reference_id=add.generate_ref_id([self.inputs[1]], int(self.inputs[2])),
            title=self.inputs[0],
            authors=[self.inputs[1]],
            year=int(self.inputs[2]),
            publisher=self.inputs[3],
            tags=[self.inputs[4]]
            )
        )

    def proceedings_reference_should_be_edited_correctly(self):
        add = Add(self.repository_mock, self.io_mock)
        try:
            edit = Edit(self.repository_mock, self.io_mock)
            edit.run()
        except StopIteration:
            return "Wrong parameters"

        self.repository_mock.put.assert_called_with(
            Reference(
                reference_id=add.generate_ref_id([self.inputs[2]], int(self.inputs[4])),
                title=self.inputs[0],
                booktitle = self.inputs[1],
                authors=[self.inputs[2]],
                series = self.inputs[3],
                year=int(self.inputs[4]),
                pages=self.inputs[5],
                publisher=self.inputs[6],
                address=self.inputs[7],
                tags=[self.inputs[8]]
            )
        )


