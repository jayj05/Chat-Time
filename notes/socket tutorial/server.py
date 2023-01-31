import socket
import threading 

HEADER = 16
# Choosing an unused port number to run the server on
PORT = 5050
# Getting local IP of the machine the server is running on 
SERVER = socket.gethostbyname(socket.gethostname())
# Creating an address for the socket to bind to 
ADDR = (SERVER, PORT)
# Format to decode the byte message sent from the client into a string
FORMAT = "utf-8"

DISCONNECT_MESSAGE = "!DISCONNECT"


# Creating the socket that will run on the server, choosing its type (INET) and how data moves through it (STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Binding the socket to our IP address and port
server.bind(ADDR)

# Handling the individual connection between the client and the server 
# Running in its own thread 
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True 
    while connected:
        """
        Message protocol: 

            The first message sent from the client to the server will always be a header with
            a fixed length that will contain the byte length of the next message from the client. 

            ex:
                The client wants to send a message "hello" which we will say is 5 bytes, so before
                that message is sent, a header such as "5      " which is padded to the fixed byte length 
                will be sent first. 
            
            Then the server will take that header and convert it into an integer 5 which will then be used to 
            give an accurate byte length of the message the client wants to send, which is "hello". 
        """

        msg_length = conn.recv(HEADER).decode(FORMAT)
        # Checking to see if the message sent from the client is valid 
        # When a connection is made a blank message is sent to the server to let it 
        # know that a new connection has been made 
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False 

            print(f"[{addr}] {msg}")
            send("Msg received", conn)
    
    conn.close()

def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    conn.send(send_length)
    conn.send(message)
    


# This function will allow the server to listen for new connections and pass those new connections to the 
# handle_client function which will run in a different thread
def start():
    # server is listening for connections
    server.listen()
    print(f"[LISTENING] serving is listening on {SERVER}")

    while True: 
        # This line will wait for a connection to the server 
        # conn = object that allows us to send information back to the connection 
        # addr = the port and IP of the connection 
        conn, addr = server.accept()

        # Taking that connection and passing it to a new thread
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        # This will tell us how many active connections we have because we make a new thread for every connection 
        # We subtract one because we will always have the main thread running which is the start function distributing new connections 
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()