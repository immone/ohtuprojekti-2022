import sys


class Translator:

    def __init__(self, repository, io):
        self.repository = repository
        self.io = io

    def run(self):
        reference_id = self.__query_saved_reference_id()
        if reference_id == "A":
            self.__print_all()

    def __print_all(self):
        self.io.write("Trying to print all references...")
        try:
            reference_list = self.repository.get_all()
        except:
            sys.exit("\n A database error occurred. Failed to load references.")

        for ref in reference_list:
            authors = ""
            for i in range(0, len(ref.authors)):
                if i == len(ref.authors)-1:
                    authors += (" " + ref.authors[i])
                elif i == 0:
                    authors += (ref.authors[i] + ",")
                else:
                    authors += (" " + ref.authors[i] + ",")
            self.__print_ref(ref, authors)

    def __print_ref(self, ref, authors):
        self.io.write("@book{" + ref.reference_id + ",")
        self.io.write("  author    = {" + authors + "}, ")
        self.io.write("  title     = {" + ref.title + "},")
        self.io.write("  year      = {" + str(ref.year) + "},")
        self.io.write("  publisher = {" + ref.publisher + "},")
        self.io.write("}")

    def __query_saved_reference_id(self):
        while True:
            reference_id = self.io.read(
                "<A> to print all references: ", "You need to input <A>")

            # if self.repository.id_exists(reference_id):
            #    break
            if reference_id == "A":
                break
            # else:
            #    self.io.write("ID not in the database")

        return reference_id
