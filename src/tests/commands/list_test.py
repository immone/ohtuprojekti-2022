import unittest
from unittest.mock import Mock
from commands.list import List
from entities.reference import Reference
from database_connection import get_database_connection
from repositories.reference_repository import ReferenceRepository

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
        self.connection = get_database_connection()
        self.reference_repository = ReferenceRepository(self.connection)
        self.reference_repository.delete_all()


    def test_output_one(self):
        ref = SMITH_REF
        self.reference_repository.post(SMITH_REF)
        print_object = List(self.reference_repository, self.io_mock)
        print_object.run()
        self.assertIn(ref.title, self.io_mock.write.call_args.args[0])

    def test_output_two(self):
        ref = SMITH_REF
        self.reference_repository.post(ref)
        print_object = List(self.reference_repository, self.io_mock)
        print_object.run()
        self.assertIn(ref.title, self.io_mock.write.call_args.args[0])
        ref = WILLIAMS_REF
        self.reference_repository.post(ref)
        print_object.run()
        self.assertIn(ref.title, self.io_mock.write.call_args.args[0])
