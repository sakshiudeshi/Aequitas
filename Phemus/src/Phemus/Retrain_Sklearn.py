import joblib
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import LabelEncoder

# from sklearn.tree import DecisionTreeClassifier
# import pandas as pd
# from dataclasses import dataclass

from .Dataset import Dataset
le=LabelEncoder()
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

def extract_inputs(dataset: Dataset, input_csv_dir):
    col_to_be_predicted_idx = dataset.col_to_be_predicted_idx

    df = open(input_csv_dir).readlines()
    
    X = []
    Y = []
    i = 0
    neg_count = 0
    pos_count = 0
    
    for line in df:
        if (i == 0): # first row, col name, skip
            i += 1
            continue
        line = line.strip().split(",")
        L = list(map(int, line[:col_to_be_predicted_idx] + line[col_to_be_predicted_idx + 1:])) # exclude col to be predicted 
        X.append(L)
        if (int(line[-1]) == -1):
            Y.append(-1)
            neg_count = neg_count + 1
        else:
            Y.append(1)
            pos_count = pos_count + 1

    return X, Y

def extract_original(dataset: Dataset):
    X, Y = extract_inputs(dataset, dataset.dataset_dir)
    X_original = np.array(X)
    Y_original = np.array(Y)
    return X, Y, X_original, Y_original

def retrain(model, X_original, Y_original, X_additional, Y_additional):
    X = np.concatenate((X_original, X_additional), axis = 0)
    Y = np.concatenate((Y_original, Y_additional), axis = 0)

    model.fit(X, Y)
    return model

def get_random_input(dataset: Dataset):
    num_params = dataset.num_param
    input_bounds = dataset.input_bounds
    sensitive_param_idx = dataset.sensitive_param_idx

    x = []
    for i in range(num_params):
        random.seed(time.time())
        x.append(random.randint(input_bounds[i][0], input_bounds[i][1]))

    x[sensitive_param_idx] = 0
    return x

def evaluate_input(inp, model, dataset: Dataset):
    sensitive_param_idx = dataset.sensitive_param_idx

    inp0 = [int(i) for i in inp]
    inp1 = [int(i) for i in inp]

    for i in range(dataset.input_bounds[sensitive_param_idx][1] + 1):
        for j in range(dataset.input_bounds[sensitive_param_idx][1] + 1):
            if i < j: 
                inp0 = [int(k) for k in inp]
                inp1 = [int(k) for k in inp]

                inp0[sensitive_param_idx] = i
                inp1[sensitive_param_idx] = j

                inp0 = np.asarray(inp0)
                inp0 = np.reshape(inp0, (1, -1))

                inp1 = np.asarray(inp1)
                inp1 = np.reshape(inp1, (1, -1))

                out0 = model.predict(inp0)
                out1 = model.predict(inp1)
            
                if abs(out1 + out0) == 0:
                    return abs(out1 + out0) == 0
    # return (abs(out0 - out1) > threshold)
    # for binary classification, we have found that the
    # following optimization function gives better results
    return False

def get_estimate(model, dataset: Dataset, num_trials, samples):
    estimate_array = []
    rolling_average = 0.0
    for i in range(num_trials):
        disc_count = 0
        total_count = 0
        for j in range(samples):
            total_count = total_count + 1
            if(evaluate_input(get_random_input(dataset), model, dataset)):
                disc_count = disc_count + 1

        estimate = float(disc_count)/total_count
        rolling_average = ((rolling_average * i) + estimate)/(i + 1)
        estimate_array.append(estimate)

    print("Current biasedness:", np.average(estimate_array))
    return np.average(estimate_array)


def retrain_search(model, dataset: Dataset, retrain_csv_dir, num_trials, samples):
    current_model = model
    current_estimate = get_estimate(model, dataset, num_trials, samples)
    fairness = [] 
    fairness.append(current_estimate)
    
    X, Y, X_original, Y_original = extract_original(dataset)
    X_retrain, Y_retrain = extract_inputs(dataset, retrain_csv_dir)
    retrain_len = len(X_retrain)
    for i in range(7):
        X_additional = []
        Y_additional = []
        retraining_input_set = set()
        additive_percentage = random.uniform(pow(2, i), pow(2, i + 1))
        num_inputs_for_retrain = int((additive_percentage * len(X))/100)

        if (num_inputs_for_retrain > retrain_len):
            raise ValueError('Number of inputs in retraining are not enough. Please add more inputs')

        while (len(retraining_input_set) < num_inputs_for_retrain):
            retraining_input_set.add(random.randint(0, retrain_len - 1))

        for i in retraining_input_set:
            X_additional.append(X_retrain[i])
            Y_additional.append(Y_retrain[i])
        retrained_model = retrain(current_model, X_original, Y_original, np.array(X_additional), np.array(Y_additional))
        retrained_estimate = get_estimate(retrained_model, dataset, num_trials, samples)
        fairness.append(retrained_estimate)
        if (retrained_estimate > current_estimate):
            return current_model
        else:
            current_model = retrained_model
            current_estimate = retrained_estimate
            del retrained_estimate
            del retrained_model
    return current_model, fairness

def retrain_sklearn(dataset: Dataset, input_pkl_dir, retrain_csv_dir, improved_pkl_dir, plot_dir, num_trials, samples):
    original_model = joblib.load(input_pkl_dir)
    improved_model, fairness= retrain_search(original_model, dataset, retrain_csv_dir, num_trials, samples)
    # file_to_save_model = config.improved_classfier_name

    joblib.dump(improved_model, improved_pkl_dir)

    # display fairness improvement 
    plt.plot(fairness)
    plt.xticks(np.arange(0, len(fairness), 1.0))
    plt.xlabel("Number of Iterations")
    plt.ylabel("Percentage of Biased Outputs")
    plt.savefig(plot_dir)

