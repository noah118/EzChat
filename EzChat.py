import socket
import threading

file_format = 'UTF-8'
# Configure the connection to the internet
host = input('What is the ip? (Public Ipv4) ')
try:
    port = int(input('What is the room number you want to open? 1000-6000 '))
except:
    print('Error')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((host, port))
except:
    print('Failed to connect!')
    quit()

nickname = input('Choose a nickname! ')


def receive():
    while True:
        try:
            message = client.recv(1204).decode(file_format)
            if message == 'NICK':
                client.send(nickname.encode(file_format))
            else:
                print(message)
        except:
            print('Error')
            client.close()
            break


def write():
    while True:
        message = f'[{nickname}]: {input("")}'
        client.send(message.encode(file_format))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
