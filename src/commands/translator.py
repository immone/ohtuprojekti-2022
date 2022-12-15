import sys



class Translator:

    def __init__(self, service, io, searcher=None):
        self.service = service 
        self.command_io = io
        
        if searcher is not None:
            self.searcher = searcher

    def run(self):

        user_term = self.__query_search_term()      
        if user_term == "":
            try:
                reference_list = self.service.get_all()
            except:
                sys.exit("\n A database error occurred. Failed to load references.")

            self.__print_refs(reference_list)

        if user_term[:2] == "t-":
            tag = user_term[2:]
            tagged_refs = self.service.get_by_tag(tag)
            self.command_io.write("Showing " + str(len(tagged_refs)) + " matches for tag: " + tag)
            self.__print_refs(tagged_refs)
        
        else:
            found_refs = self.searcher.search(user_term.split())
            #self.command_io.write(user_term.split())
            self.__print_refs(found_refs)

    def __print_refs(self, references):

        for ref in references:
            self.__print_ref(ref)

    def __print_ref(self, ref):


        self.command_io.write("@"+ ref["type"] + "{" + ref["reference_id"] + ",")

        for key in ref.keys():
            if key in ["tag", "reference_id", "type"]:
                continue
            if type(ref[key]) is list:
                self.command_io.write("  " + f"{key:12}" + "    = {" + str(ref[key])[1:-1].replace("'","").replace(",",";") + "}, ")
            else:
                self.command_io.write("  " + f"{key:12}" + "    = {" + ref[key] + "}, " )

        self.command_io.write("}")
    

    def __query_search_term(self):
        while True:
            search_term = self.command_io.read("Give search terms or t-\'tag\' for what " + 
                                               "you want to translate or <empty> to translate all references: ")
            if search_term == "" or search_term:
                break
        return search_term
