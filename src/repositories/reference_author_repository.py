from database_connection import get_database_connection
from repositories.author_repository import AuthorRepository


class ReferenceAuthorRepository:
    def __init__(self):
        self.connection = get_database_connection()
        self.author_repository = AuthorRepository()

    def get(self, reference_id: object):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM reference_author ra LEFT JOIN author a ON ra.author_id = a.author_id WHERE reference_id = :reference_id",
                       {"reference_id": reference_id})
        reference_authors = cursor.fetchall()
        if reference_authors is None:
            return []
        return [reference_author["name"] for reference_author in reference_authors]

    def post(self, reference: object):
        cursor = self.connection.cursor()
        for author_name in reference.authors:
            author_id = self.author_repository.get(author_name)
            if author_id is None:
                author_id = self.author_repository.post(author_name)

            cursor.execute(
                """
                    INSERT INTO
                        reference_author (reference_id, author_id) 
                        VALUES (:reference_id, :author_id)
                    """,
                {"reference_id": reference.reference_id,
                 "author_id": author_id}
            )

        self.connection.commit()
