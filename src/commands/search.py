class Search:
    def __init__(self, service, io):
        self.__service = service
        self.__io = io

    def run(self):
        terms = self.__io.read("Enter search terms: ", "Please provide search terms")
        terms = terms.split()

        refs = self.__search(terms)
        n_refs = len(refs)

        if n_refs > 0:
            self.__io.write(f"{n_refs} reference(s) matched one or more of the search terms:")
            for ref in refs:
                self.__io.write(f"\t{ref} (id: {ref.reference_id})")
        else:
            self.__io.write("0 references matched the search terms")

    def __search(self, terms):
        all_refs = self.__service.get_all()
        results = []
        for ref in all_refs:
            matches = 0
            print(f"IN SEARCH REF_STR {str(ref)}")
            for term in terms:
                ref_str = f"{str(ref)} {ref.reference_id}"
                print(f"    TERM {term}")
                matches += ref_str.lower().count(term.lower())
                print(f"    matches: {matches}")
        
            if matches > 0:
                results.append({"ref": ref, "matches": matches})

        results = sorted(results, key=lambda result: result["matches"], reverse=True)
        return list(map(lambda result: result["ref"], results))