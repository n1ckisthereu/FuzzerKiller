#coding: utf-8

try:
    import requests
except:
    print("Dependy requests not found!")

from concurrent.futures.thread import ThreadPoolExecutor
from argparse import ArgumentParser
from modules.beautify import render
from modules.formatters import keyvalue
from sys import exit as ext
from modules.functions import *
from status.codes import *

parser = ArgumentParser(usage='fk {options} [TARGET]')
parser.add_argument('target', help='Specify the target to scan.')
parser.add_argument('-w', '--wordlist', dest='wordlist', required=True, metavar="",
        help='Pass wordlist for fuzzing!')
parser.add_argument('-t', '--threads', type=int ,dest='threads', default=1, metavar="",
        help='number of threads u.u')

parser.add_argument('-e', '--error-text', dest='etext', metavar="",
        help='If the text passed in this argument is not on the page and the status code is != 404 the script will return success')

parser.add_argument('-H', '--headers', nargs='*', action=keyvalue, dest='pheaders', metavar="",
        help='Pass headers format "key=value" "key1=value1"')

parser.add_argument('-v', '--verbose', action='store_true', help='-v to Verbose mode')

args = parser.parse_args()

if "FUZZ" not in args.target:
    print('Please add \"FUZZ\" in target')
    ext(1)

urls = []
code = 404

if args.pheaders:
    headers = args.pheaders
    print(headers)
else:
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}


def send(url, rheader=headers, status_code=code):
    try:
        r = requests.get(url, headers=rheader)
        response = r.status_code
        if response != status_code:
            if args.etext:
                content = r.text
                if args.etext not in content:
                    print(f"[{response}]    {url}")
            else:
                print(f"[{response}]    {url}")
        
        elif args.verbose:
            print(f"[{response}]    {url}")
        
        else:
            pass
    except:
        pass

def create_list(args):
    global urls

    teste = functions()
    result = teste.createList(args)

    if result['status'] == status_error:
        print(result['message'])
    elif result['status'] == status_ok:
        urls = result['message']    
        
def start():
    if args.threads:
        if args.threads == 1:
            print("[+] Running in single thread mode")
    
        pool = ThreadPoolExecutor(max_workers=args.threads)
    
    else:
        pool = ThreadPoolExecutor(max_workers=10)

    for i in urls:
        pool.submit(send, i)

if __name__ == '__main__':
    if "FUZZ" not in args.target:
        print('Please add \"FUZZ\" in target')
        ext(1)

    print(render())
    create_list(args)
    start()
