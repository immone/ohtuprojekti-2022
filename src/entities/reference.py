class Reference:
    def __init__(self, reference_id: str, authors: list, title: str, year: int, publisher: str, tags: list = None) -> None:
        self.__reference_id = reference_id
        self.__authors = authors
        self.__title = title
        self.__year = year
        self.__publisher = publisher
        self.__tags = tags

    def __str__(self) -> str:
        return f"{', '.join(self.authors)}. {self.title}. {self.publisher}, {self.year}."

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return other.to_dict() == self.to_dict()
        else:
            return False

    @property
    def reference_id(self):
        return self.__reference_id

    @property
    def authors(self):
        return self.__authors

    @property
    def title(self):
        return self.__title

    @property
    def year(self):
        return self.__year

    @property
    def publisher(self):
        return self.__publisher

    @property
    def tags(self):
        return self.__tags

    def to_dict(self):
        return {
            "reference_id": self.reference_id,
            "title": self.title,
            "year": self.year,
            "publisher": self.publisher,
            "authors": self.authors,
            "tags": self.tags
        }
