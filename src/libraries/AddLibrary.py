from unittest.mock import Mock

import sys
sys.path.append(sys.path[0] + "/..")


from entities.reference import Reference
from commands.add import Add


class AddLibrary:
    def __init__(self):
        self.inputs = []

    def input_text(self, text):
        self.inputs.append(text)

    def output_should_contain(self, expected):
        repository_mock = Mock()
        repository_mock.id_exists.return_value = False

        io_mock = Mock()
        io_mock.read.side_effect = self.inputs

        add = Add(repository_mock, io_mock)
        add.run()

        output = io_mock.write.call_args_list[-1].args[0]

        if expected not in output:
            raise AssertionError(
                f"{expected} was not in command output {output}")

    def reference_should_be_saved_with_provided_fields(self):
        repository_mock = Mock()
        repository_mock.id_exists.return_value = False

        io_mock = Mock()
        io_mock.read.side_effect = self.inputs

        add = Add(repository_mock, io_mock)
        add.run()

        repository_mock.post.assert_called_with(Reference(
            reference_id=add.generate_ref_id([self.inputs[1]], int(self.inputs[2])),
            title=self.inputs[0],
            authors=[self.inputs[1]],
            year=int(self.inputs[2]),
            publisher=self.inputs[3],
            tags=[self.inputs[4]]
        ))
