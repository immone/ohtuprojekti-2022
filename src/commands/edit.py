import sys
import re
import datetime
from entities.reference import Reference

class Edit():
    def __init__(self, repository, io):
        self.repository = repository
        self.io = io

    def run(self):
        self.io.write("Attempting to edit a reference..")

        id_to_edit = self.__check_id_exists()

        title = self.__query_title()
        authors = self.__query_authors()
        year = self.__query_year()
        publisher = self.io.read(" ... enter publisher: ",
                                 " ...... please provide a publisher")
        tags = self.__query_tags()

        new_ref_object = Reference(
                reference_id=id_to_edit,
                authors=authors,
                title=title,
                year=year,
                publisher=publisher,
                tags=tags
            )
        try:
            self.repository.put(new_ref_object)
            self.io.write("\nReference edited.")
        except:
            sys.exit(
                "\nAn error occurred while trying to edit reference. Exiting..")


    # can abstract somewhere
    def __check_id_exists(self):
        reference_id = self.io.read("Enter reference ID: ",
                                    "Please provide a reference ID")
        while not self.repository.id_exists(reference_id):
            self.io.write("No such reference ID exists")
            reference_id = self.io.read("Enter reference ID: ",
                                        "Please provide a reference ID")
        return reference_id

    def __query_title(self):
        while True:
            title = self.io.read(" ... enter new title: ",
                                 " ...... please provide a title")

            if len(title) <= 300:
                return title

            self.io.write(
                " ...... please provide a valid title (max length: 300 characters)")

    def __query_authors(self):
        name_regex = "^[a-zA-Z][a-zA-Z'.-]*(?: [a-zA-Z'.-]+)*[a-zA-Z]$"

        while True:
            authors = self.io.read(" ... enter new authors (delimited by semicolons) [format: [FirstName(s)] LastName]: ",
                                   " ...... please provide at least one author")

            authors = [a.strip() for a in authors.split(";")]
            authors = list(filter(lambda a: len(a) > 0, authors))

            if len(authors) > 0 and all(re.search(name_regex, a) for a in authors):
                break

            self.io.write(" ...... please provide valid author(s)")

        return authors

    def __query_year(self):
        while True:
            year = self.io.read(" ... enter new year of publication: ",
                                " ...... please provide a year")

            if year.isnumeric() and int(year) > 0 and int(year) <= datetime.date.today().year:
                return int(year)

            self.io.write(" ...... please provide a valid year")

    def __query_tags(self):
        tags = self.io.read(" ... enter new reference tags (delimited by semicolons) [optional]: ")
        return [t.strip() for t in tags.split(";")]
