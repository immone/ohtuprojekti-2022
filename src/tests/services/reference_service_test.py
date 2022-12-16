import unittest
from services import ReferenceService


class ReferenceServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = ReferenceService()
        self.service.delete_all()
        self.article = {
            "reference_id": "1",
            "type": "article",
            "author": ["P. J. Cohen"],
            "title": "The independence of the continuum hypothesis",
            "journal": "Proceedings of the National Academy of Sciences",
            "year": "1963",
            "volume": "50",
            "number": "6",
            "pages": "1143--1148",
            "tag": ["test_tag1", "test_tag_2"]
        }
        self.book = {
            "reference_id": "2",
            "type": "book",
            "author": ["Leonard Susskind", "George Hrabovsky"],
            "title": "Classical mechanics: the theoretical minimum",
            "publisher": "Penguin Random House",
            "year": "2014",
            "tag": ["test_tag2", "test_tag_3"]
        }
        self.inproceedings = {
            "reference_id": "3",
            "type": "inproceedings",
            "author": ["Holleis, Paul", "Wagner, Matthias", "Koolwaaij, Johan"],
            "title": "Studying mobile context-aware social services in the wild",
            "booktitle": "Proc. of the 6th Nordic Conf. on Human-Computer Interaction",
            "series": "NordiCHI",
            "year": "2010",
            "pages": "207--216",
            "publisher": "ACM",
            "tag": ["test_tag3", "test_tag_4"]
        }
        self.misc = {
            "reference_id": "4",
            "type": "misc",
            "author": ["J. R. S. Blair"],
            "title": "The 3x3x3 Rubik's Cube",
            "howpublished": "http://www.cubewhiz.com/",
            "year": "2009",
            "tag": ["test_tag4", "test_tag_5"]
        }

    def test_can_post_article(self):
        self.service.post(self.article)
        self.assertTrue(self.service.id_exists(1))

    def test_can_post_book(self):
        self.service.post(self.book)
        self.assertTrue(self.service.id_exists(2))

    def test_can_post_inproceedings(self):
        self.service.post(self.inproceedings)
        self.assertTrue(self.service.id_exists(3))

    def test_can_post_misc(self):
        self.service.post(self.misc)
        self.assertTrue(self.service.id_exists(4))

    def test_id_exists(self):
        self.service.post(self.article)
        self.assertTrue(self.service.id_exists(1))

    def test_invalid_id_does_not_exist(self):
        self.service.post(self.article)
        self.assertFalse(self.service.id_exists(2))

    def test_get_type(self):
        self.service.post(self.article)
        self.assertEqual("article", self.service.get_type(1))

    def test_get_type_invalid_id(self):
        self.service.post(self.article)
        self.assertEqual(None, self.service.get_type(2))

    def test_get_fields(self):
        self.service.post(self.article)
        fields = sorted(["author", "title", "journal", "year",
                        "volume", "number", "pages", "tag"])
        self.assertEqual(fields, self.service.get_fields("article"))

    def test_get_fields_invalid_type(self):
        self.service.post(self.article)
        self.assertEqual([], self.service.get_fields("invalid_type"))

    def test_get(self):
        self.service.post(self.article)
        reference = self.service.get(1)
        del reference["reference_id"]
        del reference["type"]
        self.assertEqual(self.article, reference)

    def test_get_invalid_id(self):
        self.service.post(self.article)
        self.assertEqual({}, self.service.get(2))

    def test_get_all(self):
        self.service.post(self.article)
        self.service.post(self.book)
        self.service.post(self.inproceedings)
        self.service.post(self.misc)
        references = self.service.get_all()
        for i in references:
            del i["reference_id"]
            del i["type"]
        self.assertEqual(4, len(references))
        self.assertEqual(self.article, references[0])
        self.assertEqual(self.book, references[1])
        self.assertEqual(self.inproceedings, references[2])
        self.assertEqual(self.misc, references[3])

    def test_get_all_empty(self):
        self.assertEqual([], self.service.get_all())

    def test_post(self):
        self.service.post(self.article)
        article = self.service.get(1)
        del article["reference_id"]
        del article["type"]
        self.assertEqual(self.article, article)

    def test_post_invalid_type(self):
        self.article["type"] = "invalid_type"
        with self.assertRaises(Exception):
            self.service.post(self.article)
        self.assertFalse(self.service.id_exists(1))

    def test_post_invalid_field(self):
        self.article["invalid_field"] = "invalid_value"
        article = self.service.get(1)
        self.assertNotEqual(self.article, article)

    def test_put(self):
        self.service.post(self.article)
        self.service.put(1, "title", "new_title")
        self.assertEqual("new_title", self.service.get(1)["title"])

    def test_put_invalid_id(self):
        self.service.post(self.article)
        self.service.put(2, "title", "new_title")
        self.assertEqual(self.article["title"], self.service.get(1)["title"])

    def test_put_invalid_field(self):
        self.service.post(self.article)
        self.service.put(1, "invalid_field", "new_value")
        self.assertEqual(self.article["title"], self.service.get(1)["title"])

    def test_put_list(self):
        self.service.post(self.article)
        self.service.put(1, "tag", ["environment", "economy"])
        self.assertEqual(["environment", "economy"], self.service.get(1)["tag"])

    def test_delete(self):
        self.service.post(self.article)
        self.service.delete(1)
        self.assertFalse(self.service.id_exists(1))

    def test_delete_invalid_id(self):
        self.service.post(self.article)
        self.service.delete(2)
        self.assertTrue(self.service.id_exists(1))

    def test_delete_all(self):
        self.service.post(self.article)
        self.service.post(self.book)
        self.service.post(self.inproceedings)
        self.service.post(self.misc)
        self.service.delete_all()
        self.assertEqual([], self.service.get_all())
