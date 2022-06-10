from variables.codes import *
from modules.beautify import formatError

try:
    from requests import get
except:
    print("Dependy requests not found!")

code = 404

class functions():
    def __init__(self,args):
        self.args = args

    def createList(self):
        urls = []

        try:
            file = open(self.args.wordlist)
            read_file = file.read().splitlines()
            for i in read_file:
                new_url = self.args.target.replace('FUZZ', i)
                urls.append(new_url)
            file.close()   
            
            return formatError(status_ok, urls)

        except Exception as error:
            return formatError(status_error, error)

    # def send(self,url, rheader=headers, status_code=code):
    #     try:
    #         r = get(url, headers=rheader)
    #         response = r.status_code
    #         if response != status_code:
    #             if args.etext:
    #                 content = r.text
    #                 if args.etext not in content:
    #                     print(f"[{response}]    {url}")
    #             else:
    #                 print(f"[{response}]    {url}")
          
    #         elif args.verbose:
    #             print(f"[{response}]    {url}")
          
    #         else:
    #             pass
    #     except:
    #         pass