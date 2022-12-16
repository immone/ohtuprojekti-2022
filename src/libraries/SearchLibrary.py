from unittest.mock import Mock

import sys
sys.path.append(sys.path[0] + "/..")


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

REFS_DICT = {
    "SMITH": SMITH_REF,
    "RODRIGUEZ": RODR_REF,
    "JOHNSON": JOHNSON_REF,
    "WILLIAMS": WILLIAMS_REF
}

REFS_LIST = [SMITH_REF, RODR_REF, JOHNSON_REF, WILLIAMS_REF]


class SearchLibrary:
    def __init__(self):
        self.terms = ""

    def input_terms(self, terms):
        self.terms = terms

    def results_should_contain(self, expected):
        service_mock = Mock()
        service_mock.get_all.return_value = REFS_LIST

        io_mock = Mock()
        io_mock.read.return_value = self.terms

        search = Search(service_mock, io_mock)
        search.run()

        write_args = [args[0][0] for args in io_mock.write.call_args_list]
                
        expected = expected.split()

        for e in expected:
            found = False
            for arg in write_args:
                if ref_to_str(REFS_DICT[e]) in arg:
                    found = True

            if not found:
                raise AssertionError(f"Reference {e} was not in the search results")
