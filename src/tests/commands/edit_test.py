import unittest
from unittest.mock import Mock
from commands.edit import Edit
from entities.reference import Reference
from database_connection import get_database_connection
from repositories.reference_repository import ReferenceRepository
from services.reference_service import ReferenceService

SMITH_REF = Reference(
    reference_id="Smith2019",
    authors=["Jane Smith", "John Doe"],
    title="The Origins of Life: A Comprehensive Guide",
    year=2019,
    publisher="Oxford University Press",
    tags="Smith"
)

SMITH_REF2 = Reference(
    reference_id="Smith2019",
    authors=["Test"],
    title="Test",
    year=1111,
    publisher="Test",
    tags="Test"
)

class TestEdit(unittest.TestCase):
    def setUp(self):
        self.connection = get_database_connection()
        self.reference_repository = ReferenceRepository(self.connection)
        self.reference_repository.delete_all()
        self.repository_mock = Mock()
        self.repository_mock.post(SMITH_REF)
        self.service = ReferenceService()
        self.io_mock = Mock()

    def test_calls(self):
        def put(ref):
            return None
        self.repository_mock.put.side_effect = put
        self.io_mock.read.side_effect = ["Smith2019",
                                         "Test",
                                         "Test",
                                         "1111",
                                         "Test",
                                         "Test"]
        edit_object = Edit(self.repository_mock, self.io_mock)
        edit_object.run()
        self.repository_mock.put.assert_called()

    def test_ref_not_in_db(self):
        self.reference_repository.post(SMITH_REF)
        self.io_mock.read.side_effect = ["Nonexistent",
                                         "Smith2019",
                                         "Test",
                                         "Test",
                                         "1111",
                                         "Test",
                                         "Test"]
        edit_object = Edit(self.reference_repository, self.io_mock)
        edit_object.run()
        all_ref = self.service.get_all()
        self.assertTrue(SMITH_REF2.year == all_ref[0].year and
                        SMITH_REF2.title == all_ref[0].title and
                        SMITH_REF2.reference_id == all_ref[0].reference_id and
                        SMITH_REF2.publisher == all_ref[0].publisher)

