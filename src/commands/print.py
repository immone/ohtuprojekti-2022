import sys
from entities.reference import Reference

class Print():
    def __init__(self, repository):
        self.repository = repository

    def list(self):
        print("Printing all references in the database..")

        all_references = self.repository.get_all()
        if len(all_references) == 0:
            print("There are no references to be printed.")
        else:
            for ref in all_references:
                print("Author(s): ", ref.__authors)
                print("Title: ", ref.__title)
                print("Published in: ", ref.__year)
                print("Published by: ", ref.__publisher, "\n")
