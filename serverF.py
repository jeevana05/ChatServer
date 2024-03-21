import socket
import ssl
import threading

host = '192.168.203.227'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Wrap the server socket with the SSL context
server_ssl = context.wrap_socket(server, server_side=True)

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if not msg:
                break  # Break the loop if no data is received
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick, ban=False)
                else:
                    client.send('command was refused'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban, ban=True)
                    print(f'{name_to_ban} was banned')
                    # Close the client connection after banning
                    client.close()
                else:
                    client.send('command was refused'.encode('ascii'))
            else:
                broadcast(message)
        except OSError as e:
            print(f"An error occurred in handle: {e}")
            break  # Break the loop on OSError
        except Exception as e:
            print("An unexpected error occurred in handle:", e)
            break  # Break the loop on any other exception

    # Client has disconnected
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        nickname = nicknames[index]
        broadcast(f'{nickname} left the chat'.encode('ascii'))
        nicknames.remove(nickname)
    client.close()


def receive():
    while True:
        client, address = server_ssl.accept()
        print(f'connected with {str(address)}')

        # ip_address = address[0]

        client.send('JEEVANA'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        
        if nickname+'\n' in bans: #if ip_address+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
        
        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password!='adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue
        
        nicknames.append(nickname)
        clients.append(client)
        print(f'nickname of client is {nickname}')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('connected to the server '.encode('ascii'))

        thread = threading.Thread(target = handle, args=(client,))
        thread.start()

def kick_user(name, ban=False):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        nicknames.remove(name)

        if ban:
            # Add the banned user to the bans.txt file
            with open('bans.txt', 'a') as f:
                f.write(f'{name}\n')

        client_to_kick.send(f'You were kicked by the admin'.encode('ascii'))
        client_to_kick.close()

        if ban:
            broadcast(f'{name} was banned by an admin'.encode('ascii'))
        else:
            broadcast(f'{name} was kicked by an admin'.encode('ascii'))
    else:
        broadcast(f'{name} not found'.encode('ascii'))

# def kick_user(identifier, ban=False):
#     if ban:
#         # Add the banned IP address to bans.txt file
#         with open('bans.txt', 'a') as f:
#             f.write(f'{identifier}\n')

#     for c, addr in zip(clients, addresses):
#         if addr[0] == identifier:
#             c.send(f'You were kicked by the admin{" and banned" if ban else ""}'.encode('ascii'))
#             c.close()
#             index = clients.index(c)
#             clients.remove(c)
#             nickname = nicknames[index]
#             broadcast(f'{nickname} was kicked by an admin'.encode('ascii'))
#             nicknames.remove(nickname)




print("server is listening")
receive()