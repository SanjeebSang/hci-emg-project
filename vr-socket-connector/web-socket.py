import asyncio
import websockets
import socket
import datetime as dt
import time

##############################################################################
CLIENT_DESCRIPTIONS = ['Hand Close', 'Hand Open', 'No Motion', 'Wrist Extension', 'Wrist Flexion']
SERVER_DESCRIPTIONS = ['No Motion', 'Hand Close', 'Hand Open', 'Wrist Flexion', 'Wrist Extension']

CHANGE_INDEX_LIST = [1, 2, 0, 4, 3]

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
PORT = 5006

async def run_server_in_loop(websocket, path):
    while True:
        received = await websocket.recv()
        log(f"Received: {received}")

        handleMessage(received)
        sendMessage = f"Keep running!"

        await websocket.send(sendMessage)
        log(f"Sent: {sendMessage}")

def setup_socket_server():
    log_imp(f"Hostname: {IP} and Port: {PORT}")

    start_server = websockets.serve(run_server_in_loop, IP, PORT)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def handleMessage(message):
    if (message is None or len(message) == 0):
        log("None or zero length message.")

    parts = message.split("|")
    p0 = parts[0].strip()
    if p0 == "ExperimentHasStarted":
        onExperimentStart()
    elif p0 == "ExperimentHasEnded":
        onExperimentHasEnded()
    elif p0 == "MovementInfo":
        params = parts[2].split(",")
        repNumber, movementNumber, time_in_millis = int(params[0].strip()), int(params[1].strip()), int(params[2].strip())
        startDateTime = dt.datetime.fromtimestamp(time_in_millis / 1000.0, tz=dt.timezone.utc)
        movementIndex = CHANGE_INDEX_LIST[movementNumber]
        onMovementToStart(repNumber, movementIndex)


def onExperimentStart():
    log("EXPERIMENT START: ")


def onExperimentHasEnded():
    log(f"EXPERIMENT ENDED: ")
################################################################################


def onMovementToStart(repNumber, movementNumber):
    log_imp(f"RECORDING NOW: {repNumber}, {movementNumber}, Description: {SERVER_DESCRIPTIONS[movementNumber]}")
    ###############################################################
    ## Use this repNumber and movementNumber to store the VR data
    ###############################################################


def log(message):
    # Set to true to log trivial informationi for debuggin
    if False:
        print(message)

def log_imp(message):
    print(message)

if __name__ == '__main__':
    setup_socket_server()



