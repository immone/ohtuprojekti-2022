class ReferenceRepository:
    def __init__(self, connection) -> None:
        self.__connection = connection

    def id_exists(self, reference_id: str) -> bool:
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

    def get(self, reference_id: str):
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
        return cursor.fetchone()

    def get_all(self) -> list:
        cursor = self.__connection.cursor()
        cursor.execute(
            """
            SELECT 
                *
            FROM
                reference
            """
        )
        return cursor.fetchall()

    def post(self, reference) -> None:
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

    def put(self, reference) -> None:
        cursor = self.__connection.cursor()
        cursor.execute(
            """
            UPDATE
                reference
            SET
                title = :title,
                year = :year,
                publisher = :publisher
            WHERE
                reference_id = :reference_id
            """,
            reference.to_dict()
        )
        self.__connection.commit()

    def delete(self, reference_id: str) -> None:
        cursor = self.__connection.cursor()
        cursor.execute("DELETE FROM reference WHERE reference_id = :reference_id",
                       {"reference_id": reference_id})
        self.__connection.commit()

    def delete_all(self) -> None:
        cursor = self.__connection.cursor()
        cursor.execute("DELETE FROM reference")
        self.__connection.commit()
