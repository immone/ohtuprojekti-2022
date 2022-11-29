class AuthorRepository:
    def __init__(self, connection) -> None:
        self.__connection = connection

    def get(self, name: str) -> int:
        cursor = self.__connection.cursor()
        cursor.execute(
            """
            SELECT 
                * 
            FROM
                author 
            WHERE 
                name = :name
            """,
            {"name": name}
        )
        author = cursor.fetchone()
        return author["author_id"] if author else None

    def post(self, author: str) -> int:
        cursor = self.__connection.cursor()
        author_id = self.get(author)
        if author_id:
            return author_id
        cursor.execute(
            """
            INSERT INTO
                author (name) 
                VALUES (:name)
            """,
            {"name": author}
        )
        self.__connection.commit()
        return cursor.lastrowid

    def delete(self, author_id: int) -> None:
        cursor = self.__connection.cursor()
        cursor.execute(
            """
            DELETE FROM 
                author 
            WHERE 
                author_id = :author_id
            """,
            {"author_id": author_id}
        )
        self.__connection.commit()
