class Translator:
    
    def __init__(self, repository, io):
        self.repository = repository
        self.io = io


    def run(self):
        self.io.write("Trying to print references")
        reference_list = self.repository.get_all()
        
        for ref in reference_list:

            authors = ""
            for i in range(0, len(ref.authors)):
                if i == len(ref.authors)-1:
                    authors += (" "+ ref.authors[i])
                elif i == 0:
                    authors += (ref.authors[i] +",")
                else: 
                    authors += (" " + ref.authors[i] + ",")

            self.io.write("@book{"+ ref.reference_id +",")
            self.io.write("  author    = {"+ authors +"}, ")
            self.io.write("  title     = {"+ ref.title +"},")
            self.io.write("  year      = {"+ str(ref.year) +"},")
            self.io.write("  publisher = {"+ ref.publisher +"},")
            self.io.write("}")
