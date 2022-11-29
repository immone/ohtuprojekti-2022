import sys
from entities.reference import Reference


class Command:
    def __init__(self, repository=None):
        self.repository = repository

    def add(self):
        print("Adding new reference...")

        reference_id = self.__query_non_empty("Enter reference ID: ",
            "Please provide a reference ID")

        while not self.__check_id_unique(reference_id):
            print("That ID is already taken")
            reference_id = self.__query_non_empty("Enter reference ID: ",
                "Please provide a reference ID")

        title = self.__query_non_empty("Enter reference title: ",
            "Please provide a reference title")

        authors = self.__query_authors()
        year = self.__query_year()
        publisher = self.__query_non_empty("Enter publisher: ",
            "Please provide a publisher")

        try:
            self.repository.post(Reference(
                reference_id=reference_id,
                authors=authors,
                title=title,
                year=year,
                publisher=publisher
            ))
            print("\nReference added.")
        except:
            sys.exit("\nA database error occurred. Failed to add reference.")

    def __query_non_empty(self, prompt, empty_msg):
        query = input(prompt)
        while len(query) == 0:
            print(empty_msg)
            query = input(prompt)

        return query

    def __check_id_unique(self, ref_id):
        try:
            references = self.repository.get_all()
        except:
            sys.exit("\nA database error occurred.")

        for ref in references:
            if ref.reference_id == ref_id:
                return False

        return True

    def __query_authors(self):
        num_authors = input("Enter the number of authors: ")
        while not num_authors.isnumeric() or int(num_authors) == 0:
            print("Please provide a valid number")
            num_authors = input("Enter the number of authors: ")

        authors = []
        for i in range(0, int(num_authors)):
            author = self.__query_non_empty(f"Enter author {i + 1}: ",
                "Please provide an author")

            # if author is given in format lastname, firstname, parse that
            if ", " in author:
                names = author.split(", ")
                author = f"{names[1]} {names[0]}"

            authors.append(author)

        return authors

    def __query_year(self):
        year = input("Enter reference year: ")
        while not year.isnumeric() or int(year) <= 0:
            print("Please provide a valid year")
            year = input("Enter reference year: ")

        return int(year)

    def delete(self):
        print("Attempting to remove a reference..")

        id_to_remove = self.__check_id_exists()

        try:
            self.repository.delete(id_to_remove)
            print("\nReference deleted.")
        except:
            sys.exit("\nAn error occurred while trying to delete reference. Exiting..")

    def __check_id_exists(self):

        reference_id = self.__query_non_empty("Enter reference ID: ",
                                              "Please provide a reference ID")
        # loop till given id exists in db
        while self.repository.id_exists(reference_id) == False:
            print("No such reference ID exists")
            reference_id = self.__query_non_empty("Enter reference ID: ",
                                                  "Please provide a reference ID")
        return reference_id

