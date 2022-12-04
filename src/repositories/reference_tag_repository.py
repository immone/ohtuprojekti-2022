class ReferenceTagRepository:
    def __init__(self, connection, tag_repository) -> None:
        self.__connection = connection
        self.__tag_repository = tag_repository

    def get(self, reference_id: object) -> list:
        cursor = self.__connection.cursor()
        cursor.execute(
            """
            SELECT
                *
            FROM
                reference_tag rt LEFT JOIN
                tag t ON rt.tag_id = t.tag_id
            WHERE
                reference_id = :reference_id
            """,
            {"reference_id": reference_id}
        )
        reference_tags = cursor.fetchall()
        return [reference_tag["name"] for reference_tag in reference_tags] if reference_tags else []

    def post(self, reference: object) -> None:
        cursor = self.__connection.cursor()
        for tag_name in reference.tags:
            tag_id = self.__tag_repository.post(tag_name)
            cursor.execute(
                """
                INSERT INTO
                    reference_tag (reference_id, tag_id)
                    VALUES (:reference_id, :tag_id)
                """,
                {"reference_id": reference.reference_id,
                 "tag_id": tag_id}
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
                reference_tag
            WHERE
                reference_id = :reference_id
            """,
            {"reference_id": reference_id}
        )
        self.__connection.commit()
        self.__tag_repository._cleanup()

    def delete_all(self) -> None:
        cursor = self.__connection.cursor()
        cursor.execute("DELETE FROM reference_tag")
        self.__tag_repository._cleanup()
