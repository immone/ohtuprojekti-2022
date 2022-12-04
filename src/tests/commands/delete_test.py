import unittest
from unittest.mock import Mock, patch
from repositories.reference_repository import ReferenceRepository
from commands.add import Add
from io import StringIO
from commands.delete import Delete
from entities.reference import Reference
from database_connection import get_database_connection

class TestDelete(unittest.TestCase):
    def setUp(self):
        self.connection = get_database_connection()
        self.repository_mock = Mock()
        self.mock_reference = Reference(
            reference_id="id",
            authors=["author"],
            title="value",
            year=1234,
            publisher="value"
        )
        self.repository_mock.post(self.mock_reference)
        self.io_mock = Mock()


    def test_delete_method_of_repository_called(self):
        self.io_mock.read.side_effect = ["id"]
        delete = Delete(self.repository_mock, self.io_mock)
        delete.run()
        self.repository_mock.delete.assert_called_with("id")

    def test_delete_when_id_doesnt_exist(self):
        self.reference_repository = ReferenceRepository(self.connection)
        self.mock_reference = Reference(
            reference_id="id",
            authors=["author"],
            title="field",
            year=1234,
            publisher="field"
        )
        self.reference_repository.post(self.mock_reference)
        self.io_mock.read.side_effect = ["id2"]
        delete = Delete(self.reference_repository, self.io_mock)
        self.assertRaises(StopIteration, delete.run)

    def test_when_exists(self):
        self.reference_repository = ReferenceRepository(self.connection)
        self.mock_reference = Reference(
            reference_id="id",
            authors=["author"],
            title="field",
            year=1234,
            publisher="field"
        )
        self.io_mock.read.side_effect = ["id"]
        delete = Delete(self.reference_repository, self.io_mock)
        delete.run()
        self.assertFalse(self.reference_repository.id_exists("id"))
        self.assertRaises(StopIteration, delete.run)
