from __future__ import division
from random import seed, shuffle
import random
import math
import os
from collections import defaultdict
from sklearn import svm
import os,sys
#import urllib2
sys.path.insert(0, './fair_classification/') # the code for fair classification is in this directory
import numpy as np
import loss_funcs as lf # loss funcs that can be optimized subject to various constraints
import random
import time
from scipy.optimize import basinhopping
import config
import joblib
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

random.seed(time.time())
start_time = time.time()

init_prob = 0.5
num_params = config.num_params
direction_probability = [init_prob] * num_params
direction_probability_change_size = 0.001

sensitive_param_idx = config.sensitive_param_idx
sensitive_param_name = config.sensitive_param_name
cov = 0

perturbation_unit = config.perturbation_unit

threshold = config.threshold

global_disc_inputs = set()
global_disc_inputs_list = []

local_disc_inputs = set()
local_disc_inputs_list = []

tot_inputs = set()

global_iteration_limit = 1000
local_iteration_limit = 1000

input_bounds = config.input_bounds
classifier_name = config.classifier_name

model = joblib.load(classifier_name)

class Local_Perturbation(object):

    def __init__(self, stepsize=1):
        self.stepsize = stepsize

    def __call__(self, x):
        s = self.stepsize
        val = np.random.choice(range(num_params))
        act = [-1, 1]
        x[val] = x[val] + random.choice(act)

        x[val] = max(input_bounds[val][0], x[val])
        x[val] = min(input_bounds[val][1], x[val])

        return x


class Global_Discovery(object):
    def __init__(self, stepsize=1):
        self.stepsize = stepsize

    def __call__(self, x):
        s = self.stepsize
        for i in range(num_params):
            random.seed(time.time())
            x[i] = random.randint(input_bounds[i][0], input_bounds[i][1])

        x[sensitive_param_idx] = 0
        # print(x)
        return x

def evaluate_global(inp):
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

    tot_inputs.add(tuple(map(tuple, inp0)))

    if (abs(out0 + out1) == 0 and tuple(map(tuple, inp0)) not in global_disc_inputs):
        global_disc_inputs.add(tuple(map(tuple, inp0)))
        global_disc_inputs_list.append(inp0.tolist()[0])

    return not abs(out0 - out1) > threshold
    # for binary classification, we have found that the
    # following optimization function gives better results
    # return abs(out1 + out0)


def evaluate_local(inp):
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

    tot_inputs.add(tuple(map(tuple, inp0)))

    if (abs(out0 + out1) == 0 and (tuple(map(tuple, inp0)) not in global_disc_inputs)
        and (tuple(map(tuple, inp0)) not in local_disc_inputs)):
        local_disc_inputs.add(tuple(map(tuple, inp0)))
        local_disc_inputs_list.append(inp0.tolist()[0])

    return not abs(out0 - out1) > threshold
    # for binary classification, we have found that the
    # following optimization function gives better results
    # return abs(out1 + out0)


# initial_input = [7, 4, 26, 1, 4, 4, 0, 0, 0, 1, 5, 73, 1]
initial_input = [random.randint(low,high) for [low, high] in input_bounds]
minimizer = {"method": "L-BFGS-B"}

global_discovery = Global_Discovery()
local_perturbation = Local_Perturbation()

basinhopping(evaluate_global, initial_input, stepsize=1.0, take_step=global_discovery, minimizer_kwargs=minimizer,
             niter=global_iteration_limit)

print("Finished Global Search")
print("Percentage discriminatory inputs - " + str(float(len(global_disc_inputs_list)
                                                        + len(local_disc_inputs_list)) / float(len(tot_inputs))*100))
print()
print("Starting Local Search")

for inp in global_disc_inputs_list:
    basinhopping(evaluate_local, inp, stepsize=1.0, take_step=local_perturbation, minimizer_kwargs=minimizer,
                 niter=local_iteration_limit)
    print("Percentage discriminatory inputs - " + str(float(len(global_disc_inputs_list) + len(local_disc_inputs_list))
                                                      / float(len(tot_inputs))*100))

print()
print("Local Search Finished")
print("Percentage discriminatory inputs - " + str(float(len(global_disc_inputs_list) + len(local_disc_inputs_list))
                                                  / float(len(tot_inputs))*100))

print()
print("Total Inputs are " + str(len(tot_inputs)))
print("Number of discriminatory inputs are " + str(len(global_disc_inputs_list)+len(local_disc_inputs_list)))

# save the discriminatory inputs to file
original_dataset_name = config.original_inputs.split(".")[0]
retraining_example_filename = original_dataset_name + "_Retraining_Dataset.csv"
with open(retraining_example_filename, 'w') as f:
    f.write(",".join(config.column_names) + "\n") # write the column names on top first
    for input in global_disc_inputs_list + local_disc_inputs_list:
        f.write(",".join([str(num) for num in input] + [str(-1)]) + "\n") # attach the -1 at the end for the "col_to_be_predicted"