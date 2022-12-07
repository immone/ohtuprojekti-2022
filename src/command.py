import sys
from entities.reference import Reference


class Command:
    def __query_non_empty(self, prompt, empty_msg):
        query = input(prompt)
        while len(query) == 0:
            print(empty_msg)
            query = input(prompt)

        return query
