import joblib
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import LabelEncoder
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
    neg_count = 0
    pos_count = 0
    
    for i, line in enumerate(df):
        if (i == 0): # first row, col name, skip
            continue
        line = line.strip().split(",")
        L = list(map(int, line[:col_to_be_predicted_idx] + line[col_to_be_predicted_idx + 1:])) # exclude col to be predicted 
        X.append(L)
        if (int(line[col_to_be_predicted_idx]) == 0): # this is where the y column needs to exist
            Y.append(-1)
            neg_count = neg_count + 1
        else:
            Y.append(1)
            pos_count = pos_count + 1

    return X, Y

def retrain(model, X_original, Y_original, X_additional, Y_additional):
    X = np.concatenate((X_original, X_additional), axis = 0)
    Y = np.concatenate((Y_original, Y_additional), axis = 0)

    model.fit(X, Y)
    return model

def get_random_input(dataset: Dataset):
    sensitive_param_idx = dataset.sensitive_param_idx
    random.seed(time.time())
    x = [random.randint(low,high) for [low, high] in dataset.input_bounds]
    x[sensitive_param_idx] = 0
    return x

def evaluate_input(inp, model, dataset: Dataset, threshold):
    sensitive_param_idx = dataset.sensitive_param_idx
    inp0 = [int(k) for k in inp]
    sensValue = inp0[sensitive_param_idx]
    inp0 = np.asarray(inp0)
    inp0 = np.reshape(inp0, (1, -1))
    inp0delY = np.delete(inp0, [dataset.col_to_be_predicted_idx])
    inp0delY = np.reshape(inp0delY, (1, -1))
    out0 = model.predict(inp0delY)

    for i in range(dataset.input_bounds[sensitive_param_idx][1] + 1):
        if i != sensValue:
            inp1 = [int(k) for k in inp]
            inp1[sensitive_param_idx] = i

            inp1 = np.asarray(inp1)
            inp1 = np.reshape(inp1, (1, -1))

            # drop y column here 
            inp1delY = np.delete(inp1, [dataset.col_to_be_predicted_idx])
            inp1delY = np.reshape(inp1delY, (1, -1))

            out1 = model.predict(inp1delY)
            if abs(out1 - out0) > threshold: # different results came out, therefore it is biased
                return True
    # return (abs(out0 - out1) > threshold)
    # for binary classification, we have found that the
    # following optimization function gives better results
    return False

def get_estimate(model, dataset: Dataset, threshold, num_trials, samples):
    estimate_array = []
    rolling_average = 0.0
    for i in range(num_trials):
        disc_count = 0
        for j in range(samples):
            if(evaluate_input(get_random_input(dataset), model, dataset, threshold)):
                disc_count += 1

        estimate = float(disc_count)/samples
        rolling_average = ((rolling_average * i) + estimate)/(i + 1)
        estimate_array.append(estimate)

    print("Current biasedness:", np.average(estimate_array))
    return np.average(estimate_array)


def retrain_search(model, dataset: Dataset, retrain_csv_dir, threshold, num_trials, samples):
    current_model = model
    current_estimate = get_estimate(model, dataset, threshold, num_trials, samples)
    fairness = [] 
    fairness.append(current_estimate)
    
    X, Y = extract_inputs(dataset, dataset.dataset_dir)
    X_original = np.array(X)
    Y_original = np.array(Y)
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
        retrained_estimate = get_estimate(retrained_model, dataset, threshold, num_trials, samples)
        fairness.append(retrained_estimate)
        if (retrained_estimate > current_estimate):
            return current_model, fairness[:-1] # exclude the last "increased bias"
        else:
            current_model = retrained_model
            current_estimate = retrained_estimate
            del retrained_estimate
            del retrained_model
    return current_model, fairness

def retrain_sklearn(dataset: Dataset, input_pkl_dir, retrain_csv_dir, improved_pkl_dir, plot_dir, threshold, num_trials, samples):
    original_model = joblib.load(input_pkl_dir)
    improved_model, fairness= retrain_search(original_model, dataset, threshold, retrain_csv_dir, num_trials, samples)
    joblib.dump(improved_model, improved_pkl_dir)

    # display fairness improvement 
    plt.plot(fairness)
    plt.xticks(np.arange(0, len(fairness), 1.0))
    plt.xlabel("Number of Iterations")
    plt.ylabel("Percentage of Biased Outputs")
    plt.savefig(plot_dir)

