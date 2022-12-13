import sys
import datetime
import unicodedata
import re
from abc import ABC, abstractmethod
from entities.reference import Reference


class Adder(ABC):
    def __init__(self, io):
        self.io = io
    
    @abstractmethod
    def run(self):
        pass

    def _query_title(self, optional=False):
        while True:
            title = self.io.read(f" ... enter title{' (optional)' if optional else ''}: ",
                                 " ...... please provide a title" if not optional else None)

            if len(title) <= 300: 
                return title

            self.io.write(
                " ...... please provide a valid title (max length: 300 characters)")

    def _query_authors(self, optional=False):
        name_regex = "^[a-zA-Z][a-zA-Z'.-]*(?: [a-zA-Z'.-]+)*[a-zA-Z]$"

        while True:
            authors = self.io.read(f" ... enter authors (delimited by semicolons) (format: [FirstName(s)] LastName){' (optional)' if optional else ''}: ",
                                    " ...... please provide at least one author" if not optional else None)

            if optional and authors == "":
                return authors

            authors = [a.strip() for a in authors.split(";")]
            authors = list(filter(lambda a: len(a) > 0, authors))

            if len(authors) > 0 and all(re.search(name_regex, a) for a in authors):
                break

            self.io.write(" ...... please provide valid author(s)")

        return authors

    def _query_year(self, optional=False):
        while True:
            year = self.io.read(f" ... enter year of publication{' (optional)' if optional else ''}: ",
                                " ...... please provide a year" if not optional else None)

            if optional and year == "":
                return year

            if year.isnumeric() and int(year) > 0 and int(year) <= datetime.date.today().year:
                return int(year)

            self.io.write(" ...... please provide a valid year")

    def _query_tags(self):
        tags = self.io.read(" ... enter reference tags (delimited by semicolons) (optional): ")
        return [t.strip() for t in tags.split(";")]


class BookAdder(Adder):
    def run(self):
        title = self._query_title()
        authors = self._query_authors()
        year = self._query_year()
        publisher = self.io.read(" ... enter publisher: ",
                                 " ...... please provide a publisher")
        tags = self._query_tags()

        return {
            "type": "book",
            "title": title,
            "author": authors,
            "year": year,
            "publisher": publisher,
            "tags": tags
        }


class InProceedingsAdder(Adder):
    def run(self):
        title = self._query_title()
        booktitle = self.__query_booktitle()
        authors = self._query_authors()
        series = self.__query_series() # optional
        year = self._query_year()
        pages = self.__query_pages() # optional
        publisher = self.io.read(" ... enter publisher (optional): ")
        address = self.io.read(" ... enter address (optional): ")
        tags = self._query_tags()

        return {
            "type": "inproceedings",
            "title": title,
            "booktitle": booktitle,
            "author": authors,
            "series": series,
            "year": year,
            "pages": pages,
            "publisher": publisher,
            "address": address,
            "tags": tags
        }


    def __query_booktitle(self):
        while True:
            title = self.io.read(" ... enter book title: ",
                                 " ...... please provide a book title")

            if len(title) <= 300:
                return title

            self.io.write(
                " ...... please provide a valid book title (max length: 300 characters)")

    def __query_series(self):
        while True:
            series = self.io.read(" ... enter series (optional): ")

            if len(series) <= 300:
                return series

            self.io.write(
                " ...... please provide a valid series (max length: 300 characters)")

    def __query_pages(self):
        pages_regex = "^[1-9]+--[1-9]+$"

        while True:
            pages = self.io.read(" ... enter pages (format: N--M) (optional): ")
            nums = pages.split("--")
            
            if len(pages) == 0 or (re.match(pages_regex, pages) and nums[0] < nums[1]):
                return pages

            self.io.write(
                " ...... please provide valid pages")


class MiscAdder(Adder):
    def run(self):
        title = self._query_title(True)
        authors = self._query_authors(True)
        howpublished = self.io.read(" ... enter how published (optional): ")
        year = self._query_year(True)
        note = self.io.read(" ... enter note (optional): ")
        tags = self._query_tags()

        return {
            "type": "misc",
            "title": title,
            "author": authors,
            "howpublished": howpublished,
            "year": year,
            "note": note,
            "tags": tags
        }


class Add:
    def __init__(self, service, io):
        self.service = service
        self.io = io

    def run(self):
        ref_type = self.__query_ref_type()
        handlers = {
            "book": BookAdder(self.io),
            "inproceedings": InProceedingsAdder(self.io),
            "misc": MiscAdder(self.io)
        }

        self.io.write(f"Adding new {ref_type} reference...")
        ref = handlers[ref_type].run()

        # optional fields could be empty (either strings or arrays), so filter them out
        ref = {k: v for k, v in ref.items() if type(v) == int or len(v) > 0}

        ref_id = self.generate_ref_id(ref["author"] if "author" in ref.keys() else [ref["type"]],
                ref["year"] if "year" in ref.keys() else None)
        ref["reference_id"] = ref_id

        try:
            self.service.post(ref)
            self.io.write(f"\nReference added with id '{ref_id}'.")
        except:
            sys.exit("\nA database error occurred. Failed to add reference.")

    def __query_ref_type(self):
        types = ["book", "inproceedings", "misc"]

        while True:
            ref_type = self.io.read("Select type of reference to add (1=book, 2=inproceedings, 3=misc): ",
                                    " ... please provide a number between 1 and 3")

            if ref_type.isnumeric() and int(ref_type) >= 1 and int(ref_type) <= 3:
                return types[int(ref_type) - 1]

            self.io.write(" ... please provide a valid number between 1 and 3")

    # public so that AddLibrary can access it
    def generate_ref_id(self, authors, year):
        iteration = 0
        while True:
            author_lastname = authors[0].split()[-1]
            ref_id = author_lastname[:10] + (str(year) if year else '')
            ref_id = self.__normalize_str(ref_id) + (f"_{iteration}" if iteration > 0 else "")

            if not self.service.id_exists(ref_id):
                return ref_id

            iteration += 1

    # from https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
    def __normalize_str(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn' and c.isalnum())
