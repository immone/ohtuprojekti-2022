import sys
from commands import Add, Help, Search, Translator, Delete, Edit, List
from services import ReferenceService
from console_io import ConsoleIO

def main():
    args = sys.argv[1:]
    menu_io = ConsoleIO()
    command_handlers = {
        "add": add,
        "bibtex": bibtex,
        "help": lambda: menu_io.write(Help.get("file")),
        "search": search,
        "edit": edit,
        "list": list,
        "delete": delete,
        "exit": lambda: None,
    }
    if len(args) == 0:
        menu_io.write(Help.get("file"))
        while True:
            command = menu_io.read("Enter command: ", "Please provide a command")
            if command in command_handlers:
                command_handlers[command]()
            else:
                menu_io.write(Help.get("file"))

    if args[0] in command_handlers:
        command_handlers[args[0]]()

def add():
    add = Add(ReferenceService(), ConsoleIO())
    add.run()


def bibtex():
    translator = Translator(ReferenceService(), ConsoleIO())
    translator.run()


def search():
    search = Search(ReferenceService(), ConsoleIO())
    search.run()


def delete():
    delete = Delete(ReferenceService(), ConsoleIO())
    delete.run()

def edit():
    edit = Edit(ReferenceService(), ConsoleIO())
    edit.run()

def list():
    list = List(ReferenceService(), ConsoleIO())
    list.run()

if __name__ == "__main__":
    main()
