class ConsoleIO:
    def read(self, prompt, empty_msg=None):
        query = input(prompt)

        if not empty_msg is None:
            while len(query) == 0:
                print(empty_msg)
                query = input(prompt)

        return query

    def write(self, data):
        print(data)
