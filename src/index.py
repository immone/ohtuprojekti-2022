import sys
from commands.add import Add
from commands.translator import Translator
from repositories.reference_repository import ReferenceRepository
from services.reference_service import ReferenceService
from console_io import ConsoleIO
from services.reference_service import ReferenceService

def main():

    args = sys.argv[1:]
    if len(args) == 0:
        io = ConsoleIO()
        while True:
            command = io.read("Enter command: ", "Please provide a valid command")
            if command == "add":
                add()
            if command == "bibtex":
                bibtex()
            if command == "help":
                help(io)
    if args[0] == "add":
        add()
    if args[0] == "bibtex":
        bibtex()
def help(io):
    io.write("Give: ")
    io.write("add -- To add new reference")
    io.write("bibtex -- To print all references")

def add():
    add = Add(ReferenceService(),ConsoleIO())
    add.run()
def bibtex():
    translator = Translator(ReferenceService(), ConsoleIO())
    translator.run()

if __name__ == "__main__":
    main()
