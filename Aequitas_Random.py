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
import utils as ut
import numpy as np
import loss_funcs as lf # loss funcs that can be optimized subject to various constraints
import random
import time
from scipy.optimize import basinhopping
import config

random.seed(time.time())
start_time = time.time()

init_prob = 0.5
params = config.params
direction_probability = [init_prob] * params
direction_probability_change_size = 0.001

sensitive_param = config.sensitive_param
name = 'sex'
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

X = []
Y = []
i = 0
sensitive = {}
sens = []
with open("cleaned_train", "r") as ins:
    for line in ins:
        line = line.strip()
        line1 = line.split(',')
        if (i == 0):
            i += 1
            continue
        L = list(map(int, line1[:-1]))
        sens.append(L[sensitive_param - 1])
        # L[sens_arg-1]=-1
        X.append(L)

        if (int(line1[-1]) == 0):
            Y.append(-1)
        else:
            Y.append(1)

X = np.array(X, dtype=float)
Y = np.array(Y, dtype=float)
sensitive[name] = np.array(sens, dtype=float)
loss_function = lf._logistic_loss
sep_constraint = 0
sensitive_attrs = [name]
sensitive_attrs_to_cov_thresh = {name: cov}

gamma = None

model = ut.train_model(X, Y, sensitive, loss_function, 1, 0, sep_constraint, sensitive_attrs, sensitive_attrs_to_cov_thresh,
                   gamma)


class Local_Perturbation(object):

    def __init__(self, stepsize=1):
        self.stepsize = stepsize

    def __call__(self, x):
        s = self.stepsize
        val = random.randint(0, 12)
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
        for i in range(params):
            random.seed(time.time())
            x[i] = random.randint(input_bounds[i][0], input_bounds[i][1])

        x[sensitive_param - 1] = 0
        # print(x)
        return x



def evaluate_global(inp):
    inp0 = [int(i) for i in inp]
    inp1 = [int(i) for i in inp]

    inp0[sensitive_param - 1] = 0
    inp1[sensitive_param - 1] = 1
    out0 = np.sign(np.dot(model, inp0))
    out1 = np.sign(np.dot(model, inp1))
    tot_inputs.add(tuple(inp0))

    if (abs(out0 - out1) > threshold and tuple(inp0) not in global_disc_inputs):
        global_disc_inputs.add(tuple(inp0))
        global_disc_inputs_list.append(inp0)

    return not abs(out0 - out1) > threshold
    # for binary classification, we have found that the
    # following optimization function gives better results
    # return abs(out1 + out0)


def evaluate_local(inp):
    inp0 = [int(i) for i in inp]
    inp1 = [int(i) for i in inp]

    inp0[sensitive_param - 1] = 0
    inp1[sensitive_param - 1] = 1
    out0 = np.sign(np.dot(model, inp0))
    out1 = np.sign(np.dot(model, inp1))
    tot_inputs.add(tuple(inp0))

    if (abs(out0 - out1) > threshold and (tuple(inp0) not in global_disc_inputs) and (tuple(inp0) not in local_disc_inputs)):
        local_disc_inputs.add(tuple(inp0))
        local_disc_inputs_list.append(inp0)

    return not abs(out0 - out1) > threshold
    # for binary classification, we have found that the
    # following optimization function gives better results
    # return abs(out1 + out0)


initial_input = [7, 4, 26, 1, 4, 4, 0, 0, 0, 1, 5, 73, 1]
minimizer = {"method": "L-BFGS-B"}

global_discovery = Global_Discovery()
local_perturbation = Local_Perturbation()

basinhopping(evaluate_global, initial_input, stepsize=1.0, take_step=global_discovery, minimizer_kwargs=minimizer, niter=global_iteration_limit)

print("Finished Global Search")
print("Percentage discriminatory inputs - " + str(float(len(global_disc_inputs_list) + len(local_disc_inputs_list)) / float(len(tot_inputs))*100))
print("")
print("Starting Local Search")

for inp in global_disc_inputs_list:
    basinhopping(evaluate_local, inp, stepsize=1.0, take_step=local_perturbation, minimizer_kwargs=minimizer,
                 niter=local_iteration_limit)
    print("Percentage discriminatory inputs - " + str(float(len(global_disc_inputs_list) + len(local_disc_inputs_list)) / float(len(tot_inputs))*100))

print()
print("Local Search Finished")
print("Percentage discriminatory inputs - " + str(float(len(global_disc_inputs_list) + len(local_disc_inputs_list)) / float(len(tot_inputs))*100))

print()
print("Total Inputs are " + str(len(tot_inputs)))
print("Number of discriminatory inputs are " + str(len(global_disc_inputs_list)+len(local_disc_inputs_list)))