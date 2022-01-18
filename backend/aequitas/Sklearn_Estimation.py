import joblib
import config as config
import time
import random
import numpy as np
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

num_trials = 100
samples = 100

classifier_name = config.classifier_name
model = joblib.load(f'TrainedModels/{classifier_name}')
input_bounds = config.input_bounds
num_params = config.num_params
sensitive_param_idx = config.sensitive_param_idx

def get_random_input():
    x = []
    for i in range(num_params):
        random.seed(time.time())
        x.append(random.randint(input_bounds[i][0], input_bounds[i][1]))

    x[sensitive_param_idx] = 0
    return x

def evaluate_input(inp):
    inp0 = [int(i) for i in inp]
    inp1 = [int(i) for i in inp]

    inp0[sensitive_param_idx] = 0
    inp1[sensitive_param_idx] = 1

    inp0 = np.asarray(inp0)
    inp0 = np.reshape(inp0, (1, -1))

    inp1 = np.asarray(inp1)
    inp1 = np.reshape(inp1, (1, -1))

    out0 = model.predict(inp0)
    out1 = model.predict(inp1)

    return (abs(out0 + out1) == 0)

def get_estimate_arrray():
    estimate_array = []
    rolling_average = 0.0
    for i in range(num_trials):
        disc_count = 0
        total_count = 0
        for j in range(samples):
            total_count = total_count + 1
            if(evaluate_input(get_random_input())):
                disc_count = disc_count + 1

        estimate = float(disc_count)/total_count
        rolling_average = ((rolling_average * i) + estimate)/(i + 1)
        estimate_array.append(estimate)
        print(estimate, rolling_average)
    return estimate_array

def run():
    print("Getting Estimate array")
    arr = get_estimate_arrray()
    print("Estimate is " + str(np.mean(arr) * 100) + "%")
    return str(np.mean(arr) * 100)