from Levenshtein import distance


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
            dist = 0
            
            fields = [
                ref.reference_id,
                ref.title,
                str(ref.year),
                ref.publisher
            ] + ref.authors

            for term in terms:
                term = term.lower()
                cutoff = round(len(term) / 3)
                for field in fields:
                    for s in field.split():
                        d = distance(term, s.lower(), score_cutoff=cutoff)
                        if d <= cutoff:
                            matches += 1
                            dist += d
            
            if matches > 0:
                results.append({"ref": ref, "matches": matches, "dist": dist})

        results = sorted(results, key=lambda result: (result["matches"], -result["dist"]), reverse=True)
        return list(map(lambda result: result["ref"], results))