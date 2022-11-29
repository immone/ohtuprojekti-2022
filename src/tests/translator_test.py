import unittest
from unittest.mock import Mock
from commands.translator import Translator
from entities.reference import Reference
from repositories.reference_repository import ReferenceRepository

class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.repository_mock = Mock()
        self.repository_mock.get_all.return_value = [Reference(
            reference_id="refid",
            authors=["author"],
            title="title",
            year=2022,
            publisher="publisher"
            )]
        self.io_mock = Mock()

    def test_tries_to_load_database(self):
        self.io_mock.read.side_effect = "A"

        test_translator = (Translator(self.repository_mock, self.io_mock))
        test_translator.run()

        self.repository_mock.get_all.assert_called()

        


