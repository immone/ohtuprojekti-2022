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
            "1",
            "title",
            "author",
            "2022",
            "publisher",
            ""
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called()

    def test_post_method_of_repository_is_called_with_correct_arguments_with_book_ref(self):
        self.io_mock.read.side_effect = [
            "1",
            "title",
            "author",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with({
            "type": "book",
            "title": "title",
            "author":["author"],
            "year": 2022,
            "publisher": "publisher",
            "tag": ["tag"],
            "reference_id": "author2022"
        })

    def test_post_method_of_repository_is_called_with_correct_arguments_with_inproceedings_ref(self):
        self.io_mock.read.side_effect = [
            "2",
            "title",
            "booktitle",
            "author",
            "series",
            "2022",
            "100--200",
            "publisher",
            "address",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with({
            "type": "inproceedings",
            "title": "title",
            "booktitle": "booktitle",
            "author":["author"],
            "series": "series",
            "year": 2022,
            "pages": "100--200",
            "publisher": "publisher",
            "address": "address",
            "tag": ["tag"],
            "reference_id": "author2022"
        })

    def test_post_method_of_repository_is_called_with_correct_arguments_with_misc_ref(self):
        self.io_mock.read.side_effect = [
            "3",
            "title",
            "author",
            "howpublished",
            "2022",
            "note",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with({
            "type": "misc",
            "title": "title",
            "author":["author"],
            "howpublished": "howpublished",
            "year": 2022,
            "note": "note",
            "tag": ["tag"],
            "reference_id": "author2022"
        })

    def test_multiple_authors_can_be_provided(self):
        self.io_mock.read.side_effect = [
            "1",
            "title",
            "author-one;author-two; author-three",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with({
            "type": "book",
            "title": "title",
            "author":["author-one", "author-two", "author-three"],
            "year": 2022,
            "publisher": "publisher",
            "tag": ["tag"],
            "reference_id": "authorone2022"
        })

    def test_if_author_is_given_in_wrong_format_new_author_is_queried(self):
        self.io_mock.read.side_effect = [
            "1",
            "title",
            "Invalid  Author",  # two spaces
            "Valid Author",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with({
            "type": "book",
            "title": "title",
            "author":["Valid Author"],
            "year": 2022,
            "publisher": "publisher",
            "tag": ["tag"],
            "reference_id": "Author2022"
        })

    def test_multiple_tags_can_be_provided(self):
        self.io_mock.read.side_effect = [
            "1",
            "title",
            "author",
            "2022",
            "publisher",
            "tag1;tag2; tag3"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with({
            "type": "book",
            "title": "title",
            "author":["author"],
            "year": 2022,
            "publisher": "publisher",
            "tag": ["tag1", "tag2", "tag3"],
            "reference_id": "author2022"
        })

    def test_if_title_is_too_long_new_title_is_queried(self):
        self.io_mock.read.side_effect = [
            "1",
            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec p",
            "short title",
            "author",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with({
            "type": "book",
            "title": "short title",
            "author":["author"],
            "year": 2022,
            "publisher": "publisher",
            "tag": ["tag"],
            "reference_id": "author2022"
        })

    def test_if_year_is_nonnumeric_new_year_is_queried(self):
        self.io_mock.read.side_effect = [
            "1",
            "title",
            "author",
            "not a number",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with({
            "type": "book",
            "title": "title",
            "author":["author"],
            "year": 2022,
            "publisher": "publisher",
            "tag": ["tag"],
            "reference_id": "author2022"
        })

    def test_if_year_is_negative_new_year_is_queried(self):
        self.io_mock.read.side_effect = [
            "1",
            "title",
            "author",
            "-1",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with({
            "type": "book",
            "title": "title",
            "author":["author"],
            "year": 2022,
            "publisher": "publisher",
            "tag": ["tag"],
            "reference_id": "author2022"
        })


    def test_if_year_is_too_large_new_year_is_queried(self):
        self.io_mock.read.side_effect = [
            "1",
            "title",
            "author",
            "999999999999",
            "2022",
            "publisher",
            "tag"
        ]

        add = Add(self.repository_mock, self.io_mock)
        add.run()

        self.repository_mock.post.assert_called_with({
            "type": "book",
            "title": "title",
            "author":["author"],
            "year": 2022,
            "publisher": "publisher",
            "tag": ["tag"],
            "reference_id": "author2022"
        })