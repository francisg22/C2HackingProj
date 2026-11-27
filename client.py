# Import socket module 
import socket             
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

PSS = padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH,
)
with open(os.path.join(APP_DIR, "client_private.pem"), "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(), password=None
    )
# Create a socket object 
s = socket.socket()         

# Define the port on which you want to connect 
port = 12345                

# connect to the server on local computer 
s.connect(('10.0.2.15', port)) 
#key auth
request_to_sign = s.recv(1024)
s.sendall(private_key.sign(request_to_sign, PSS, hashes.SHA256()))

# receive data from the server and decoding to get the string.
print (s.recv(1024).decode())
# close the connection
while True:
    print("Enter a command")
    cmd = input()
    
    s.send(cmd.encode())
    print (s.recv(8024).decode())
    if cmd == "close":
        break


s.close()
