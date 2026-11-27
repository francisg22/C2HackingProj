# Import socket module 
import socket             
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

PSS = padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH,
)
with open( "client_private.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(), password=None
    )
# Create a socket object 
s = socket.socket()                
print ("Socket successfully created")

# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345                

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind(('', port))         
print ("socket binded to %s" %(port)) 

# put the socket into listening mode 
s.listen(5)     
print ("socket is listening") 
# Define the port on which you want to connect 
port = 12345                

# connect to the server on local computer 
#s.connect(('10.0.2.15', port)) 
#key auth
while True:
    c, addr = s.accept()
    print ('Got connection from', addr )
    request_to_sign = c.recv(1024)
    c.sendall(private_key.sign(request_to_sign, PSS, hashes.SHA256()))

    # receive data from the server and decoding to get the string.
    print (c.recv(1024).decode())
# close the connection
    while True:
        print("Enter a command")
        cmd = input()
    
        c.send(cmd.encode())
        print (c.recv(8024).decode())
        if cmd == "close":
            break


    c.close()
