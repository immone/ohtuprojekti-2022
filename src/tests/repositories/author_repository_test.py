import unittest
from database_connection import get_database_connection
from repositories import AuthorRepository, ReferenceRepository


class AuthorRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.connection = get_database_connection()
        self.reference_repository = ReferenceRepository(self.connection)
        self.reference_repository.delete_all()
        self.author_repository = AuthorRepository(self.connection)
        self.author_id = self.author_repository.post("Test Author")

    def test_author_repository_exits(self):
        self.assertIsNotNone(self.author_repository)

    def test_get(self):
        self.assertEqual(
            self.author_id, self.author_repository.get("Test Author"))

    def test_get_non_existent_author(self):
        self.assertIsNone(self.author_repository.get("Non Existent Author"))

    def test_post_author(self):
        self.assertEqual(2, self.author_repository.post("second author"))
        self.assertEqual(2, self.author_repository.get("second author"))

    def test_post_identical_author(self):
        self.assertEqual(1, self.author_repository.post("Test Author"))
        self.assertEqual(1, self.author_repository.get("Test Author"))

    def test_delete(self):
        self.author_repository.delete(self.author_id)
        self.assertIsNone(self.author_repository.get("Test Author"))

    def test_delete_non_existent_author(self):
        self.author_repository.delete(999)
        self.assertEqual(1, self.author_repository.get("Test Author"))
