class ConsoleIO:
    def read(self, prompt):
        return input(prompt)

    def read_non_empty(self, prompt, empty_msg):
        query = input(prompt)
        while len(query) == 0:
            print(empty_msg)
            query = input(prompt)

        return query

    def write(self, data):
        print(data)