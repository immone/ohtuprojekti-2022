from services.reference_service import ReferenceService
import sys

class List():
    def __init__(self, repository, io):
        self.repository = repository
        self.service = ReferenceService()
        self.io = io

    def run(self):
        all_references = self.service.get_all()
        if len(all_references) == 0:
            self.io.write("There are no references to be listed.")
        else:
            self.io.write(f"Found a total number of {len(all_references)} references.\n")
            self.io.write("Printing all references in the database..\n")
            for ref in all_references:
                for val in ref:
                    self.io.write(self.__match_key_to_io_write(val, ref))
                self.io.write("")

    def __match_key_to_io_write(self, key, ref):
        match key:
            case "type":
                return f"Reference type: {ref['type']}"
            case "title":
                return f"Title: {ref['title']}"
            case "author":
                return f"Author(s): {', '.join(ref['author'])}"
            case "booktitle":
                return f"Book title: {ref['booktitle']}"
            case "series":
                return f"Series: {ref['series']}"
            case "pages":
                return f"Pages: {ref['pages']}"
            case "year":
                return f"Published in: {ref['year']}"
            case "publisher":
                return f"Published by: {ref['publisher']}"
            case"howpublished":
                return f"How published (notes): {ref['howpublished']}"
            case "address":
                return f"Address: {ref['address']}"
            case "reference_id":
                return f"Reference ID: {ref['reference_id']}"
            case "tag":
                return f"Tags: {', '.join(ref['tag'])}"
            case _:
                pass