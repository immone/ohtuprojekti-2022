import sys


class Translator:

    def __init__(self, service, io):
        self.service = service 
        self.command_io = io

    def run(self):

        user_term = self.__query_search_term()      
        if user_term == "":
            try:
                reference_list = self.service.get_all()
            except:
                sys.exit("\n A database error occurred. Failed to load references.")

            self.__print_all(reference_list)

        if user_term[:2]

    def __print_all(self, references):

        for ref in references:
            self.__print_ref(ref)

    def __print_ref(self, ref):

        self.command_io.write(ref.keys())

        self.command_io.write("@book{" + ref["reference_id"] + ",")

        for key in ref.keys():
            if key in ["tag", "reference_id", "type"]:
                continue
            if type(ref[key]) is list:
                self.command_io.write("  " + key + "    = {" + str(ref[key])[1:-1].replace("'","") + "}, ")
            else:
                self.command_io.write("  " + key + "    = {" + ref[key] + "}, " )

        self.command_io.write("}")
    

    def __query_search_term(self):
        while True:
            search_term = self.command_io.read("Give a search term or t-\'tag\' for what" + 
                                               "you want to translate or <empty> to translate all references: ")
            if search_term == "" or search_term:
                break
        return search_term
