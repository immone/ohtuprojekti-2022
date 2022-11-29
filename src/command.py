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

    ## TODO: does it make sense to delete based on the reference id?
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


    ## TODO: which information is printed? in which format?
    def list(self):
        print("Printing all references in the database..")

        all_references = self.repository.get_all()
        if len(all_references) == 0:
            print("There are no references to be printed.")
        else:
            for ref in all_references:
                print("Author(s): ", ref.__authors)
                print("Title: ", ref.__title)
                print("Published in: ", ref.__year)
                print("Published by: ", ref.__publisher, "\n")

    ## TODO: does it make sense to delete based on the reference id?
    def edit(self):
        print("Attempting to edit a reference..")

        id_to_edit = self.__check_id_exists()

        ref_object = self.__get_reference_object(id_to_edit)

        field = self.__match_edit_field()
        if field == "author" or "authors":
            ref_object.__authors = field
            print("Author field changed successfully")
        elif field == "title":
            ref_object.__title = field
            print("Title field changed successfully")
        elif field == "year":
            ref_object.__year = field
            print("Year field changed successfully")
        elif field == "publisher":
            ref_object.__year = field
            print("Publisher field changed successfully")
        else:
            print("No such field exists")

    def __match_edit_field(self):
        field = self.__query_non_empty("Which field of the given reference "
                                       "would you like to edit? (author, title, year, publisher)?",
                                       "Please provide a field").strip().lower()

        ## feel free to refactor to Python 3.10 match case or something alike
        while field not in ["author", "title", "year", "publisher"]:
            print("Please give one of the listed fields")
            field = self.__query_non_empty("Which field of the given reference "
                                           "would you like to edit? (author, title, year, publisher)?",
                                           "Please provide a field").strip().lower()

        return field


    # returns None if doesn't exist in db; call __check_id_exists prior
    def __get_reference_object(self, id):
        all_refs = self.repository.get_all()
        for ref in all_refs:
            if ref.__reference_id == id: return ref
        return None





