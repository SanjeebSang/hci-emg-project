"""
Script to display real-time classification using previous data.
Author: Christian Morrell (cmorrell@unb.ca)
Date created: 2023-11-03
"""
import libemg

from training import OUTPUT_FOLDER


WINDOW_SIZE = 40
WINDOW_INCREMENT = 10
FEATURES    = ["MAV","ZC","SSC","WL"]
CLASSIFIER = "SVM"
LABEL_NAMES = ['Hand Close', 'Hand Open', 'No Motion', 'Wrist Extension', 'Wrist Flexion']

def parse_data(data_folder, reps = None):
    # Set parsing arguments
    classes_values = [str(idx) for idx in range(5)] # determine how many classes to consider
    reps_values = [str(idx) for idx in range(5)]
    classes_regex = libemg.utils.make_regex(left_bound='_C_', right_bound='.csv', values=classes_values)
    reps_regex = libemg.utils.make_regex(left_bound='/R_', right_bound='_C_', values=reps_values)
    filename_map = {
        'classes': classes_values,
        'classes_regex': classes_regex,
        'reps': reps_values,
        'reps_regex': reps_regex
    }
    
    # Create offline data handler
    offline_data_handler = libemg.data_handler.OfflineDataHandler()
    offline_data_handler.get_data(folder_location=data_folder, filename_dic=filename_map)

    if reps is not None:
        offline_data_handler = offline_data_handler.isolate_data(key='reps', values=reps)
    
    # Extract features
    windows, metadata = offline_data_handler.parse_windows(WINDOW_SIZE, WINDOW_INCREMENT)
    return windows, metadata

def extract_features(windows):
    feature_extractor = libemg.feature_extractor.FeatureExtractor()
    feature_set = feature_extractor.extract_features(FEATURES, windows)
    return feature_set


def create_offline_classifier(data_folder, reps = None):
    windows, metadata = parse_data(data_folder, reps=reps)
    feature_set = extract_features(windows)
    # Create offline EMG classifier
    offline_classifier = libemg.emg_classifier.EMGClassifier()
    feature_map = {
        'training_features': feature_set,
        'training_labels': metadata['classes']
    }
    offline_classifier.fit(CLASSIFIER, feature_dictionary=feature_map)
    return offline_classifier


def create_online_classifier(offline_classifier, output_format = 'predictions'):
    libemg.streamers.myo_streamer()
    online_data_handler = libemg.data_handler.OnlineDataHandler()
    online_data_handler.start_listening()
    online_classifier = libemg.emg_classifier.OnlineEMGClassifier(
        offline_classifier, WINDOW_SIZE, WINDOW_INCREMENT, online_data_handler, FEATURES,
        std_out=True, output_format=output_format
    )
    return online_classifier


def main():
    offline_classifier = create_offline_classifier(OUTPUT_FOLDER)
    
    # Create online classifier
    online_classifier = create_online_classifier(offline_classifier, output_format='probabilities')
    online_classifier.run(block=False)  # don't block main thread so script will continue
    
    # Visualize classifier
    online_classifier.visualize(legend=LABEL_NAMES)


if __name__ == '__main__':
    main()
