#coding: utf-8

from concurrent.futures import as_completed, process
from concurrent.futures.thread import ThreadPoolExecutor
from argparse import ArgumentParser
from modules.beautify import render
from modules.formatters import keyvalue
from sys import exit as ext
from modules.functions import *
from variables.codes import *

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

# Variables

urls = []

f = functions(args)

if args.pheaders:
    headers = args.pheaders

else:
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

def create_list():
    global urls

    result = f.createList()

    if result['status'] == status_error:
        print(result['message'])
    elif result['status'] == status_ok:
        urls = result['message']    
        
def start():
    processes = []

    if args.threads:
        if args.threads == 1:
            print("[+] Running in single thread mode")
    
        pool = ThreadPoolExecutor(max_workers=args.threads)

    else:
        pool = ThreadPoolExecutor(max_workers=10)

    for i in urls:
        processes.append( pool.submit(f.send, i, headers, 404))

    for future in as_completed(processes):
        try:
            if future.result()['status'] == request_successful:
                print(future.result()['message'])

            if future.result()['status'] == unkdownError:
                print(future.result()['message'])

        except Exception as error:
            print(error)
        
if __name__ == '__main__':
    if "FUZZ" not in args.target:
        print('Please add \"FUZZ\" in target')
        ext(1)

    print(render())
    create_list()
    start()
