import SocketClient from "./socket-client";


export default class ExperimentMovementNotifier {

    ip = '127.0.0.1'
    socketClient = null;
    port = '5006'

    constructor(isAudit = false) {
        // this.ip = process.env.REACT_APP_SOCKET_IP;
        // this.port = process.env.REACT_APP_SOCKET_PORT;
        this.socketClient = new SocketClient(this.ip, this.port);
        this.isAudit = isAudit;
    }

    notify(repNumber, movNumber, timeInMillis) {
        setTimeout(() => this.notifyServer(repNumber, movNumber, timeInMillis), 150);   
    }

    notifyExperimentHasStarted(timeInMillis) {
        if (!this.isAudit) {
            let message = `ExperimentHasStarted | StartTime | ${timeInMillis}`;
            this.socketClient.send(message);
        }
    }

    notifyServer(repNumber, movNumber, timeInMillis) {
        if (!this.isAudit) {
            let message = `MovementInfo | Rep, Movement Number, startTimeInFuture | ${repNumber}, ${movNumber}, ${timeInMillis}`;
            this.socketClient.send(message);
        }
    }

    notifyExperimentHasEnded(timeInMillis) {
        if (!this.isAudit) {
            let message = `ExperimentHasEnded | EndTime | ${timeInMillis}`;
            this.socketClient.send(message);
        }
    }
}
