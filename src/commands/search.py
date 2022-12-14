from Levenshtein import distance


def ref_to_str(ref):
    authors = ', '.join(ref["author"]) if len(ref["author"]) > 0 else "<no authors>"
    title = ref["title"] if "title" in ref.keys() else "<no title>"
    booktitle = f"In {ref['booktitle']}" if "booktitle" in ref.keys() else ""
    series = f"{ref['series']}" if "series" in ref.keys() else ""
    pages = f"pages {ref['pages']}" if "pages" in ref.keys() else ""
    address = f"{ref['address']}" if "address" in ref.keys() else ""
    howpublished = ref["howpublished"] if "howpublished" in ref.keys() else "<no publisher info>"
    publisher = ref["publisher"] if "publisher" in ref.keys() else howpublished
    year = ref["year"] if "year" in ref.keys() else "<no publication year>"

    mid_section = list(filter(lambda f: len(f) > 0, [booktitle, series, pages, address, publisher]))
    if len(mid_section) > 0:
        mid_section.append("")
    
    return f"{authors}. {title}. {', '.join(mid_section)}{year}."


class Search:
    def __init__(self, service, io):
        self.__service = service
        self.__io = io

    def run(self):

        terms = self.__io.read("Enter search terms: ", " ... please provide at least one search term")
        terms = terms.split()
        refs = self.search(terms)
        n_refs = len(refs)

        if n_refs > 0:
            self.__io.write(f"{n_refs} reference(s) matched one or more of the search terms:")
            for ref in refs:
                ref_id = ref["reference_id"]
                self.__io.write(f"\t{ref_to_str(ref)} (id: {ref_id})")
        else:
            self.__io.write("0 references matched the search terms")

    def search(self, terms):
        all_refs = self.__service.get_all()
        results = []
        for ref in all_refs:
            matches = 0
            dist = 0
            
            fields = []
            for field in ref.values():
                if type(field) == str:
                    fields.append(field)
                elif type(field) == list:
                    fields.extend(field)
                elif type(field) == int:
                    fields.extend(str(field))

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
