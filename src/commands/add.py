import sys
import datetime
from entities.reference import Reference


class Add:
    def __init__(self, repository, io):
        self.repository = repository
        self.io = io

    def run(self):
        self.io.write("Adding new reference...")

        reference_id = self.io.read_non_empty("Enter reference ID: ",
            "Please provide a reference ID")

        while self.repository.id_exists(reference_id):
            self.io.write("That ID is already taken")
            reference_id = self.io.read_non_empty("Enter reference ID: ",
                "Please provide a reference ID")

        title = self.__query_title()
        authors = self.__query_authors()
        year = self.__query_year()
        publisher = self.io.read_non_empty("Enter publisher: ",
            "Please provide a publisher")

        try:
            self.repository.post(Reference(
                reference_id=reference_id,
                authors=authors,
                title=title,
                year=year,
                publisher=publisher
            ))
            self.io.write("\nReference added.")
        except:
            sys.exit("\nA database error occurred. Failed to add reference.")

    def __query_title(self):
        title = self.io.read_non_empty("Enter reference title: ",
            "Please provide a title")
        while len(title) > 300:
            self.io.write("Please provide a valid title (max length: 300 characters): ")
            title = self.io.read_non_empty("Enter reference title: ",
                "Please provide a title")

    def __query_authors(self):
        num_authors = self.io.read("Enter the number of authors: ")
        while not num_authors.isnumeric() or int(num_authors) == 0:
            self.io.write("Please provide a valid number")
            num_authors = self.io.read("Enter the number of authors: ")

        authors = []
        for i in range(0, int(num_authors)):
            author = self.io.read_non_empty(f"Enter author {i + 1}: ",
                "Please provide an author")

            # if author is given in format lastname, firstname, parse that
            if ", " in author:
                names = author.split(", ")
                author = f"{names[1]} {names[0]}"

            authors.append(author)

        return authors

    def __query_year(self):
        year = self.io.read("Enter reference year: ")
        while not year.isnumeric() or int(year) <= 0 or int(year) > datetime.date.today().year:
            self.io.write("Please provide a valid year")
            year = self.io.read("Enter reference year: ")

        return int(year)