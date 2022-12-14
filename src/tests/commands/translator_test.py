import unittest
from unittest.mock import Mock
from commands.translator import Translator
from entities.reference import Reference


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.repository_mock = Mock()
        self.repository_mock.get_all.return_value = [
        Reference(
            reference_id="bb2022",
            authors=["bbbbbbbb","cccccccc","dddddddd"],
            title="title2",
            year=2022,
            publisher="publisher2"
        )]
        self.io_mock = Mock()
        self.test_translator = (Translator(self.repository_mock, self.io_mock))

    def test_tries_to_load_database(self):

        self.test_translator.run()

        self.repository_mock.get_all.assert_called()

    def test_parses_authors_correctly(self):

        self.test_translator.run()
        self.io_mock.write.assert_any_call("  author    = {bbbbbbbb, cccccccc, dddddddd}, ")
