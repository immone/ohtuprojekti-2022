import unittest
from unittest.mock import Mock
from commands.list import List
from entities.reference import Reference

SMITH_REF = Reference(
    reference_id="Smith2019",
    authors=["Jane Smith", "John Doe"],
    title="The Origins of Life: A Comprehensive Guide",
    year=2019,
    publisher="Oxford University Press"
)

WILLIAMS_REF = Reference(
    reference_id="Williams2022",
    authors=["David Williams", "Elizabeth Taylor"],
    title="The Future of Artificial Intelligence: Implications and Opportunities",
    year=2022,
    publisher="Princeton University Press"
)

ALL_REFS = [SMITH_REF, WILLIAMS_REF]


class ListTest(unittest.TestCase):
    def setUp(self):
        self.io_mock = Mock()
        self.service_mock = Mock()
        self.io_mock = Mock()
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

    def test_empty(self):
        self.io_mock.read.return_value = "n"
        self.service_mock.get_all.return_value = []
        list_object = List(self.service_mock, self.io_mock)
        list_object.run()
        self.assertTrue("There are no references to be listed." in self.io_mock.write.call_args.args[0])

    def test_output_no_tags(self):
        self.io_mock.read.return_value = "n"
        self.service_mock.get_all.return_value = [self.reference]
        print_object = List(self.service_mock, self.io_mock)
        print_object.run()
        self.assertIn("Tags: test_tag2, test_tag_3", self.io_mock.write.call_args_list[-2].args[0])

    def test_output_tags_any(self):
        self.io_mock.read.side_effect = ["y", "test_tag3", "any"]
        self.service_mock.get_all.return_value = [self.reference]
        self.service_mock.get_by_tag.return_value = [self.reference2]
        print_object = List(self.service_mock, self.io_mock)
        print_object.run()
        self.assertIn("Tags: test_tag3, test_tag_4", self.io_mock.write.call_args_list[-2].args[0])

    def test_output_tags_all(self):
        self.io_mock.read.side_effect = ["y", "test_tag2", "any"]
        self.service_mock.get_all.return_value = [self.reference]
        self.service_mock.get_by_tag.return_value = [self.reference2]
        print_object = List(self.service_mock, self.io_mock)
        print_object.run()
        self.assertIn("Tags: test_tag3, test_tag_4", self.io_mock.write.call_args_list[-2].args[0])

    def test_output_tags_all2(self):
        self.io_mock.read.side_effect = ["y", "test_tag2;test_tag_3", "any"]
        self.service_mock.get_all.return_value = [self.reference]
        self.service_mock.get_by_tag.return_value = [self.reference2]
        print_object = List(self.service_mock, self.io_mock)
        print_object.run()
        self.assertIn("Tags: test_tag3, test_tag_4", self.io_mock.write.call_args_list[-2].args[0])

