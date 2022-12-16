import unittest
from unittest.mock import Mock, MagicMock
from commands.translator import Translator

class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.repository_mock = Mock()
        self.search_mock = MagicMock()
        self.repository_mock.get_all.return_value = [
                {
                    "reference_id":"bb2022",
                    "authors":["bbbbbbbb","cccccccc","dddddddd"],
                    "title":"title2",
                    "year":"2022",
                    "publisher":"publisher2",
                    "type":"book",
                    "tag":[]
                    }]
        self.io_mock = MagicMock()
        self.test_translator = Translator(self.repository_mock, self.io_mock,self.search_mock)

    def test_tries_to_load_database(self):

        self.io_mock.read.return_value = ""
        self.test_translator.run()

        self.repository_mock.get_all.assert_called()

    def test_parses_authors_correctly(self):

        self.io_mock.read.return_value = ""
        self.test_translator.run()

        self.io_mock.write.assert_any_call("  title           = {title2}, ")
        self.io_mock.write.assert_any_call("  year            = {2022}, ")
        self.io_mock.write.assert_any_call("  publisher       = {publisher2}, ")
        self.io_mock.write.assert_any_call("  authors         = {bbbbbbbb; cccccccc; dddddddd}, ")
