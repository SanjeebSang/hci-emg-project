"""
Script to implement screen-guided training for EMG data collection.
Author: Christian Morrell (cmorrell@unb.ca)
Date created: 2023-11-03
"""
import os
import socket
import websockets
import datetime as dt
import time

import libemg
import pandas as pd
import asyncio


# Constants
SUBJECT_ID = 0
SGT = 'sgt'
VR = 'vr'
TRAINING_METHOD = VR
DATA_FOLDER = 'data'
IMAGE_FOLDER = 'images/'
SGT_FOLDER = os.path.join(DATA_FOLDER, SGT)
VR_FOLDER = os.path.join(DATA_FOLDER, VR)
SUBJECT_FOLDER = f'subject{SUBJECT_ID}'
TRAINING_FOLDER = SGT_FOLDER if TRAINING_METHOD == SGT else VR_FOLDER
OUTPUT_FOLDER = os.path.join(TRAINING_FOLDER, SUBJECT_FOLDER, '')
NUM_REPS = 5
REP_TIME = 5
TIME_BETWEEN_REPS = 1


CLIENT_DESCRIPTIONS = ['Hand Close', 'Hand Open', 'No Motion', 'Wrist Extension', 'Wrist Flexion']
SERVER_DESCRIPTIONS = ['No Motion', 'Hand Close', 'Hand Open', 'Wrist Flexion', 'Wrist Extension']

CHANGE_INDEX_LIST = [1, 2, 0, 4, 3]

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
PORT = 5006

# online_data_handler = libemg.data_handler.OnlineDataHandler()


def log(message):
    # Set to true to log trivial informationi for debuggin
    if False:
        print(message)

def log_imp(message):
    print(message)

async def run_server_in_loop(websocket, path):
    while True:
        received = await websocket.recv()
        log(f"Received: {received}")

        handle_message(received)
        sendMessage = f"Keep running!"

        await websocket.send(sendMessage)
        log(f"Sent: {sendMessage}")

def setup_socket_server():
    log_imp(f"Hostname: {IP} and Port: {PORT}")
    # online_data_handler.start_listening()

    start_server = websockets.serve(run_server_in_loop, IP, PORT)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def handle_message(message):
    if (message is None or len(message) == 0):
        log("None or zero length message.")

    parts = message.split("|")
    p0 = parts[0].strip()
    if p0 == "ExperimentHasStarted":
        print('start experiment')
    elif p0 == "ExperimentHasEnded":
        print('end experiment')
    elif p0 == "MovementInfo":
        params = parts[2].split(",")
        repNumber, movementNumber, time_in_millis = int(params[0].strip()), int(params[1].strip()), int(params[2].strip())
        startDateTime = dt.datetime.fromtimestamp(time_in_millis / 1000.0, tz=dt.timezone.utc)
        movementIndex = CHANGE_INDEX_LIST[movementNumber]
        
        vr_training(OUTPUT_FOLDER, repNumber, movementIndex)

def check_for_directory(directory, overwriting = True):
    print(f'Saving data to {directory}')
    if not os.path.exists(directory):
        # Create directory
        os.makedirs(directory)
    elif any(os.listdir(directory)) and overwriting:
        # Files already exist here
        print(f'Files already exist at {directory}. Terminating program.')
        exit()

def screen_guided_training(output_folder):
    # Launch screen-guided training (see https://libemg.github.io/libemg/emg_toolbox.html#module-libemg.screen_guided_training)
    sgt = libemg.screen_guided_training.ScreenGuidedTraining()
    # Download gestures if needed (see https://github.com/libemg/LibEMGGestures)
    gesture_ids = [1, 2, 3, 4, 5]   # corresponds to no motion, hand close / open, and wrist flexion / extension
    sgt.download_gestures(gesture_ids, IMAGE_FOLDER)
    # Create handler to read in data from MyoBand
    # online_data_handler = libemg.data_handler.OnlineDataHandler()
    # online_data_handler.start_listening()
    # Launch training window
    check_for_directory(output_folder)
    sgt.launch_training(online_data_handler, num_reps=NUM_REPS, rep_time=REP_TIME, rep_folder=IMAGE_FOLDER, output_folder=output_folder,
                        time_between_reps=TIME_BETWEEN_REPS, randomize=True)

    
def vr_training(output_folder, rep_number, class_number):
    rep_number -= 1
    print(rep_number, class_number)
    online_data_handler.raw_data.reset_emg()    # reset data
    
    # Do I need to keep track of reps or is that sent to me?
    filename = f'R_{rep_number}_C_{class_number}.csv'
    filepath = os.path.join(output_folder, filename)
    # online_data_handler = libemg.data_handler.OnlineDataHandler(file=filepath)
    # Start listening when socket says go
    # online_data_handler.start_listening()
    # Stop listening when timer is up
    time.sleep(5)   # wait for 5 seconds
    # online_data_handler.stop_listening()    # reset data
    data = online_data_handler.get_data() # could also just write to file using odh
    # # online_data_handler.stop_listening()
    # # Save data
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    

def main():
    libemg.streamers.myo_streamer()
    global online_data_handler
    online_data_handler = libemg.data_handler.OnlineDataHandler()
    online_data_handler.start_listening()
    check_for_directory(OUTPUT_FOLDER)
    if TRAINING_METHOD == SGT:
        screen_guided_training(OUTPUT_FOLDER)
    elif TRAINING_METHOD == VR:
        setup_socket_server()
    else:
        print('Unrecognized training method')
    online_data_handler.stop_listening()

if __name__ == '__main__':
    main()
