import joblib
import time
import random
import numpy as np
from .Dataset import Dataset
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

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

def get_estimate_array(dataset: Dataset, model, threshold, num_trials, samples):
    estimate_array = []
    rolling_average = 0.0
    for i in range(num_trials):
        disc_count = 0
        for j in range(samples):
            if(evaluate_input(get_random_input(dataset), model, dataset, threshold)): # if the input is biased
                disc_count += 1

        estimate = float(disc_count)/samples # average biasedness
        rolling_average = ((rolling_average * i) + estimate)/(i + 1)
        estimate_array.append(estimate)
        print(estimate, rolling_average)
    return estimate_array

def get_fairness_estimation(dataset: Dataset, input_pkl_name, threshold, num_trials, samples):
    model = joblib.load(input_pkl_name)
    arr = get_estimate_array(dataset, model, threshold, num_trials, samples)
    print("final biasedness estimate: " + str(np.mean(arr) * 100))
    return str(np.mean(arr) * 100) 
