import unittest
from database_connection import get_database_connection
from repositories import ReferenceTagRepository, TagRepository
from entities import Reference


class ReferenceTagRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.__connection = get_database_connection()
        self.__tag_repository = TagRepository(self.__connection)
        self.__reference_tag_repository = ReferenceTagRepository(
            self.__connection, self.__tag_repository)
        self.__reference_tag_repository.delete_all()
        self.__test_reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test"]
        )

    def tearDown(self):
        self.__reference_tag_repository.delete_all()

    def test_get(self):
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test"]
        )
        self.__reference_tag_repository.post(reference)
        self.assertEqual(
            self.__reference_tag_repository.get(reference.reference_id),
            reference.tags
        )

    def test_post(self):
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test"]
        )
        self.__reference_tag_repository.post(reference)
        self.assertEqual(
            self.__reference_tag_repository.get(reference.reference_id),
            reference.tags
        )

    def test_put(self):
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test"]
        )
        self.__reference_tag_repository.post(reference)
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test", "Test 2"]
        )
        self.__reference_tag_repository.put(reference)
        self.assertEqual(
            self.__reference_tag_repository.get(reference.reference_id),
            reference.tags
        )

    def test_delete(self):
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test"]
        )
        self.__reference_tag_repository.post(reference)
        self.__reference_tag_repository.delete(reference.reference_id)
        self.assertEqual(
            self.__reference_tag_repository.get(reference.reference_id),
            []
        )

    def test_delete_all(self):
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test"]
        )
        self.__reference_tag_repository.post(reference)
        self.__reference_tag_repository.delete_all()
        self.assertEqual(
            self.__reference_tag_repository.get(reference.reference_id),
            []
        )

    def test_get_non_existent_reference(self):
        self.assertEqual(
            self.__reference_tag_repository.get(999),
            []
        )

    def test_post_identical_reference(self):
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test"]
        )
        self.__reference_tag_repository.post(reference)
        with self.assertRaises(Exception):
            self.__reference_tag_repository.post(reference)

    def test_post_identical_tag(self):
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test", "Test"]
        )
        with self.assertRaises(Exception):
            self.__reference_tag_repository.post(reference)

    def test_put_identical_tag(self):
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test"]
        )
        self.__reference_tag_repository.post(reference)
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test", "Test"]
        )
        with self.assertRaises(Exception):
            self.__reference_tag_repository.put(reference)

    def test_delete_non_existent_reference(self):
        reference = Reference(
            reference_id=1,
            authors=["John Doe"],
            title="Test",
            year=2020,
            publisher="Test",
            tags=["Test"]
        )
        self.__reference_tag_repository.post(reference)
        self.__reference_tag_repository.delete(999)
        self.assertEqual(
            self.__reference_tag_repository.get(reference.reference_id),
            reference.tags
        )
