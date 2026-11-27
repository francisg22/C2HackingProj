# Import socket module 
import socket             

# Create a socket object 
s = socket.socket()         

# Define the port on which you want to connect 
port = 12345                

# connect to the server on local computer 
s.connect(('10.0.2.15', port)) 


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
