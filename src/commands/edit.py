
class Edit():
    def __init__(self, repository, io):
        self.repository = repository
        self.io = io

    def edit(self):
        print("Attempting to edit a reference..")

        id_to_edit = self.__check_id_exists()

        ref_object = self.__get_reference_object(id_to_edit)

        # feel free to refactor to Python 3.10 match case or something alike
        field = self.__match_edit_field()
        if field == "author" or "authors":
            ref_object.__authors = field
            self.io.write("Author field changed successfully")
        elif field == "title":
            ref_object.__title = field
            self.io.write("Title field changed successfully")
        elif field == "year":
            ref_object.__year = field
            self.io.write("Year field changed successfully")
        elif field == "publisher":
            ref_object.__year = field
            self.io.write("Publisher field changed successfully")
        else:
            self.io.write("No such field exists")

    def __match_edit_field(self):
        field = self.io.read("Which field of the given reference "
                             "would you like to edit? (author, title, year, publisher)?",
                             "Please provide a field").strip().lower()

        while field not in ["author", "title", "year", "publisher"]:
            self.io.write("Please give one of the listed fields")
            field = self.io.read("Which field of the given reference "
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

    # can abstract somewhere
    def __check_id_exists(self):
        reference_id = self.io.read("Enter reference ID: ",
                                    "Please provide a reference ID")
        # loop till given id exists in db
        while self.repository.id_exists(reference_id) == False:
            self.io.write("No such reference ID exists")
            reference_id = self.io.read("Enter reference ID: ",
                                        "Please provide a reference ID")
        return reference_id
