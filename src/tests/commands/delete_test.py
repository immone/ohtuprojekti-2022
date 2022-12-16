import unittest
from unittest.mock import Mock
from services import ReferenceService
from commands.delete import Delete

class TestDelete(unittest.TestCase):
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
            "tag": ["test_tag3", "test_tag_4"]
        }
        self.service_mock = Mock()
        self.io_mock = Mock()

    def test_delete_method_of_repository_called(self):
        self.io_mock.read.return_value = "id"
        delete = Delete(self.service_mock, self.io_mock)
        delete.run()
        self.service_mock.delete.assert_called_with("id")

    def test_delete_when_id_doesnt_exist(self):
        self.service_mock.id_exists.return_value = False
        delete = Delete(self.service_mock, self.io_mock)
        delete.run()
        self.assertTrue("No such reference ID exists\n" in self.io_mock.write.call_args.args[0])

    def test_when_exists(self):
        self.service.post(self.reference)
        self.io_mock.read.return_value = "2"
        delete = Delete(self.service, self.io_mock)
        delete.run()
        print(self.io_mock.write.call_args.args[0])
        print(self.io_mock.write.call_args.args[0])
        self.assertTrue("Reference deleted." in self.io_mock.write.call_args.args[0])

    def test_multiple(self):
        self.service.post(self.reference)
        self.service.post(self.reference2)
        self.io_mock.read.return_value = "2"
        delete = Delete(self.service, self.io_mock)
        delete.run()
        self.assertFalse(self.service.id_exists("2"))
        self.assertTrue(self.service.id_exists("3"))
