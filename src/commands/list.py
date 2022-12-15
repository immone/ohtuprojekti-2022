from services.reference_service import ReferenceService
import sys

class List():
    def __init__(self, repository, io):
        self.repository = repository
        self.service = ReferenceService()
        self.io = io

    def run(self):
        tag_filter = self.io.read("Would you like to filter the listing according to some tags? (y/n) ",
                                  "Please indicate your answer")
        while tag_filter not in ["y", "n", "yes", "no"]:
            print(tag_filter)
            self.io.read("Would you like to filter the listing according to some tags? (y/n) ",
                         "Please indicate your answer")
        if tag_filter in ["n", "no"]:
            self.__no_tag()
        else:
            self.__tag()

    def __no_tag(self):
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

    def __tag(self):
        tags = self.io.read("Please enter the tags you would like search under (delimited by semicolons)",
                            "Please enter a nonempty tag")
        tags_parsed = [t.strip() for t in tags.split(";")]

        operation = self.io.read("Would you like the search to include matches that contain all or any of the given tags? (all/any) ",
                            "Please indicate your answer")

        # union or intersection of search words
        while operation not in ["all", "any"]:
            self.io.read(
                "Would you like the search to include matches that contain all or any of the given tags? (all/any)",
                "Please indicate your answer")
            
        if operation == "any":
            tag_refs = []
            for tag in tags_parsed:
                tag_refs = tag_refs + self.service.get_by_tag(tag)
        else:
            tag_refs = []
            for tag in tags_parsed:
                candidate_refs = self.service.get_by_tag(tag)
                for candidate in candidate_refs:
                    print(candidate["tag"], tags_parsed)
                    if all(tag in candidate["tag"] for tag in tags_parsed) and candidate not in tag_refs:
                        tag_refs.append(candidate)

        if len(tag_refs) == 0:
            self.io.write("There are no references to be listed.")
        else:
            self.io.write(f"Found a total number of {len(tag_refs)} references under the given tag(s).\n")
            self.io.write("Printing all found references under the given tag(s)..\n")
            for ref in tag_refs:
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