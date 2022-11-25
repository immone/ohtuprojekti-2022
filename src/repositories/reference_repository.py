from entities.reference import Reference
from database_connection import get_database_connection
from repositories.author_repository import AuthorRepository
from repositories.reference_author_repository import ReferenceAuthorRepository


class ReferenceRepository:
    def __init__(self):
        self.connection = get_database_connection()
        self.author_repository = AuthorRepository()
        self.reference_author_repository = ReferenceAuthorRepository()

    def id_exists(self, reference_id: str) -> bool:
        """Returns True if reference_id exists in the database"""

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM reference WHERE reference_id = :reference_id",
                       {"reference_id": reference_id})
        reference = cursor.fetchone()
        return reference is not None

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM reference")
        references = cursor.fetchall()
        reference_lst = []
        for reference in references:
            authors = self.reference_author_repository.get(
                reference["reference_id"])
            reference_lst.append(Reference(
                reference_id=reference["reference_id"],
                authors=authors,
                title=reference["title"],
                year=reference["year"],
                publisher=reference["publisher"]
            ))
        return reference_lst

    def post(self, reference: Reference):
        self.reference_author_repository.post(reference)
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO
                reference (reference_id, title, year, publisher) 
                VALUES (:reference_id, :title, :year, :publisher)
            """,
            reference.to_dict()
        )
        self.connection.commit()

    def delete(self, reference_id: str):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM reference WHERE reference_id = :reference_id",
                       {"reference_id": reference_id})
        self.connection.commit()

    def delete_all(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM reference")
        cursor.execute("DELETE FROM author")
        cursor.execute("DELETE FROM reference_author")
        self.connection.commit()

    def insert_mock_data(self):
        reference = Reference(
            reference_id="1",
            authors=["John Doe", "Jane Doe"],
            title="A title",
            year=2020,
            publisher="A publisher"
        )
        self.post(reference)
        reference = Reference(
            reference_id="2",
            authors=["John Talker", "Jane Doe"],
            title="A second title",
            year=2020,
            publisher="A publisher"
        )
        self.post(reference)
