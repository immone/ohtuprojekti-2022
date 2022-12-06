import sys
import datetime
import unicodedata
import re
from entities.reference import Reference


class Add:
    def __init__(self, service, io):
        self.service = service
        self.io = io

    def run(self):
        self.io.write("Adding new book reference...")

        title = self.__query_title()
        authors = self.__query_authors()
        year = self.__query_year()
        publisher = self.io.read(" ... enter publisher: ",
                                 " ...... please provide a publisher")
        tags = self.__query_tags()

        reference_id = self.__generate_ref_id(authors, year)

        try:
            self.service.post(Reference(
                reference_id=reference_id,
                authors=authors,
                title=title,
                year=year,
                publisher=publisher,
                tags=tags
            ))
            self.io.write(f"\nReference added with id '{reference_id}'.")
        except:
            sys.exit("\nA database error occurred. Failed to add reference.")

    def __query_title(self):
        while True:
            title = self.io.read(" ... enter title: ",
                                 " ...... please provide a title")

            if len(title) <= 300:
                return title

            self.io.write(
                " ...... please provide a valid title (max length: 300 characters)")

    def __query_authors(self):
        name_regex = "^[a-zA-Z][a-zA-Z'.-]*(?: [a-zA-Z'.-]+)*[a-zA-Z]$"

        while True:
            authors = self.io.read(" ... enter authors (delimited by semicolons): ",
                                    " ...... please provide at least one author")

            authors = [a.strip() for a in authors.split(";")]
            authors = list(filter(lambda a: len(a) > 0, authors))

            if len(authors) > 0 and all(re.search(name_regex, a) for a in authors):
                break

            self.io.write(" ...... please provide valid author(s)")

        for i in range(0, len(authors)):
            # if author is given in format lastname, firstname, parse that
            if ", " in authors[i]:
                names = authors[i].split(", ")
                authors[i] = f"{names[1]} {names[0]}"

        return authors

    def __query_year(self):
        while True:
            year = self.io.read(" ... enter year of publication: ",
                                " ...... please provide a year")

            if year.isnumeric() and int(year) > 0 and int(year) <= datetime.date.today().year:
                return int(year)

            self.io.write(" ...... please provide a valid year")

    def __generate_ref_id(self, authors, year):
        iteration = 0
        while True:
            author_lastname = authors[0].split()[-1]
            ref_id = author_lastname[:10] + \
                str(year) + ("_" + str(iteration) if iteration > 0 else "")
            ref_id = self.__normalize_str(ref_id)

            if not self.service.id_exists(ref_id):
                return ref_id

            iteration += 1

    # from https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
    def __normalize_str(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')

    def __query_tags(self):
        tags = self.io.read_opt(" ... enter reference tags (delimited by semicolons) [optional]: ")
        return [t.strip() for t in tags.split(";")]
