class TagRepository:
    def __init__(self, connection):
        self.connection = connection

    def get(self, tag_name: str) -> list:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT
                *
            FROM
                tag
            WHERE
                name = :name
            """,
            {"name": tag_name}
        )
        tag = cursor.fetchone()
        return tag["tag_id"] if tag else None

    def post(self, tag: str) -> int:
        cursor = self.connection.cursor()
        tag_id = self.get(tag)
        if tag_id:
            return tag_id
        cursor.execute(
            """
            INSERT INTO
                tag (name)
                VALUES (:name)
            """,
            {"name": tag}
        )
        self.connection.commit()
        return cursor.lastrowid

    def delete(self, tag_id: int) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            DELETE FROM
                tag
            WHERE
                tag_id = :tag_id
            """,
            {"tag_id": tag_id}
        )
        self.connection.commit()

    def _cleanup(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            DELETE FROM
                tag
            WHERE
                tag_id NOT IN (
                    SELECT
                        tag_id
                    FROM
                        reference_tag
                )
            """
        )
        self.connection.commit()
