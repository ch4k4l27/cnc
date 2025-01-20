import socket # para criar uma nova conexão
from termcolor import colored # para dar cor ao terminal

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('172.22.163.174', 4444))

print(colored('[-] Waiting for connections', 'yellow'))
sock.listen(5)

target, ip = sock.accept()
print(colored(f'[+] Connected with: {str(ip)}', 'green'))
