import sys
from commands.add import Add
from commands.translator import Translator
from commands.search import Search
from repositories.reference_repository import ReferenceRepository
from services.reference_service import ReferenceService
from console_io import ConsoleIO
from services.reference_service import ReferenceService

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        io = ConsoleIO()
        while True:
            command = io.read("Enter command: ", "Please provide a command")
            if command == "add":
                add()
            elif command == "bibtex":
                bibtex()
            elif command == "help":
                list_commands(io)
            elif command == "search":
                search()
            elif command == "exit":
                return
            else:
                list_commands(io)

    if args[0] == "add":
        add()
    elif args[0] == "bibtex":
        bibtex()
    elif args[0] == "search":
        search()

def list_commands(io):
    io.write("Give: ")
    io.write("add -- To add new reference")
    io.write("bibtex -- To print all references")
    io.write("exit -- To stop program")


def add():
    add = Add(ReferenceService(), ConsoleIO())
    add.run()


def bibtex():
    translator = Translator(ReferenceService(), ConsoleIO())
    translator.run()


def search():
    search = Search(ReferenceService(), ConsoleIO())


if __name__ == "__main__":
    main()
