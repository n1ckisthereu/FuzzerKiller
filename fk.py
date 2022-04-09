#coding: utf-8

try:
    import requests
except:
    print("Dependy requests not found!")

import sys
import time
from threading import Thread
from argparse import ArgumentParser
import argparse
import threading

class keyvalue(argparse.Action): 
    def __call__( self , parser, namespace, 
                 values, option_string = None): 
        setattr(namespace, self.dest, dict()) 
        for value in values: 
              key, value = value.split('=') 
              getattr(namespace, self.dest)[key] = value 

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
args = parser.parse_args()

if "FUZZ" not in args.target:
    print('Please add \"FUZZ\" in target')
    sys.exit(1)

def render():
    print("""                                              
    ______                      _   ___ _ _           
    |  ___|                    | | / (_) | |          
    | |_ _   _ ___________ _ __| |/ / _| | | ___ _ __ 
    |  _| | | |_  /_  / _ \ '__|    \| | | |/ _ \ '__|
    | | | |_| |/ / / /  __/ |  | |\  \ | | |  __/ |   
    \_|  \__,_/___/___\___|_|  \_| \_/_|_|_|\___|_|   
                                                  
    
    Developed by                   @eumn1ck @thisfarias
    """)

urls = []

if args.pheaders:
    headers = args.pheaders
    print(headers)
else:
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

code = 404

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
        else:
            pass
    except:
        pass

def create_list():
    global urls
    
    try:
        file = open(args.wordlist)
        read_file = file.read().splitlines()
        for i in read_file:
            new_url = args.target.replace('FUZZ', i)
            urls.append(new_url)
            
        file.close()   
        
    except Exception as error:
        print(error)
        
def start():
    if args.threads:
        print('Scan started at ' + time.strftime('%x %X %z') + '\n')
        count = 1
        var_threads = args.threads + 1   
        for i in urls:
            while True:     
                if count < var_threads:          
                    count += 1 
                    a = Thread(target=send, args=(i,))
                    a.start()                     
                    break
                if len(threading.enumerate()) < var_threads:
                    count -= var_threads - len(threading.enumerate())
        print('\nScan finished at '  + time.strftime('%x %X %z')) 
    else:
        for i in urls:
            send(i)

render()
create_list()
start()
