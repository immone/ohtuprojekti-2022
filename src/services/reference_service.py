from database_connection import get_database_connection
from repositories import ReferenceRepository


class ReferenceService:
    def __init__(self):
        self.__connection = get_database_connection()
        self.__reference_repository = ReferenceRepository(self.__connection)

    def id_exists(self, reference_id: int) -> bool:
        exists = self.__reference_repository.id_exists(reference_id)
        return exists is not None

    def get_type(self, reference_id: int) -> str:
        type_name = self.__reference_repository.get_type(reference_id)
        if type_name:
            return type_name["type_name"]
        return None

    def get_field(self, field_name: str) -> int:
        field = self.__reference_repository.get_field(field_name)
        if field:
            return field["field_id"]
        return None

    def get_fields(self, type_name: str) -> list:
        fields = list(self.__reference_repository.get_fields(type_name))
        if fields:
            return sorted([field["field_name"] for field in fields])
        return []

    def get(self, reference_id: int) -> dict:
        reference = self.__reference_repository.get(reference_id)
        author = []
        tag = []
        result = {}
        if reference:
            for i in reference:
                if i["field_name"] == "author":
                    author.append(i["value"])
                elif i["field_name"] == "tag":
                    tag.append(i["value"])
                else:
                    result[i["field_name"]] = i["value"]

            result["author"] = author
            result["tag"] = tag
            result["reference_id"] = reference_id
            result["type"] = self.get_type(reference_id)
        return result

    def get_all(self) -> list:
        all_ref_ids = self.__reference_repository.get_all()
        if all_ref_ids:
            return [self.get(ref_id["reference_id"]) for ref_id in all_ref_ids]
        return []

    def get_by_tag(self, tag) -> list:
        all_refs = self.get_all()
        tagged_refs = []
        for ref in all_refs:
            if tag in ref["tag"]:
                tagged_refs.append(ref)

        return tagged_refs

    def post(self, reference: dict) -> None:
        id = reference["reference_id"]
        type = reference["type"]
        del reference["reference_id"]
        del reference["type"]
        self.__reference_repository.post(id, type, reference)

    def put(self, reference_id: str, field: str, value: str) -> None:
        self.__reference_repository.put(reference_id, field, value)

    def delete(self, reference_id: int) -> None:
        self.__reference_repository.delete(reference_id)

    def delete_all(self) -> None:
        self.__reference_repository.delete_all()
