import unittest
from unittest.mock import Mock
from commands.add import Add
from entities.reference import Reference


class TestAdd(unittest.TestCase):
    def setUp(self):
        self.repository_mock = Mock()
        self.repository_mock.id_exists.return_value = False

        self.io_mock = Mock()

    def test_post_method_of_repository_is_called(self):
        self.io_mock.read.side_effect = [
            "title",
            "author",
            "2022",
            "publisher",
            ""
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called()

    def test_post_method_of_repository_is_called_with_correct_arguments(self):
        self.io_mock.read.side_effect = [
            "title",
            "author",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with(Reference(
            reference_id="author2022",
            authors=["author"],
            title="title",
            year=2022,
            publisher="publisher",
            tags=["tag"]
        ))

    def test_multiple_authors_can_be_provided(self):
        self.io_mock.read.side_effect = [
            "title",
            "author-one;author-two; author-three",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with(Reference(
            reference_id="authorone2022",
            authors=["author-one", "author-two", "author-three"],
            title="title",
            year=2022,
            publisher="publisher",
            tags=["tag"]
        ))

    def test_if_author_is_given_in_wrong_format_new_author_is_queried(self):
        self.io_mock.read.side_effect = [
            "title",
            "Invalid  Author",  # two spaces
            "Valid Author",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with(Reference(
            reference_id="Author2022",
            authors=["Valid Author"],
            title="title",
            year=2022,
            publisher="publisher",
            tags=["tag"]
        ))

    def test_multiple_tags_can_be_provided(self):
        self.io_mock.read.side_effect = [
            "title",
            "author",
            "2022",
            "publisher",
            "tag1;tag2; tag3"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with(Reference(
            reference_id="author2022",
            authors=["author"],
            title="title",
            year=2022,
            publisher="publisher",
            tags=["tag1", "tag2", "tag3"]
        ))

    def test_if_title_is_too_long_new_title_is_queried(self):
        self.io_mock.read.side_effect = [
            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec p",
            "short title",
            "author",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with(Reference(
            reference_id="author2022",
            authors=["author"],
            title="short title",
            year=2022,
            publisher="publisher",
            tags=["tag"]
        ))

    def test_if_year_is_nonnumeric_new_year_is_queried(self):
        self.io_mock.read.side_effect = [
            "title",
            "author",
            "not a number",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with(Reference(
            reference_id="author2022",
            authors=["author"],
            title="title",
            year=2022,
            publisher="publisher",
            tags=["tag"]
        ))

    def test_if_year_is_negative_new_year_is_queried(self):
        self.io_mock.read.side_effect = [
            "title",
            "author",
            "-1",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with(Reference(
            reference_id="author2022",
            authors=["author"],
            title="title",
            year=2022,
            publisher="publisher",
            tags=["tag"]
        ))

    def test_if_year_is_too_large_new_year_is_queried(self):
        self.io_mock.read.side_effect = [
            "title",
            "author",
            "999999999999",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with(Reference(
            reference_id="author2022",
            authors=["author"],
            title="title",
            year=2022,
            publisher="publisher",
            tags=["tag"]
        ))
