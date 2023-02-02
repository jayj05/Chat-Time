// Initializing socket connection on client side
const socket = io("ws://"); // SERVER IP ADDRESS 

// Automatically triggered when connection is made 
socket.on("connect", () => {
        socket.emit("connection", socket.id + " connected");
});

// Receiving message from server and then making it visible on screen
socket.on("message", (text) => {
        const message_bubble = document.createElement("div")
        message_bubble.style.setProperty("height", "30px");
        message_bubble.style.setProperty("width", "70px");
        message_bubble.style.setProperty("background-color", "rgb(51, 189, 85)");
        message_bubble.style.setProperty("position", "absolute");
        message_bubble.style.setProperty("left", "40px");
        message_bubble.innerHTML = text;
        document.getElementById("feed").appendChild(message_bubble);
});

// Sending client input when send button is clicked 
document.getElementById("sender").onclick = () => {
    const text = document.querySelector("input").value;
    socket.emit("message", text);
}
