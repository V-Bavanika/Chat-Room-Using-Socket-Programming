import threading as threading
import socket as socket


host = "127.0.0.1"
port =5555 #user def. port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4 address.

server.bind((host, port))

server.listen()

clients = []
nicknames = []

# Broadcasting
def broadcast(received_msg_at_server):
    for client in clients:
        client.send(received_msg_at_server)

#Recieving Messages
def handle(client):
    while True:
        try:
            msg = received_msg_at_server = client.recv(1024)  
            if msg.decode('ascii').startswith('REPORT'):
                if nicknames[clients.index(client)] in ['Shuvam','Bavanika','Tanushree']:
                    name_to_kick = msg.decode('ascii')[7:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command Refused!'.encode('ascii'))
            elif msg.decode('ascii').startswith('BLOCK'):
                if nicknames[clients.index(client)] in ['Shuvam','Bavanika','Tanushree']:
                    name_to_ban = msg.decode('ascii')[6:]
                    kick_user(name_to_ban)
                    with open('blocked_users.txt','a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned by the Admin!')
                else:
                    client.send('Command Refused!'.encode('ascii'))
            else:
                broadcast(received_msg_at_server)   
        
        except:
            if client in clients:
                index = clients.index(client)
                #Index : for keeping active clients only.
                client.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(f'{nickname} left the Chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break
# Reciever func.
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        
        with open('blocked_users.txt', 'r') as f:
            bans = f.readlines()
        
        if nickname+'\n' in bans:
            client.send('BLOCK'.encode('ascii'))
            client.close()
            continue

        if nickname in ['Shuvam','Bavanika','Tanushree']:
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            
            if password != 'p@ssw0rd':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'UserID of the client is {nickname}')
        broadcast(f'{nickname} joined the Chat'.encode('ascii'))
        client.send('Connected to the Server!'.encode('ascii'))

        #using threads to make process lighter & faster & scalable.
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames and name not in ['Shuvam','Bavanika','Tanushree'] :
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You Were Kicked from Chat !'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked from the server!'.encode('ascii'))
    else :
        broadcast(f'{name} can\'t be kicked from the server!'.encode('ascii'))


#__main__()
print('Server is Running & Listening ...at :127.0.0.1:5555\n')
recieve()