import socket as socket
import threading as threading
import getpass
 
userid = input("Choose Your Name:")

while((userid ==' ') or (len(userid)==0 ) or userid.startswith(('0','1','2','3','4','5','6','7','8','9'))):
    print("Enter a valid user name(mustnot begin with \'\' or \' \' or a num)")
    userid = input("Choose Your Name:")
    
if userid in ['Shuvam','Bavanika','Tanushree']:
    password = getpass.getpass("Enter Password for Admin access:")  #input("Enter Password for Admin access:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect to a host
client.connect(('127.0.0.1',5555))

stop_thread = False

def my_admin_works(message):
    
    if message[len(userid)+2:].startswith('_'):
            if userid in ['Shuvam','Bavanika','Tanushree']:
                
                if message[len(userid)+2:].startswith('_REPORT_'):
                    
                    client.send(f'REPORT {message[len(userid)+2+9:]}'.encode('ascii'))
                elif message[len(userid)+2:].startswith('_BLOCK_'):
                    
                    client.send(f'BLOCK {message[len(userid)+2+8:]}'.encode('ascii'))
                
            else:
                print("_privileged_ commands can only be executed by admin!!")
    else:
        client.send(message.encode('ascii'))


def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break    
        try:
            message = client.recv(1024).decode('ascii')
            
            if message == 'NICK':
                client.send(userid.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Refused to connect\nError : Incorrect password")
                        stop_thread = True
                
                elif next_message == 'BLOCK':
                    print("Connection Refused due to BLOCK")
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            
            print("Error Occured while Connecting")
            client.close()
            break
        
def write():
    while True:
        if stop_thread:
            break
        
        message = f'{userid}: {input("")}'
        
        my_admin_works(message)

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()