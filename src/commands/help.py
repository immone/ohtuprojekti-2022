class Help:
    @staticmethod
    def console():
        return """\nRun interactive mode without arguments 
Optional arguments: -a[dd] -s[earch] -b[ibtex] -h[elp]\n"""

    @staticmethod
    def file():
        return """\nCommands: \n
add -- To add new reference
bibtex -- To print all references
search -- To search for references
exit -- To stop program\n"""

    @staticmethod
    def get(type):
        if type == "console":
            return Help.console()
        elif type == "file":
            return Help.file()
        else:
            return None
