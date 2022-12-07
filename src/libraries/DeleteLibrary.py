from unittest.mock import Mock

import sys
sys.path.append(sys.path[0] + "/..")
from commands.delete import Delete

class DeleteLibrary():
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

        def id_exists(input):
            return input in self.db_model

        def delete(input):
            if input in self.db_model:
                self.db_model.remove(input)

        self.repository_mock.post.side_effect = post
        self.repository_mock.delete.side_effect = delete
        self.repository_mock.id_exists.side_effect = id_exists

        try:
            delete = Delete(self.repository_mock, self.io_mock)
            delete.run()
        except StopIteration:
            return "Wrong parameters"

        output = self.io_mock.write.call_args_list[-1].args[0]

        if expected not in output:
            raise AssertionError(
                f"{expected} was not in command output {output}")


    def reference_should_be_deleted_correctly(self):
            def post():
                for e in self.inputs:
                    self.db_model.append(e)

            def delete(input):
                if input in self.db_model:
                    self.db_model.remove(input)

            self.repository_mock.post.side_effect = post
            self.repository_mock.delete.side_effect = delete
            self.io_mock.read.side_effect = self.inputs

            try:
                edit = Delete(self.repository_mock, self.io_mock)
                edit.run()
            except StopIteration:
                return "Wrong parameters"


            self.repository_mock.delete.assert_called_with(self.inputs[0])
