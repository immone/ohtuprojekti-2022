import unittest
from unittest.mock import Mock
from commands.edit import Edit
from entities.reference import Reference
from repositories.reference_repository import ReferenceRepository
from services.reference_service import ReferenceService

SMITH_REF = Reference(
    reference_id="Smith2019",
    authors=["Jane Smith", "John Doe"],
    title="The Origins of Life: A Comprehensive Guide",
    year=2019,
    publisher="Oxford University Press",
    tags="[Smith]"
)

SMITH_REF2 = Reference(
    reference_id="Smith2019",
    authors=["Test"],
    title="Test",
    year=1111,
    publisher="Test",
    tags="[Test]"
)

SMITH_REF3 = Reference(
    reference_id="Smith2019",
    authors=["Jane Smith", "John Doe"],
    booktitle = "Book of Smith",
    series = "Series",
    title="The Origins of Life: A Comprehensive Guide",
    year=2019,
    pages = "1--100",
    publisher="Oxford University Press",
    tags="[Smith]"
)

class TestEdit(unittest.TestCase):
    def setUp(self):
        self.repository_mock = Mock()
        self.repository_mock.post(SMITH_REF)
        self.reference_repository = ReferenceRepository()
        self.service = ReferenceService()
        self.service_mock = Mock()
        self.io_mock = Mock()

    def test_calls(self):
        def put(ref):
            return None
        def get(ref):
            return SMITH_REF

        self.repository_mock.put.side_effect = put
        self.service_mock.get.side_effect = get

        self.io_mock.read.side_effect = ["Smith2019", "", "", "", "", ""]
        edit_object = Edit(self.repository_mock, self.io_mock)
        edit_object.run()
        self.repository_mock.put.assert_called()

    def test_ref_not_in_db(self):
        self.reference_repository.post(SMITH_REF)
        self.io_mock.read.side_effect = ["Nonexistent",
                                         "Smith2019",
                                         "Test",
                                         "Test",
                                         "1111",
                                         "Test",
                                         "Test"]
        edit_object = Edit(self.reference_repository, self.io_mock)
        edit_object.run()
        all_ref = self.service.get_all()
        self.assertTrue(SMITH_REF2.year == all_ref[0]["year"] and
                        SMITH_REF2.title == all_ref[0]["title"] and
                        SMITH_REF2.reference_id == all_ref[0]["reference_id"] and
                        SMITH_REF2.publisher == all_ref[0]["publisher"])

    def test_edit_inproceedings(self):
        self.reference_repository.post(SMITH_REF3)
        self.io_mock.read.side_effect = ["Smith2019",
                                         "New Title",
                                         "[Author1; Author2]",
                                         "Series2",
                                         "1999",
                                         "2--3",
                                         "",
                                         "",
                                         "[new]"]
        edit_object = Edit(self.reference_repository, self.io_mock)
        edit_object.run()
        all_ref = self.service.get_all()
        self.assertTrue(1999 == all_ref[0]["year"] and
                        "New Title" == all_ref[0]["title"] and
                        "Series2" == all_ref[0]["series"] and
                        "[new]" == all_ref[0]["tag"])

    def test_empty(self):
        self.reference_repository.post(SMITH_REF3)
        self.io_mock.read.side_effect = ["", "", "", "","", "","", "", ""]
        edit_object = Edit(self.reference_repository, self.io_mock)
        edit_object.run()
        all_ref = self.service.get_all()
        self.assertTrue(SMITH_REF3.year == all_ref[0]["year"] and
                        SMITH_REF3.title == all_ref[0]["title"] and
                        SMITH_REF3.series == all_ref[0]["series"] and
                        SMITH_REF3.tags == all_ref[0]["tag"])


