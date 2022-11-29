import sys
from commands.add import Add
from commands.translator import Translator
from repositories.reference_repository import ReferenceRepository
from console_io import ConsoleIO

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        ## TODO: start interactive console
        return

    if args[0] == "add":
        add = Add(ReferenceRepository(), ConsoleIO())
        add.run()

    if args[0] == "bibtex":
        translator = Translator(ReferenceRepository(), ConsoleIO())
        translator.run()

if __name__ == "__main__":
    main()
