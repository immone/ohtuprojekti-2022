import sys
from entities.reference import Reference


class Delete:
    def __init__(self, repository, io):
        self.repository = repository
        self.io = io

    def run(self):
        self.io.write("Attempting to remove a reference..")

        id_to_remove = self.__check_id_exists()

        try:
            self.repository.delete(id_to_remove)
            self.io.write("\nReference deleted.")
        except:
            sys.exit(
                "\nAn error occurred while trying to delete reference. Exiting..")

    # can abstract somewhere
    def __check_id_exists(self):
        reference_id = self.io.read("Enter reference ID: ",
                                    "Please provide a reference ID")
        # loop till given id exists in db
        while self.repository.id_exists(reference_id) == False:
            self.io.write("No such reference ID exists")
            reference_id = self.io.read("Enter reference ID: ",
                                        "Please provide a reference ID")
        return reference_id
