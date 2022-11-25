class Command:
    def __init__(self, repository=None):
        self.repository = repository

    def add(self):
        print("Adding new reference...")

        reference_id = self.__query_non_empty("Enter reference ID: ",
            "Please provide a reference ID")
        # TODO: use repository object to ensure ID is unique

        title = self.__query_non_empty("Enter reference title: ",
            "Please provide a reference title")

        authors = self.__query_authors()
        year = self.__query_year()

        print(authors)
        # TODO: use repository object to add reference
        print("\nReference added.")

    def __query_non_empty(self, prompt, empty_msg):
        query = input(prompt)
        while len(query) == 0:
            print(empty_msg)
            query = input(prompt)

        return query

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
