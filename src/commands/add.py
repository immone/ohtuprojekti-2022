import sys
import datetime
import unicodedata
from entities.reference import Reference


class Add:
    def __init__(self, repository, io):
        self.repository = repository
        self.io = io

    def run(self):
        self.io.write("Adding new reference...")

        title = self.__query_title()
        authors = self.__query_authors()
        year = self.__query_year()
        publisher = self.io.read("Enter publisher: ",
                                 "Please provide a publisher")

        reference_id = self.__generate_ref_id(authors, year)

        try:
            self.repository.post(Reference(
                reference_id=reference_id,
                authors=authors,
                title=title,
                year=year,
                publisher=publisher
            ))
            self.io.write(f"\nReference added with id '{reference_id}'.")
        except:
            sys.exit("\nA database error occurred. Failed to add reference.")

    def __query_reference_id(self):
        while True:
            reference_id = self.io.read("Enter reference ID: ",
                                        "Please provide a reference ID")

            if not self.repository.id_exists(reference_id):
                break
            else:
                self.io.write("That ID is already taken")

        return reference_id

    def __query_title(self):
        while True:
            title = self.io.read("Enter reference title: ",
                                 "Please provide a title")

            if len(title) <= 300:
                break
            else:
                self.io.write(
                    "Please provide a valid title (max length: 300 characters)")

        return title

    def __query_authors(self):
        while True:
            num_authors = self.io.read("Enter the number of authors: ",
                                       "Please provide a number")

            if num_authors.isnumeric() and int(num_authors) > 0:
                break
            else:
                self.io.write("Please provide a valid number")

        authors = []
        for i in range(0, int(num_authors)):
            author = self.io.read(f"Enter author {i + 1}: ",
                                  "Please provide an author")

            # if author is given in format lastname, firstname, parse that
            if ", " in author:
                names = author.split(", ")
                author = f"{names[1]} {names[0]}"

            authors.append(author)

        return authors

    def __query_year(self):
        while True:
            year = self.io.read("Enter reference year: ",
                                "Please provide a year")
            if year.isnumeric() and int(year) > 0 and int(year) <= datetime.date.today().year:
                break
            else:
                self.io.write("Please provide a valid year")

        return int(year)

    def __generate_ref_id(self, authors, year):
        iteration = 0
        while True:
            author_lastname = authors[0].split()[1]
            ref_id = author_lastname[:10] + str(year) + ("_" + str(iteration) if iteration > 0 else "")
            ref_id = self.__normalize_str(ref_id)

            if not self.repository.id_exists(ref_id):
                return ref_id

            iteration += 1

    # from https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
    def __normalize_str(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                    if unicodedata.category(c) != 'Mn')
