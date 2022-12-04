from repositories import AuthorRepository, ReferenceAuthorRepository, ReferenceRepository
from entities import Reference
from database_connection import get_database_connection


class ReferenceService:
    def __init__(self) -> None:
        self.__connection = get_database_connection()
        self.__reference_repository = ReferenceRepository(self.__connection)
        self.__author_repository = AuthorRepository(self.__connection)
        self.__reference_author_repository = ReferenceAuthorRepository(
            self.__connection, self.__author_repository)

    def id_exists(self, reference_id: int) -> bool:
        return self.__reference_repository.id_exists(reference_id)

    def get(self, reference_id: int) -> Reference:
        reference = self.__reference_repository.get(reference_id)
        authors = self.__reference_author_repository.get(reference_id)
        return Reference(
            reference_id=reference["reference_id"],
            authors=authors,
            title=reference["title"],
            year=reference["year"],
            publisher=reference["publisher"]
        )

    def get_all(self) -> list:
        references = self.__reference_repository.get_all()
        return [self.get(reference["reference_id"]) for reference in references]

    def post(self, reference: Reference) -> None:
        self.__reference_author_repository.post(reference)
        self.__reference_repository.post(reference)

    def put(self, reference: Reference) -> None:
        self.__reference_author_repository.put(reference)
        self.__reference_repository.put(reference)

    def delete(self, reference_id: int) -> None:
        self.__reference_repository.delete(reference_id)
        self.__reference_author_repository.delete(reference_id)

    def delete_all(self) -> None:
        self.__reference_repository.delete_all()
        self.__reference_author_repository.delete_all()
