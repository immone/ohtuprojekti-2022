import unittest
from database_connection import get_database_connection
from repositories import ReferenceTagRepository, TagRepository


class TagRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.__connection = get_database_connection()
        self.__tag_repository = TagRepository(self.__connection)
        self.__reference_tag_repository = ReferenceTagRepository(
            self.__connection, self.__tag_repository)
        self.__reference_tag_repository.delete_all()
        self.__tag_repository.post("Test")

    def test_get(self):
        self.assertEqual(1, self.__tag_repository.get("Test"))

    def test_post(self):
        self.assertEqual(2, self.__tag_repository.post("Test2"))
        self.assertEqual(2, self.__tag_repository.get("Test2"))

    def test_delete(self):
        self.__tag_repository.delete(1)
        self.assertIsNone(self.__tag_repository.get("Test"))

    def test_delete_non_existent_tag(self):
        self.__tag_repository.delete(999)
        self.assertEqual(1, self.__tag_repository.get("Test"))

    def test_get_non_existent_tag(self):
        self.assertIsNone(self.__tag_repository.get("Non Existent Tag"))

    def test_post_identical_tag(self):
        self.assertEqual(1, self.__tag_repository.post("Test"))
        self.assertEqual(1, self.__tag_repository.get("Test"))
