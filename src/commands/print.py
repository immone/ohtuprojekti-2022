from entities.reference import Reference


class Print():
    def __init__(self, repository, io):
        self.repository = repository
        self.io = io

    def run(self):
        self.io.write("Printing all references in the database..")

        all_references = self.repository.get_all()
        if len(all_references) == 0:
            self.io.write("There are no references to be printed.")
        else:
            for ref in all_references:
                self.io.write("Author(s): ", ref.__authors)
                self.io.write("Title: ", ref.__title)
                self.io.write("Published in: ", ref.__year)
                self.io.write("Published by: ", ref.__publisher, "\n")
