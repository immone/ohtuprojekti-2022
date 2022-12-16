import unittest
from unittest.mock import Mock
from commands.search import Search, ref_to_str


SMITH_REF = {
    "type": "book",
    "reference_id": "Smith2019",
    "author": ["Jane Smith", "John Doe"],
    "title": "The Origins of Life: A Comprehensive Guide",
    "year": 2019,
    "publisher": "Oxford University Press"
}

RODR_REF = {
    "type": "book",
    "reference_id": "Rodriguez2020",
    "author": ["Maria Rodriguez", "David Johnson"],
    "title": "Advanced Quantum Mechanics: Theory and Applications",
    "year": 2020,
    "publisher": "Cambridge University Press"
}

JOHNSON_REF = {
    "type": "book",
    "reference_id": "Johnson2021",
    "author": ["Sarah Johnson", "William Thompson"],
    "title": "The Evolution of Human Language: From Grunts to Grammar",
    "year": 2021,
    "publisher": "Harvard University Press"
}

WILLIAMS_REF = {
    "type": "book",
    "reference_id": "Williams2022",
    "author": ["David Williams", "Elizabeth Taylor"],
    "title": "The Future of Artificial Intelligence: Implications and Opportunities",
    "year": 2022,
    "publisher": "Princeton University Press"
}

ALL_REFS = [SMITH_REF, RODR_REF, JOHNSON_REF, WILLIAMS_REF]


class TestAdd(unittest.TestCase):
    def setUp(self):
        self.service_mock = Mock()
        self.service_mock.get_all.return_value = ALL_REFS

        self.io_mock = Mock()

    def test_search_by_id(self):
        self.io_mock.read.return_value = "williams2022"

        search = Search(self.service_mock, self.io_mock)
        search.run()
        
        self.assertTrue(ref_to_str(WILLIAMS_REF) in self.io_mock.write.call_args.args[0])

    def test_search_by_authors(self):
        self.io_mock.read.return_value = "rodriguez"

        search = Search(self.service_mock, self.io_mock)
        search.run()
        
        self.assertTrue(ref_to_str(RODR_REF) in self.io_mock.write.call_args.args[0])

    def test_search_by_title(self):
        self.io_mock.read.return_value = "evolution"

        search = Search(self.service_mock, self.io_mock)
        search.run()

        self.assertTrue(ref_to_str(JOHNSON_REF) in self.io_mock.write.call_args.args[0])

    def test_search_by_year(self):
        self.io_mock.read.return_value = "2019"

        search = Search(self.service_mock, self.io_mock)
        search.run()

        self.assertTrue(ref_to_str(SMITH_REF) in self.io_mock.write.call_args.args[0])

    def test_search_by_publisher_multiple_results(self):
        self.io_mock.read.return_value = "press"

        search = Search(self.service_mock, self.io_mock)
        search.run()

        def get_ref_id(ref):
            return ref["reference_id"]

        ref_reprs = [f"\t{ref_to_str(ref)} (id: {get_ref_id(ref)})" for ref in ALL_REFS]
        expected = [f"{len(ALL_REFS)} reference(s) matched one or more of the search terms:"] + ref_reprs

        self.assertEqual(expected, [args[0][0] for args in self.io_mock.write.call_args_list])