import sys


class Translator:

    def __init__(self, service, io):
        self.service = service 
        self.command_io = io

    def run(self):
        self.command_io.write("Trying to print all references...")
        try:
            reference_list = self.service.get_all()
        except:
            sys.exit("\n A database error occurred. Failed to load references.")
        self.__print_all(reference_list)

    def __print_all(self, references):

        for ref in references:
            self.__print_ref(ref)

    def __print_ref(self, ref):
        authors = ""
        for i in range(0, len(ref.authors)):
            if i == len(ref.authors)-1:
                authors += (" " + ref.authors[i])
            elif i == 0:
                authors += (ref.authors[i] + ",")
            else:
                authors += (" " + ref.authors[i] + ",")
                
        self.command_io.write("@book{" + ref.reference_id + ",")
        self.command_io.write("  author    = {" + authors + "}, ")
        self.command_io.write("  title     = {" + ref.title + "},")
        self.command_io.write("  year      = {" + str(ref.year) + "},")
        self.command_io.write("  publisher = {" + ref.publisher + "},")
        self.command_io.write("}")
    
    def __print_article(self, ref):
        pass

    def __query_saved_reference_id(self):
        while True:
            reference_id = self.command_io.read(
                "<A> to print all references: ", "You need to input <A>")

            # if self.service.id_exists(reference_id):
            #    break
            if reference_id == "A":
                break
            # else:
            #    self.command_io.write("ID not in the database")

        return reference_id
