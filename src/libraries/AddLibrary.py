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

    def submit_reference(self):
        self.repository_mock = Mock()
        self.repository_mock.id_exists.return_value = False

        io_mock = Mock()
        io_mock.read.side_effect = self.inputs

        self.add = Add(self.repository_mock, io_mock)
        self.add.run()

    def book_reference_should_be_saved_with_provided_fields(self):
        self.submit_reference()
        
        self.repository_mock.post.assert_called_with({
            "type": "book",
            "title": self.inputs[1],
            "author": [self.inputs[2]],
            "year": int(self.inputs[3]),
            "publisher": self.inputs[4],
            "tag": [self.inputs[5]],
            "reference_id": self.add.generate_ref_id([self.inputs[2]], int(self.inputs[3]))
        })

    def inproceedings_reference_should_be_saved_with_provided_fields(self):
        self.submit_reference()
        
        self.repository_mock.post.assert_called_with({
            "type": "inproceedings",
            "title": self.inputs[1],
            "booktitle": self.inputs[2],
            "author": [self.inputs[3]],
            "series": self.inputs[4],
            "year": int(self.inputs[5]),
            "pages": self.inputs[6],
            "publisher": self.inputs[7],
            "address": self.inputs[8],
            "tag": [self.inputs[9]],
            "reference_id": self.add.generate_ref_id([self.inputs[3]], int(self.inputs[5]))
        })

    def misc_reference_should_be_saved_with_provided_fields(self):
        self.submit_reference()
        
        self.repository_mock.post.assert_called_with({
            "type": "misc",
            "title": self.inputs[1],
            "author": [self.inputs[2]],
            "howpublished": self.inputs[3],
            "year": int(self.inputs[4]),
            "note": self.inputs[5],
            "tag": [self.inputs[6]],
            "reference_id": self.add.generate_ref_id([self.inputs[2]], int(self.inputs[4]))
        })
