import unittest
from unittest.mock import Mock, patch
from repositories.reference_repository import ReferenceRepository
from commands.add import Add
from io import StringIO
from commands.print import Print
from entities.reference import Reference

class PrintTest(unittest.TestCase):
    def setUp(self):
        self.io_mock = Mock()

    def test_calls_get_all(self):
        self.repository_mock = Mock()
        def get_all():
            return []
        print = Print(self.repository_mock, self.io_mock)
        self.repository_mock.get_all.side_effect = get_all
        print.run()
        self.repository_mock.get_all.assert_called()
