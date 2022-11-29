from entities.reference import Reference
from database_connection import get_database_connection
from repositories.author_repository import AuthorRepository
from repositories.reference_author_repository import ReferenceAuthorRepository


class ReferenceRepository:
    def __init__(self) -> None:
        self.__connection = get_database_connection()
        self.__author_repository = AuthorRepository(self.__connection)
        self.__reference_author_repository = ReferenceAuthorRepository(
            self.__connection,
            self.__author_repository
        )

    def id_exists(self, reference_id: str) -> bool:
        """Returns True if reference_id exists in the database"""

        cursor = self.__connection.cursor()
        cursor.execute(
            """
            SELECT 
                * 
            FROM 
                reference 
            WHERE 
                reference_id = :reference_id
            """,
            {"reference_id": reference_id}
        )
        reference = cursor.fetchone()
        return reference is not None

    def get_all(self) -> list:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT * FROM reference")
        references = cursor.fetchall()
        reference_lst = []
        for reference in references:
            authors = self.__reference_author_repository.get(
                reference["reference_id"])
            reference_lst.append(Reference(
                reference_id=reference["reference_id"],
                authors=authors,
                title=reference["title"],
                year=reference["year"],
                publisher=reference["publisher"]
            ))
        return reference_lst

    def post(self, reference: Reference) -> None:
        self.__reference_author_repository.post(reference)
        cursor = self.__connection.cursor()
        cursor.execute(
            """
            INSERT INTO
                reference (reference_id, title, year, publisher) 
                VALUES (:reference_id, :title, :year, :publisher)
            """,
            reference.to_dict()
        )
        self.__connection.commit()

    def delete(self, reference_id: str) -> None:
        cursor = self.__connection.cursor()
        cursor.execute("DELETE FROM reference WHERE reference_id = :reference_id",
                       {"reference_id": reference_id})
        self.__reference_author_repository.delete(reference_id)
        self.__connection.commit()

    def delete_all(self) -> None:
        cursor = self.__connection.cursor()
        cursor.execute("DELETE FROM reference")
        cursor.execute("DELETE FROM author")
        cursor.execute("DELETE FROM reference_author")
        self.__connection.commit()
