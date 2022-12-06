class ConsoleIO:
    def read(self, prompt, empty_msg):
        query = input(prompt)
        while len(query) == 0:
            print(empty_msg)
            query = input(prompt)

        return query

    def read_opt(self, prompt):
        return input(prompt)

    def write(self, data):
        print(data)
