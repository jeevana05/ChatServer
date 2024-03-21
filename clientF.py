import socket
import ssl
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nickname = input("Choose a nickname: ")
if nickname == 'admin':
    password = input("enter the password for admin: ")

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.load_verify_locations("server.crt")  # Provide the server's certificate

# Wrap the client socket with the SSL context
client_ssl = context.wrap_socket(client, server_hostname="192.168.203.227")

client_ssl.connect(('192.168.203.227', 55555))

# print("SSL/TLS handshake successful!")
# print("Peer certificate:", client_ssl.getpeercert())
# print("Cipher:", client_ssl.cipher())
# print("SSL version:", client_ssl.version())


stop_thread = False

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client_ssl.recv(1024).decode('ascii')
            if message == 'JEEVANA':
                client_ssl.send(nickname.encode('ascii'))
                next_message = client_ssl.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client_ssl.send(password.encode('ascii'))
                    if client_ssl.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection refused, wrong password")
                        stop_thread = True
                elif next_message == 'BAN':
                    print("connection refused because of ban")
                    client_ssl.close()
                    stop_thread = True
            else:
                print(message)
        except Exception as e:
            print("an error occured", e)
            client_ssl.close()
            break

def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith("/"):             #username: /command
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client_ssl.send(f'KICK{message[len(nickname)+2+5:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client_ssl.send(f'BAN{message[len(nickname)+2+4:]}'.encode('ascii'))
            else:
                print("commands can only be executed by the admin")
        else:
            client_ssl.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()