import unittest
from services import ReferenceService
from entities import Reference


class ReferenceServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = ReferenceService()
        self.service.delete_all()
        self.fake_reference = Reference(
            reference_id="1",
            authors=["test_author", "test_author_2"],
            title="Moomie",
            year=2020,
            publisher="Dotterbolaget"
        )
        self.fake_reference_2 = Reference(
            reference_id="2",
            authors=["test_author_2", "test_author_3"],
            title="Winnie the Pooh",
            year=1999,
            publisher="Epic Games"
        )

    def test_id_exists(self):
        self.service.post(self.fake_reference)
        self.assertTrue(self.service.id_exists(1))

    def test_get(self):
        self.service.post(self.fake_reference)
        self.assertEqual(self.fake_reference.to_dict(),
                         self.service.get(1).to_dict())

    def test_get_all(self):
        self.service.post(self.fake_reference)
        self.service.post(self.fake_reference_2)
        self.assertEqual([self.fake_reference.to_dict(), self.fake_reference_2.to_dict()], [
                         reference.to_dict() for reference in self.service.get_all()])

    def test_post(self):
        self.service.post(self.fake_reference)
        self.assertEqual(self.fake_reference.to_dict(),
                         self.service.get(1).to_dict())

    def test_put(self):
        self.service.post(self.fake_reference)
        fake_reference = Reference(
            reference_id="1",
            authors=["test_author_2", "test_author_3"],
            title="Winnie the Pooh",
            year=1999,
            publisher="Epic Games"
        )
        self.service.put(fake_reference)
        self.assertEqual(fake_reference.to_dict(),
                         self.service.get(1).to_dict())

    def test_delete(self):
        self.service.post(self.fake_reference)
        self.service.delete(1)
        self.assertFalse(self.service.id_exists(1))

    def test_delete_all(self):
        self.service.post(self.fake_reference)
        self.service.post(self.fake_reference_2)
        self.service.delete_all()
        self.assertEqual([], self.service.get_all())
