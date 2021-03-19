import socket
import threading

file_format = 'UTF-8'
# Configure the connection to the internet
host = input('What is the ip? (local Ipv4) ')
try:
    port = int(input('What is the room number you want to open? 1000-6000 '))
except:
    print('Wrong Room Code | ERROR')
    quit()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((host, port))
except:
    print('Failed to connect!')
    quit()
server.listen()
print('connected')
# list's
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} Left'.encode(file_format))
            print(f'{nickname} left')
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, addr = server.accept()

        client.send('NICK'.encode(file_format))

        nickname = client.recv(1024).decode(file_format)
        nicknames.append(nickname)
        clients.append(client)

        print(f'{nickname} {addr} joined')
        broadcast(f'{nickname} joined'.encode(file_format))
        client.send('Connected'.encode(file_format))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is up...')
receive()
