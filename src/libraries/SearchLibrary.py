from unittest.mock import Mock

import sys
sys.path.append(sys.path[0] + "/..")


from entities.reference import Reference
from commands.search import Search


SMITH_REF = Reference(
    reference_id="Smith2019",
    authors=["Jane Smith", "John Doe"],
    title="The Origins of Life: A Comprehensive Guide",
    year=2019,
    publisher="Oxford University Press"
)

RODR_REF = Reference(
    reference_id="Rodriguez2020",
    authors=["Maria Rodriguez", "David Johnson"],
    title="Advanced Quantum Mechanics: Theory and Applications",
    year=2020,
    publisher="Cambridge University Press"
)

JOHNSON_REF = Reference(
    reference_id="Johnson2021",
    authors=["Sarah Johnson", "William Thompson"],
    title="The Evolution of Human Language: From Grunts to Grammar",
    year=2021,
    publisher="Harvard University Press"
)

WILLIAMS_REF = Reference(
    reference_id="Williams2022",
    authors=["David Williams", "Elizabeth Taylor"],
    title="The Future of Artificial Intelligence: Implications and Opportunities",
    year=2022,
    publisher="Princeton University Press"
)

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
        
        print(f"WRITE ARGS: {write_args}")
        
        expected = expected.split()

        for e in expected:
            found = False
            for arg in write_args:
                if str(REFS_DICT[e]) in arg:
                    found = True

            if not found:
                raise AssertionError(f"Reference {e} was not in the search results")
