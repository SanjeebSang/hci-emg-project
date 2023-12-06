"""
Script created to analyze collected data and produce results.
Author: Christian Morrell (cmorrell@unb.ca)
Date created: 2023-12-01
"""
import os
import math
import pickle

import numpy as np
import libemg
from classification import parse_data, extract_features, CLASSIFIER, LABEL_NAMES
from training import SGT_FOLDER, VR_FOLDER, DATA_FOLDER
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def cross_validation(data_folder):
    if not os.path.isdir(data_folder):
        print(f'Skipping {data_folder} because it is not a directory.')
        return None
    n_splits = 5
    kf = KFold(n_splits=n_splits)
    reps = np.arange(n_splits)
    om = libemg.offline_metrics.OfflineMetrics()
    predictions = []
    true_labels = []
    for train_index, test_index in kf.split(reps):
        # Parse data
        train_reps = reps[train_index]
        test_reps = reps[test_index]
        train_windows, train_metadata = parse_data(data_folder, reps=list(train_reps))
        test_windows, test_metadata = parse_data(data_folder, reps=list(test_reps))
        
        # Extract features
        data_set = {
            'training_features': extract_features(train_windows),
            'training_labels': train_metadata['classes']
        }
        test_features = extract_features(test_windows)
        test_labels = test_metadata['classes']

        # Train model
        classifier = libemg.emg_classifier.EMGClassifier()
        classifier.fit(CLASSIFIER, data_set.copy())
        fold_predictions, _ = classifier.run(test_features)
        predictions.append(fold_predictions)
        true_labels.append(test_labels)

    predictions = np.concatenate(predictions)
    true_labels = np.concatenate(true_labels)
    metrics = om.extract_offline_metrics(['CA', 'CONF_MAT'], true_labels, predictions)
    return metrics['CA'], metrics['CONF_MAT']

def plot_confusion_matrix(confusion_matrix, title = ''):
    df = pd.DataFrame(confusion_matrix, index=LABEL_NAMES, columns=LABEL_NAMES)
    sns.heatmap(df, annot=True, fmt='.2f')
    plt.title(title)


def calculate_offline_metrics(data_folder):
    subject_folders = os.listdir(data_folder)
    accuracies = []
    confusion_matrices = []
    for subject_folder in subject_folders:
        folder_path = os.path.join(data_folder, subject_folder, '')
        result = cross_validation(folder_path)
        if result is not None:
            subject_accuracy, subject_confusion_matrix = result
            accuracies.append(subject_accuracy)
            confusion_matrices.append(subject_confusion_matrix)
    accuracies = np.array(accuracies).reshape(-1, 1)
    confusion_matrices = np.array(confusion_matrices)
    mean_accuracy = accuracies.mean()
    mean_confusion_matrix = confusion_matrices.mean(axis=0)

    # Display results
    print(f'Mean accuracy: {mean_accuracy}')

    return accuracies, mean_confusion_matrix


def calculate_throughput(subject_data):
    """Leveraged https://github.com/libemg/LibEMG_Isofitts_Showcase to inform online Fitts' metric calculation."""
    throughput = []
    trials = np.unique(subject_data['trial_number'])
    cursor_data = np.array(subject_data['cursor_position'])
    target_data = np.array(subject_data['goal_circle'])
    time_data = np.array(subject_data['global_clock'])
    for trial in trials:
        trial_indices = np.where(subject_data['trial_number'] == trial)[0]
        trial_start_idx = trial_indices[0]
        trial_cursor_data = cursor_data[trial_start_idx][0:2]
        trial_target_data = target_data[trial_start_idx][0:2]
        distance = math.dist(trial_cursor_data, trial_target_data)
        target_width = target_data[trial_start_idx][2]
        index_difficulty = math.log2(distance / target_width + 1)
        time = time_data[trial_indices[-1]] - time_data[trial_indices[0]]
        throughput.append(index_difficulty / time)
    
    return np.mean(throughput)


def calculate_efficiency(subject_data):
    """Leveraged https://github.com/libemg/LibEMG_Isofitts_Showcase to inform online Fitts' metric calculation."""
    efficiency = []
    trials = np.unique(subject_data['trial_number'])
    cursor_data = np.array([x[:2] for x in subject_data['cursor_position']])
    target_data = np.array([x[:2] for x in subject_data['goal_circle']])
    for trial in trials:
        trial_indices = np.where(subject_data['trial_number'] == trial)[0]
        trial_start_idx = trial_indices[0]
        distance_travelled = np.sum([math.dist(cursor_data[trial_indices[idx]], cursor_data[trial_indices[idx - 1]]) for idx in range(1, len(trial_indices))])
        fastest_path = math.dist(cursor_data[trial_start_idx], target_data[trial_start_idx])
        efficiency.append(fastest_path / distance_travelled)
    
    return np.mean(efficiency)

def calculate_overshoots(subject_data):
    """Leveraged https://github.com/libemg/LibEMG_Isofitts_Showcase to inform online Fitts' metric calculation."""
    def cursor_in_target(cursor, target):
        cursor_radius = cursor[2] / 2
        target_radius = target[2] / 2
        return math.dist(cursor[:2], target[:2]) < cursor_radius + target_radius
    overshoots = 0
    trials = np.unique(subject_data['trial_number'])
    cursor_data = np.array(subject_data['cursor_position'])
    target_data = np.array(subject_data['goal_circle'])
    for trial in trials:
        trial_indices = np.where(subject_data['trial_number'] == trial)[0]
        trial_cursor_data = cursor_data[trial_indices]
        trial_target_data = target_data[trial_indices]
        samples_in_target = [cursor_in_target(cursor, target) for cursor, target in zip(trial_cursor_data, trial_target_data)]
        for idx in range(1, len(samples_in_target)):
            if samples_in_target[idx - 1] == True and samples_in_target[idx] == False:
                # They were in the target then went out
                overshoots += 1
    return overshoots


def read_pickle_file(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

def calculate_online_metrics(data_folder):
    def find_pickle_file(path):
        try:
            for filename in os.listdir(path):
                if filename.endswith('.pkl'):
                    return os.path.join(path, filename)
        except NotADirectoryError:
            pass
        return None
    throughputs = []
    efficiencies = []
    overshoots = []
    subject_folders = os.listdir(data_folder)
    for subject_folder in subject_folders:
        folder_path = os.path.join(data_folder, subject_folder, '')
        filename = find_pickle_file(folder_path)
        if filename is not None:
            log = read_pickle_file(filename)
            throughputs.append(calculate_throughput(log))
            efficiencies.append(calculate_efficiency(log))
            overshoots.append(calculate_overshoots(log))
    throughputs = np.array(throughputs).reshape(-1, 1)
    efficiencies = np.array(efficiencies).reshape(-1, 1)
    overshoots = np.array(overshoots).reshape(-1, 1)
    return throughputs, efficiencies, overshoots

def combine_metrics(method, *args):
    metrics = []
    for arg in args:
        metrics.extend(arg)
    metrics = np.concatenate(metrics, axis=1)
    method_labels = np.array([method] * len(metrics)).reshape(-1, 1)
    metrics = np.concatenate((method_labels, metrics), axis=1)
    return metrics
        

def main():
    sgt_offline_metrics = calculate_offline_metrics(SGT_FOLDER)
    sgt_online_metrics = calculate_online_metrics(SGT_FOLDER)
    sgt_metrics = combine_metrics('sgt', sgt_offline_metrics[0:1], sgt_online_metrics)
    # vr_metrics = np.copy(sgt_metrics)
    # vr_metrics[:, 0] = 'vr'
    vr_offline_metrics = calculate_offline_metrics(VR_FOLDER)
    vr_online_metrics = calculate_online_metrics(VR_FOLDER)
    vr_metrics = combine_metrics('vr', vr_offline_metrics[0:1], vr_online_metrics)
    
    # Show confusion matrices
    fig = plt.figure()
    plt.subplot(1, 2, 1)
    plot_confusion_matrix(sgt_offline_metrics[1], title=f'SGT (Accuracy: {float(sgt_offline_metrics[0]) * 100:.2f}%)')
    plt.subplot(1, 2, 2)
    plot_confusion_matrix(vr_offline_metrics[1], title=f'VR (Accuracy: {float(vr_offline_metrics[0]) * 100:.2f}%)')
    fig.suptitle('Mean Confusion Matrices')
    plt.tight_layout()
    plt.show()
    
    # add survey results

    # Save data
    all_metrics = np.concatenate((sgt_metrics, vr_metrics), axis=0)
    columns = ['method', 'accuracy', 'throughput', 'efficiency', 'overshoots']
    df = pd.DataFrame(all_metrics, columns=columns)
    df.to_csv(os.path.join(DATA_FOLDER, 'results.csv'))



if __name__ == '__main__':
    main()
