class ReferenceRepository:
    def __init__(self, connection):
        self.__connection = connection

    def id_exists(self, reference_id):
        return self.__connection.execute(
            """
            SELECT
                *
            FROM
                reference
            WHERE
                reference_id = ?
            """,
            (reference_id,)
        ).fetchone()

    def get_type(self, reference_id):
        return self.__connection.execute(
            """
            SELECT
                t.type_name
            FROM
                reference r LEFT JOIN type t ON r.type_id = t.type_id
            WHERE r.reference_id = ?
            """,
            (reference_id,)
        ).fetchone()

    def get_field(self, field_name: str):
        return self.__connection.execute(
            """
            SELECT
                field_id
            FROM
                field
            WHERE field_name = ?
            """,
            (field_name,)
        ).fetchone()

    def get_fields(self, type_name):
        return self.__connection.execute(
            """
            SELECT
                f.field_name
            FROM
                type_field tf LEFT JOIN field f ON tf.field_id = f.field_id
            WHERE tf.type_id = (
                SELECT
                    type_id
                FROM
                    type
                WHERE type_name = ?
            )
            """,
            (type_name,)
        ).fetchall()

    def __included_in_fields(self, type_name: str, field: str):
        fields = self.get_fields(type_name)
        if fields:
            return field in [field["field_name"] for field in fields]
        return False

    def get(self, reference_id):
        return self.__connection.execute(
            """
            SELECT
                f.field_name, v.value
            FROM
                value v LEFT JOIN field f ON v.field_id = f.field_id
            WHERE v.reference_id = ?
            """,
            (reference_id,)
        ).fetchall()

    def get_all(self):
        return self.__connection.execute(
            """
            SELECT
                reference_id
            FROM
                reference
            """
        ).fetchall()

    def get_all_by_type(self, type_name):
        return self.__connection.execute(
            """
            SELECT
                reference_id
            FROM
                reference
            WHERE type_id = (
                SELECT
                    type_id
                FROM
                    type
                WHERE type_name = ?
            )
            """,
            (type_name,)
        ).fetchall()["reference_id"]

    def get_by_field_value(self, field_name, value):
        return self.__connection.execute(
            """
            SELECT
                r.reference_id
            FROM
                reference r LEFT JOIN value v ON r.reference_id = v.reference_id
            WHERE v.field_id = (
                SELECT
                    field_id
                FROM
                    field
                WHERE field_name = ?
            ) AND v.value = ?
            """,
            (field_name, value)
        ).fetchall()["reference_id"]

    def get_by_value(self, value):
        return self.__connection.execute(
            """
            SELECT
                r.reference_id
            FROM
                reference r LEFT JOIN value v ON r.reference_id = v.reference_id
            WHERE v.value = ?
            """,
            (value,)
        ).fetchall()["reference_id"]

    def __get_type_id(self, type_name):
        return self.__connection.execute(
            """
            SELECT
                type_id
            FROM
                type
            WHERE type_name = ?
            """,
            (type_name,)
        ).fetchone()

    def __post_reference(self, reference_id, type_name):
        type_id = self.__get_type_id(type_name)
        if not type_id:
            raise Exception(f"Type {type_name} does not exist")
        type_id = type_id["type_id"]
        self.__connection.execute(
            """
            INSERT INTO
                reference (reference_id, type_id)
                VALUES (?, ?)
            """,
            (reference_id, type_id)
        )

    def __post_value(self, reference_id, field_id, value):
        self.__connection.execute(
            """
            INSERT INTO
                value (reference_id, field_id, value)
                VALUES (?, ?, ?)
            """,
            (reference_id, field_id, value)
        )

    def post(self, reference_id: str, type_name: str, values: dict) -> None:
        self.__post_reference(reference_id, type_name)
        for field_name, value in values.items():
            if not self.__included_in_fields(type_name, field_name):
                continue
            field_id = self.get_field(field_name)["field_id"]
            if isinstance(value, list):
                for v in value:
                    self.__post_value(reference_id, field_id, v)
            else:
                self.__post_value(reference_id, field_id, value)
        self.__connection.commit()

    def __put_value(self, reference_id, field_id, value):
        # insert values to value table
        self.__connection.execute(
            """
            INSERT INTO
                value (reference_id, field_id, value)
                VALUES (?, ?, ?)
            """,
            (reference_id, field_id, value)
        )

    def put(self, reference_id: str, field: str, value: str) -> None:
        type_name = self.get_type(reference_id)
        if not type_name:
            return
        if not self.__included_in_fields(type_name["type_name"], field):
            return
        field_id = self.get_field(field)["field_id"]
        self.__put_value(reference_id, field_id, value)
        self.__connection.commit()

    def delete(self, reference_id):
        self.__connection.execute(
            """
            DELETE FROM
                reference
            WHERE
                reference_id = ?
            """,
            (reference_id,)
        )
        self.__connection.execute(
            """
            DELETE FROM
                value
            WHERE
                reference_id = ?
            """,
            (reference_id,)
        )

    def delete_field_values(self, reference_id, field_id):
        self.__connection.execute(
            """
            DELETE FROM
                value
            WHERE
                reference_id = ? AND field_id = ?
            """,
            (reference_id, field_id)
        )

    def delete_all(self):
        self.__connection.execute(
            """
            DELETE FROM
                reference
            """
        )
        self.__connection.execute(
            """
            DELETE FROM
                value
            """
        )
