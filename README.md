# C2 Reverse Shell
## Basic info
This is a simple python script to establish a reverse shell with root privledges on a machine.
It relies on mangled sudo permissions that allow strace to be run as sudo. Passing through commands to strace result in them being executed as root. 
It also contains public/private key authentication.
The way it works is the server.py file constantly pings the given host and port for a connection. When the client file runs and connects, the server provides output for the commands the client sends.

I largley based my original code off of this
 https://www.geeksforgeeks.org/python/socket-programming-python/ 
Though it was just used as a basline as I had no experience with the python socket library.

## Getting Started
Start by cloning the repo to the client machine. config.json contains everything needed to configure the program, so take a look and inputyour port and host ip (examples are in there already). 

Then, you need to create your public and private key. Run the below command in the repo folder.



(umask 077 && openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out client_private.pem && openssl pkey -in client_private.pem -pubout -out client_public.pem)







The keys need to lie in the same folder as the repo. They also need to be named as in the above command. 




Then, get the install.sh script and your public key onto the machine to backdoor. scp is an easy program to do this. An example is below.




scp client_public installserver.sh user@10.0.2.15:~/





Once both files are on the machine, run the below command.


chmod +x install.sh


And then run install.sh. 

install.sh will install the needed packages onto the machine, setup a systemd service for the backdoor, and install and unzip the repo. Put your public key into the unizpped repo. If for whatever reason the install.sh does not install the repo (github might be down), if you have the repo on another device/vm you can just scp the entire thing and put your public key into that.

Once that is completed, it should be good to go. The systemd service auto restarts on failure and restart, so it should stay up no matter what.

## Using the client.py script
Once the server.py systemd service is running, run the client.py script using the command below.


python client.py



That will wait for the server to connect. Once it does, just use it like a reguar terminal. Type in any command, hit enter, and the output will be send back from the machine. To exit, just control c. 
