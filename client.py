# Import socket module 
import socket             
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import json
#priv key reading below
PSS = padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH,
)
with open( "client_private.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(), password=None
    )

with open("config.json") as file:
    config = json.load(file)

host = config["host"]
port = config["port"]

# Create a socket object 
s = socket.socket()                
print ("Socket successfully created")                

# Next bind to the port  
s.bind(('', port))         
print ("socket binded to %s" %(port)) 

# put the socket into listening mode 
s.listen(5)     
print ("socket is listening") 

while True:
    c, addr = s.accept()
    #listen and wait here for week4 machine to connect
    print ('Got connection from', addr )
    #recieve the request to sign and sign with priv key
    request_to_sign = c.recv(1024)
    c.sendall(private_key.sign(request_to_sign, PSS, hashes.SHA256()))

    #get welcome message
    print(c.recv(1024).decode())
    while True:
        #interactive shell, sends all commands back to week 4 machine
        print("Enter a command")
        cmd = input()
    
        c.send(cmd.encode())
        print (c.recv(8024).decode())
        if cmd == "close":
            break


    c.close()
