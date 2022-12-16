import sys
import re
import datetime
from entities.reference import Reference
from services.reference_service import ReferenceService

class Edit():
    def __init__(self, service, io):
        self.io = io
        self.service = service

## TODO: parameters for one-liner

    def run(self, *params):
        self.io.write("Attempting to edit a reference..")
        self.__edit_whole_reference()

# TODO: fix one-liner s.t. there is no danger of inputting wrong type of data into the DB

    def __edit_one_liner(self, params):
        if not self.service.id_exists(params[0]):
            self.io.write("Cannot find ID. Exiting..")
            return
        try:
            self.service.put(params[0], params[1], params[2])
            self.io.write("\nReference edited.")
        except:
            sys.exit(
                "\nAn error occurred while trying to edit reference. Exiting..")

    def __edit_whole_reference(self):
        id_to_edit = self.__check_id_exists()
        if id_to_edit == None:
            return
        type_to_edit = self.service.get_type(id_to_edit)
        if type_to_edit == "book":
            new_ref_dict = self.__edit_book()
        elif type_to_edit == "inproceedings":
            new_ref_dict = self.__edit_inproceedings()
        elif type_to_edit == "misc":
            new_ref_dict = self.__edit_misc()
        else:
            sys.exit("Could not find the type of the reference. Exiting..")
        for key in new_ref_dict:
            ref = self.service.get(id_to_edit)
            if len(str(new_ref_dict[key])) == 0 or (key in ["tags, author"] and new_ref_dict[key] == []):
                new_ref_dict[key] = ref[key]
        try:
            for val in new_ref_dict:
                self.service.put(id_to_edit, val, new_ref_dict[val])
            self.io.write("\nReference edited.")
        except:
            sys.exit(
                "\nAn error occurred while trying to edit reference. Exiting..")

    # can abstract somewhere
    def __check_id_exists(self):
        reference_id = self.io.read("Enter reference ID: ",
                                    "Please provide a reference ID")
        if not self.service.id_exists(reference_id):
            self.io.write("No such reference ID exists")
            reference_id = None
        return reference_id

    def __edit_book(self):
        title = self.__query_title()
        authors = self.__query_authors()
        year = self.__query_year()
        publisher = self.io.read(" ... enter publisher (press enter to retain old value):")
        tags = self.__query_tags()
        new_ref_object = {
            "type": "book",
            "title": title,
            "author": authors,
            "year": year,
            "publisher": publisher,
            "tag": tags
        }

        return new_ref_object

    def __edit_inproceedings(self):
        title = self.__query_title()
        book_title = self.__query_booktitle()
        authors = self.__query_authors()
        series = self.__query_series()
        year = self.__query_year()
        pages = self.__query_pages()
        publisher = self.io.read(" ... enter publisher (press enter to retain old value):")
        address = self.io.read(" ... enter address (press enter to retain old value): ")
        tags = self.__query_tags()

        new_ref_object =  {
            "type": "inproceedings",
            "title": title,
            "booktitle": book_title,
            "author": authors,
            "series": series,
            "year": year,
            "pages": pages,
            "publisher": publisher,
            "address": address,
            "tag": tags
        }
        return new_ref_object

    def __edit_misc(self):
        title = self.__query_title()
        authors = self.__query_authors()
        how_published = self.io.read(" ... enter how published (press enter to retain old value): ")
        year = self.__query_year()
        note = self.io.read(" ... enter note (press enter to retain old value): ")
        tags = self.__query_tags()

        new_ref_object = {
            "type": "misc",
            "title": title,
            "author": authors,
            "howpublished": how_published,
            "year": year,
            "note": note,
            "tag": tags
        }
        return new_ref_object

    def __query_title(self):
        while True:
            title = self.io.read(" ... enter new title (press enter to retain old value):",)

            if len(title) <= 300:
                return title

            self.io.write(
                " ...... please provide a valid title (max length: 300 characters)")

    def __query_booktitle(self):
        while True:
            title = self.io.read(" ... enter book title (press enter to retain old value):")

            if len(title) <= 300:
                return title

            self.io.write(
                " ...... please provide a valid book title (max length: 300 characters)")

    def __query_authors(self):
        name_regex = "^[a-zA-Z][a-zA-Z'.-]*(?: [a-zA-Z'.-]+)*[a-zA-Z]$"

        while True:
            authors = self.io.read(" ... enter new authors (delimited by semicolons) [format: [FirstName(s)] LastName] (press enter to retain old value):")

            if len(authors) == 0:
                return ""

            authors = [a.strip() for a in authors.split(";")]
            authors = list(filter(lambda a: len(a) > 0, authors))

            if len(authors) > 0 and all(re.search(name_regex, a) for a in authors):
                break

            self.io.write(" ...... please provide valid author(s)")

        return authors

    def __query_year(self):
        while True:
            year = self.io.read(" ... enter new year of publication (press enter to retain old value):")

            if len(year) == 0:
                return ""
            elif year.isnumeric() and int(year) > 0 and int(year) <= datetime.date.today().year:
                return int(year)

            self.io.write(" ...... please provide a valid year")

    def __query_series(self):
        while True:
            series = self.io.read(" ... enter new value for series (press enter to retain old value): ")

            if len(series) <= 300:
                return series

            self.io.write(
                " ...... please provide a valid series (max length: 300 characters)")

    def __query_pages(self):
        pages_regex = "^[1-9][0-9]*--[1-9][0-9]*$"

        while True:
            pages = self.io.read(" ... enter new pages (format: N--M) (press enter to retain old value): ")
            nums = pages.split("--")

            if len(pages) == 0 or (re.match(pages_regex, pages) and nums[0] < nums[1]):
                return pages

            self.io.write(
                " ...... please provide valid pages")

    def __query_tags(self):
        tags = self.io.read(" ... enter new reference tags (delimited by semicolons) (press enter to retain old value):")
        return [t.strip() for t in tags.split(";")]
