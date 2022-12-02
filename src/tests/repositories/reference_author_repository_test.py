import unittest
from database_connection import get_database_connection
from repositories.reference_author_repository import ReferenceAuthorRepository
from repositories.author_repository import AuthorRepository
from repositories.reference_repository import ReferenceRepository
from entities.reference import Reference


class ReferenceAuthorRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.connection = get_database_connection()
        ReferenceRepository().delete_all()
        self.author_repository = AuthorRepository(self.connection)
        self.reference_author_repository = ReferenceAuthorRepository(
            self.connection, self.author_repository)
        self.mock_reference = Reference(
            reference_id="1",
            authors=["Test Author 1", "Test Author 2"],
            title="Test Title",
            year="2020",
            publisher="Test Publisher"
        )
        self.reference_author_repository.post(self.mock_reference)

    def test_reference_author_repository_exits(self):
        self.assertIsNotNone(self.reference_author_repository)

    def test_get(self):
        reference_authors = self.reference_author_repository.get(
            self.mock_reference.reference_id)
        self.assertEqual(self.mock_reference.authors, reference_authors)

    def test_get_non_existent_reference(self):
        reference_authors = self.reference_author_repository.get(
            "Non Existent Reference")
        self.assertEqual([], reference_authors)

    def test_post_reference(self):
        mock_reference = Reference(
            reference_id="2",
            authors=["Test Author 1", "Test Author 2"],
            title="Test Title",
            year="2020",
            publisher="Test Publisher"
        )
        self.reference_author_repository.post(mock_reference)
        reference_authors = self.reference_author_repository.get(
            mock_reference.reference_id)
        self.assertEqual(mock_reference.authors, reference_authors)
        self.assertEqual(1, self.author_repository.get("Test Author 1"))

    def test_post_identical_reference_causes_error(self):
        with self.assertRaises(Exception):
            self.reference_author_repository.post(self.mock_reference)

    def test_put_reference(self):
        mock_reference = Reference(
            reference_id="2",
            authors=["Test Author 1", "Test Author 2"],
            title="Test Title",
            year="2020",
            publisher="Test Publisher"
        )
        self.reference_author_repository.post(mock_reference)
        mock_reference._Reference__authors = ["Test Author 1", "Test Author 3"]
        self.reference_author_repository.put(mock_reference)
        reference_authors = self.reference_author_repository.get(
            mock_reference.reference_id)
        self.assertEqual(mock_reference.authors, reference_authors)
        self.assertEqual(1, self.author_repository.get("Test Author 1"))
        self.assertEqual(3, self.author_repository.get("Test Author 3"))

    def test_delete(self):
        self.reference_author_repository.delete(
            self.mock_reference.reference_id)
        reference_authors = self.reference_author_repository.get(
            self.mock_reference.reference_id)
        self.assertEqual([], reference_authors)

    def test_delete_non_existent_reference(self):
        self.reference_author_repository.delete("Non Existent Reference")
        reference_authors = self.reference_author_repository.get(
            self.mock_reference.reference_id)
        self.assertEqual(self.mock_reference.authors, reference_authors)

    def test_delete_reference_deletes_author(self):
        self.reference_author_repository.delete(
            self.mock_reference.reference_id)
        self.assertIsNone(self.author_repository.get("Test Author 1"))
        self.assertIsNone(self.author_repository.get("Test Author 2"))
