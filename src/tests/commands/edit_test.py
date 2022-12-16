import unittest
from unittest.mock import Mock
from commands.edit import Edit
from entities.reference import Reference
from services.reference_service import ReferenceService


class TestEdit(unittest.TestCase):
    def setUp(self):
        self.service = ReferenceService()
        self.service.delete_all()
        self.reference = {
            "reference_id": "2",
            "type": "book",
            "author": ["Leonard Susskind", "George Hrabovsky"],
            "title": "Classical mechanics: the theoretical minimum",
            "publisher": "Penguin Random House",
            "year": "2014",
            "tag": ["test_tag2", "test_tag_3"]
        }
        self.reference2 = {
            "reference_id": "3",
            "type": "inproceedings",
            "author": ["Holleis, Paul", "Wagner, Matthias", "Koolwaaij, Johan"],
            "title": "Studying mobile context-aware social services in the wild",
            "booktitle": "Proc. of the 6th Nordic Conf. on Human-Computer Interaction",
            "series": "NordiCHI",
            "year": "2010",
            "pages": "207--216",
            "publisher": "ACM",
            "address": "address",
            "tag": ["test_tag3", "test_tag_4"]
        }
        self.service_mock = Mock()
        self.io_mock = Mock()

    def test_calls(self):
        self.io_mock.read.side_effect = ["2", "", "", "", "", "", ""]

        def put(a,b,c):
            return

        self.service_mock.put.side_effect = put
        self.service_mock.id_exists.return_value = True
        self.service_mock.get_type.return_value = "book"
        self.service_mock.get.return_value = self.reference2

        edit_object = Edit(self.service_mock, self.io_mock)
        edit_object.run()
        self.service_mock.put.assert_called()

    def test_ref_not_in_db(self):
        self.io_mock.read.side_effect = ["2", "", "", "", "", "", ""]

        def put(a, b, c):
            return

        self.service_mock.put.side_effect = put
        self.service_mock.id_exists.return_value = False
        self.service_mock.get_type.return_value = "book"
        self.service_mock.get.return_value = self.reference2

        edit_object = Edit(self.service_mock, self.io_mock)
        edit_object.run()
        print(self.io_mock.write.call_args.args[0])
        self.assertTrue("No such reference ID exists" in self.io_mock.write.call_args.args[0])

    def test_edit_inproceedings(self):
        self.io_mock.read.side_effect = ["3", "title", "booktitle", "newauthor", "newseries", "", "", "", "", "newtag"]
        self.service_mock.id_exists.return_value = True
        self.service_mock.get_type.return_value = "inproceedings"
        self.service_mock.get.return_value = self.reference2

        edit_object = Edit(self.service_mock, self.io_mock)
        edit_object.run()

        self.service_mock.put.assert_called_with("3", "tag", ["newtag"])

    def test_empty(self):
        self.io_mock.read.side_effect = ["3", "", "", "", "", "", "", "", "", ""]
        self.service_mock.id_exists.return_value = True
        self.service_mock.get_type.return_value = "inproceedings"
        self.service_mock.get.return_value = self.reference2

        edit_object = Edit(self.service_mock, self.io_mock)
        edit_object.run()

        self.service_mock.put.assert_called_with("3", "tag", [""])

