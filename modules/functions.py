from variables.codes import *
from modules.beautify import formatError, returnMessage

try:
    from requests import get
except:
    print("Dependy requests not found!")


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

    def send(self,url, header, status_code):
        try:
            r = get(url, headers=header)
            response = r.status_code
            if response != status_code:
                if self.args.etext:
                    content = r.text
                    if self.args.etext not in content:
                        return returnMessage(request_successful, f"[{response}]    {url}")
                        
                else:
                    return returnMessage(request_successful, f"[{response}]    {url}")
        
            elif self.args.verbose:
                return returnMessage(request_successful, f"[{response}]    {url}")
            
            else:
                return returnMessage(ignore, None)
        except:
                return returnMessage(unkdownError, "[!] Unkdown error")
                