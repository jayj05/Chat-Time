import socket 

HEADER = 16
# Choosing an unused port number to run the server on
PORT = 5050
# Format to decode the byte message sent from the client into a string
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    # Converting message into byte form
    message = msg.encode(FORMAT)
    # Getting the byte length of the message
    msg_length = len(message)
    # Converting the length of the users message into a string and then converting that string into byte format
    send_length = str(msg_length).encode(FORMAT)
    # Then we are finding out how much we need to pad the HEADER message so that it is the fixed length of 16 
    # (Fixed byte length - byte length of the message that will tell us how long the users message is)
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)
    
    receive()

def receive():
    msg_length = client.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    message = client.recv(msg_length).decode(FORMAT)
    print(message)

send("Hey")
send(DISCONNECT_MESSAGE)
