import sys
from command import Command
from repositories.reference_repository import ReferenceRepository


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        ## TODO: start interactive console
        return

    command = Command(ReferenceRepository())
    if args[0] == "add":
        command.add()


if __name__ == "__main__":
    main()
