import { SocketIpAddress, SocketPort } from '../configs';

const PORT = SocketPort;
const IP = SocketIpAddress;


function log(message, error=false) {
    console.log(`IP: ${IP}, Post: ${PORT}, ${message}`);
}


function setup() {
    let socket = new WebSocket(`ws://${IP}:${PORT}`);
    socket.onopen = function(e) {
        log("[open] Connection established");
        log("Sending to server");
    };

    socket.onmessage = function(event) {
        log(`[message] Data received from server: ${event.data}`);
    };

    socket.onclose = function(event) {
    if (event.wasClean) {
        log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        log('[close] Connection died', true);
    }
    };

    socket.onerror = function(error) {
        log(`[error]`, true);
    };

    return socket;
}


export default class SocketClient {
    socket = null;

    constructor() {
        try {
            this.socket = setup();
        }
        catch (err) {
            console.log("Error while setting up socket.");
        }
    }

    send(message) {
        try {
            this.socket.send(`${message}`);
            console.log(`Socket Message: ${message}`);
        } catch (err) {
            console.log(`Error while sending socket message!!`);
        }
    }

}