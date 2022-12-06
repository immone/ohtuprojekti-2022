import unittest
from unittest.mock import Mock
from commands.print import Print


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
