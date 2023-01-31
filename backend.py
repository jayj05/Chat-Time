from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Initialized app 
app = Flask(__name__)
# Initialized socket
socketio = SocketIO(app)

# Landing page 
@app.route("/")
def home():
    return render_template("index.html")

# Chat room
@app.route("/chat")
def chatroom():
    return render_template("chatroom.html")

# Receiving confirmation of client connection to socket 
@socketio.on('connection')
def handle_conn(data):
    print('received message: ' + data)

# Taking message input from individual client and broadcasting to all clients
@socketio.on("message")
def handle_message(message):
    # All clients will receive message on their message event
    emit("message", message, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, host="0.0.0.0")