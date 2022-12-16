import sys
from services.reference_service import ReferenceService

class Delete:
    def __init__(self, service, io):
        self.service = service
        self.io = io

    def run(self):
        self.io.write("Attempting to remove a reference..")

        id_to_remove = self.__check_id_exists()
        if id_to_remove == None:
            return

        try:
            self.service.delete(id_to_remove)
            self.io.write("\nReference deleted.")
        except:
            sys.exit(
                "\nAn error occurred while trying to delete reference. Exiting..")

    def __check_id_exists(self):
        reference_id = self.io.read("Enter reference ID: ",
                                    "Please provide a reference ID")
        if self.service.id_exists(reference_id) == False:
            self.io.write("No such reference ID exists\n")
            reference_id = None
        return reference_id
