class ReferenceAuthorRepository:
    def __init__(self, connection, author_repository) -> None:
        self.__connection = connection
        self.__author_repository = author_repository

    def get(self, reference_id: object) -> list:
        cursor = self.__connection.cursor()
        cursor.execute(
            """
            SELECT
                *
            FROM
                reference_author ra LEFT JOIN
                author a ON ra.author_id = a.author_id
            WHERE
                reference_id = :reference_id
            """,
            {"reference_id": reference_id}
        )
        reference_authors = cursor.fetchall()
        return [reference_author["name"] for reference_author in reference_authors] if reference_authors else []

    def post(self, reference: object) -> None:
        cursor = self.__connection.cursor()
        for author_name in reference.authors:
            author_id = self.__author_repository.post(author_name)
            cursor.execute(
                """
                INSERT INTO
                    reference_author (reference_id, author_id)
                    VALUES (:reference_id, :author_id)
                """,
                {"reference_id": reference.reference_id,
                 "author_id": author_id}
            )
        self.__connection.commit()

    def put(self, reference: object) -> None:
        self.delete(reference.reference_id)
        self.post(reference)

    def delete(self, reference_id: object) -> None:
        cursor = self.__connection.cursor()
        cursor.execute(
            """
            DELETE FROM
                reference_author
            WHERE
                reference_id = :reference_id
            """,
            {"reference_id": reference_id}
        )
        self.__connection.commit()
