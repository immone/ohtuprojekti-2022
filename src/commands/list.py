from services.reference_service import ReferenceService

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
                self.io.write(f"Title: {ref.title}' \n"
                              f"Author(s): {', '.join(ref.authors)} \n"
                              f"Published in: {ref.year} \n"
                              f"Published by: {ref.publisher} \n"
                              f"Tag: {ref.tags}\n")