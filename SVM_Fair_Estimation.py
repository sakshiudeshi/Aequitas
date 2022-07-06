import joblib
import config
import time
import random
import numpy as np
import utils as ut
import loss_funcs as lf

num_trials = 100
samples = 1000

# classifier_name = config.classifier_name
# model = joblib.load(classifier_name)

sensitive_param_idx = config.sensitive_param_idx_idx
sensitive_param_name = config.sensitive_param_idx_name
cov = 0

X = []
Y = []
i = 0
sensitive = {}
sens = []
dataset = config.original_inputs
with open(dataset, "r") as ins:
    for line in ins:
        line = line.strip()
        line1 = line.split(',')
        if (i == 0):
            i += 1
            continue
        L = list(map(int, line1[:-1]))
        sens.append(L[sensitive_param_idx])
        # L[sens_arg-1]=-1
        X.append(L)

        if (int(line1[-1]) == 0):
            Y.append(-1)
        else:
            Y.append(1)

X = np.array(X, dtype=float)
Y = np.array(Y, dtype=float)
sensitive[sensitive_param_name] = np.array(sens, dtype=float)
loss_function = lf._logistic_loss
sep_constraint = 0
sensitive_attrs = [sensitive_param_name]
sensitive_attrs_to_cov_thresh = {sensitive_param_name: cov}

gamma = None

model = ut.train_model(X, Y, sensitive, loss_function, 1, 0, sep_constraint, sensitive_attrs, sensitive_attrs_to_cov_thresh,
                   gamma)


input_bounds = config.input_bounds
num_params = config.num_params
sensitive_param_idx = config.sensitive_param_idx_idx

def get_random_input():
    x = []
    for i in range(params):
        random.seed(time.time())
        x.append(random.randint(input_bounds[i][0], input_bounds[i][1]))

    x[sensitive_param_idx] = 0
    return x


def evaluate_input(inp):
    inp0 = [int(i) for i in inp]
    inp1 = [int(i) for i in inp]

    inp0[sensitive_param_idx] = 0
    inp1[sensitive_param_idx] = 1
    out0 = np.sign(np.dot(model, inp0))
    out1 = np.sign(np.dot(model, inp1))
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

print("Getting Estimate array")

arr = get_estimate_arrray()

print("Estimate is " + str(np.mean(arr)* 100) + "%")