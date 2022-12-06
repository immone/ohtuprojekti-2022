import sys
from commands.add import Add
from commands.translator import Translator
from repositories.reference_repository import ReferenceRepository
from console_io import ConsoleIO
from services.reference_service import ReferenceService

def main():

    args = sys.argv[1:]
    if len(args) == 0:
        io = ConsoleIO()
        while True:
            io.write("Give: ")
            io.write("add -- To add new reference")
            io.write("bibtex -- To print all references")
            command = io.read("Enter command: ", "Please provide a valid command")
            if command == "add":
                add()
            if command == "bibtex":
                bibtex()

    if args[0] == "add":
        add()
    if args[0] == "bibtex":
        bibtex()

def add():
        add = Add(ReferenceSerice(),ConsoleIO())
        add.run()
def bibtex():
        translator = Translator(ReferenceService(), ConsoleIO())
        translator.run()

if __name__ == "__main__":
    main()
