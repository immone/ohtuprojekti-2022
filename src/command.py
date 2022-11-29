import sys
from entities.reference import Reference


class Command:
    def __query_non_empty(self, prompt, empty_msg):
        query = input(prompt)
        while len(query) == 0:
            print(empty_msg)
            query = input(prompt)

        return query

    # TODO: does it make sense to delete based on the reference id?
    def delete(self):
        print("Attempting to remove a reference..")

        id_to_remove = self.__check_id_exists()

        try:
            self.repository.delete(id_to_remove)
            print("\nReference deleted.")
        except:
            sys.exit(
                "\nAn error occurred while trying to delete reference. Exiting..")

    def __check_id_exists(self):
        reference_id = self.__query_non_empty("Enter reference ID: ",
                                              "Please provide a reference ID")
        # loop till given id exists in db
        while self.repository.id_exists(reference_id) == False:
            print("No such reference ID exists")
            reference_id = self.__query_non_empty("Enter reference ID: ",
                                                  "Please provide a reference ID")
        return reference_id

    # TODO: which information is printed? in which format?

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

    # TODO: does it make sense to edit based on the reference id?
    def edit(self):
        print("Attempting to edit a reference..")

        id_to_edit = self.__check_id_exists()

        ref_object = self.__get_reference_object(id_to_edit)

        # feel free to refactor to Python 3.10 match case or something alike
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
            if ref.__reference_id == id:
                return ref
        return None
