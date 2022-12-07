import sys
from commands import Add, Help, Search, Translator
from services import ReferenceService
from console_io import ConsoleIO

def main():
    args = sys.argv[1:]
    menu_io = ConsoleIO()
    if len(args) == 0:
        menu_io.write(Help.get("file"))
        while True:
            command = menu_io.read("Enter command: ", "Please provide a command")
            if command == "add":
                add()
            elif command == "bibtex":
                bibtex()
            elif command == "help":
                menu_io.write(Help.get("file"))
            elif command == "search":
                search()
            elif command == "exit":
                return
            else:
                menu_io.write(Help.get("file"))

    if args[0] == "add":
        add()
    elif args[0] == "help":
        menu_io.write(Help.get("console"))
    elif args[0] == "bibtex":
        bibtex()
    elif args[0] == "search":
        search()

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
