from status.codes import *
from modules.beautify import formatError

class functions():
    def __init__(self) -> None:
        pass

    def createList(self, args):
        urls = []

        try:
            file = open(args.wordlist)
            read_file = file.read().splitlines()
            for i in read_file:
                new_url = args.target.replace('FUZZ', i)
                urls.append(new_url)
            file.close()   
            
            return formatError(status_ok, urls)

        except Exception as error:
            return formatError(status_error, error)

    def send():
        pass