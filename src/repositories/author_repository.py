from database_connection import get_database_connection


class AuthorRepository:
    def __init__(self):
        self.connection = get_database_connection()

    def get(self, name: str):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM author WHERE name = :name",
                       {"name": name})
        author = cursor.fetchone()
        return author["author_id"] if author is not None else None

    def post(self, author: str):
        cursor = self.connection.cursor()
        cursor.execute(
            """
                INSERT INTO
                    author (name) 
                    VALUES (:name)
                """,
            {"name": author}
        )
        self.connection.commit()
        return cursor.lastrowid

    def delete(self, author_id: int):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM author WHERE author_id = :author_id",
                       {"author_id": author_id})
        self.connection.commit()
