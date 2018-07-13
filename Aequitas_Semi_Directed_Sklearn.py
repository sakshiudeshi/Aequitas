from __future__ import division
from random import seed, shuffle
import random
import math
import os
from collections import defaultdict
from sklearn import svm
import os,sys
import urllib2
sys.path.insert(0, './fair_classification/') # the code for fair classification is in this directory
import numpy as np
import loss_funcs as lf # loss funcs that can be optimized subject to various constraints
import random
import time
from scipy.optimize import basinhopping
import config
from sklearn.externals import joblib

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
classifier_name = config.classifier_name

model = joblib.load(classifier_name)

class Local_Perturbation(object):

    def __init__(self, stepsize=1):
        self.stepsize = stepsize

    def __call__(self, x):
        s = self.stepsize
        param_choice = random.randint(0, 12)
        act = [-1, 1]
        direction_choice = np.random.choice(act, p=[direction_probability[param_choice], (1 - direction_probability[param_choice])])

        if (x[param_choice] == input_bounds[param_choice][0]) or (x[param_choice] == input_bounds[param_choice][1]):
            direction_choice = np.random.choice(act)

        x[param_choice] = x[param_choice] + (direction_choice * perturbation_unit)

        x[param_choice] = max(input_bounds[param_choice][0], x[param_choice])
        x[param_choice] = min(input_bounds[param_choice][1], x[param_choice])

        ei = evaluate_input(x)

        if (ei and direction_choice == -1) or (not ei and direction_choice == 1):
            direction_probability[param_choice] = min(
                direction_probability[param_choice] + (direction_probability_change_size * perturbation_unit), 1)

        elif (not ei and direction_choice == -1) or (ei and direction_choice == 1):
            direction_probability[param_choice] = max(
                direction_probability[param_choice] - (direction_probability_change_size * perturbation_unit), 0)

        return x


class Global_Discovery(object):
    def __init__(self, stepsize=1):
        self.stepsize = stepsize

    def __call__(self, x):
        s = self.stepsize
        for i in xrange(params):
            random.seed(time.time())
            x[i] = random.randint(input_bounds[i][0], input_bounds[i][1])

        x[sensitive_param - 1] = 0
        # print x
        return x


def evaluate_input(inp):
    inp0 = [int(i) for i in inp]
    inp1 = [int(i) for i in inp]

    inp0[8] = 0
    inp1[8] = 1

    inp0 = np.asarray(inp0)
    inp0 = np.reshape(inp0, (1, -1))

    inp1 = np.asarray(inp1)
    inp1 = np.reshape(inp1, (1, -1))

    out0 = model.predict(inp0)
    out1 = model.predict(inp1)

    return (abs(out0 - out1) > threshold)
    # for binary classification, we have found that the
    # following optimization function gives better results
    # return abs(out1 + out0)

def evaluate_global(inp):
    inp0 = [int(i) for i in inp]
    inp1 = [int(i) for i in inp]

    inp0[8] = 0
    inp1[8] = 1

    inp0 = np.asarray(inp0)
    inp0 = np.reshape(inp0, (1, -1))

    inp1 = np.asarray(inp1)
    inp1 = np.reshape(inp1, (1, -1))

    out0 = model.predict(inp0)
    out1 = model.predict(inp1)

    tot_inputs.add(tuple(map(tuple, inp0)))

    if (abs(out0 - out1) > threshold and tuple(map(tuple, inp0)) not in global_disc_inputs):
        global_disc_inputs.add(tuple(map(tuple, inp0)))
        global_disc_inputs_list.append(inp0.tolist()[0])

    return not abs(out0 - out1) > threshold
    # for binary classification, we have found that the
    # following optimization function gives better results
    # return abs(out1 + out0)


def evaluate_local(inp):
    inp0 = [int(i) for i in inp]
    inp1 = [int(i) for i in inp]

    inp0[8] = 0
    inp1[8] = 1

    inp0 = np.asarray(inp0)
    inp0 = np.reshape(inp0, (1, -1))

    inp1 = np.asarray(inp1)
    inp1 = np.reshape(inp1, (1, -1))

    out0 = model.predict(inp0)
    out1 = model.predict(inp1)

    tot_inputs.add(tuple(map(tuple, inp0)))

    if (abs(out0 - out1) > threshold and (tuple(map(tuple, inp0)) not in global_disc_inputs)
        and (tuple(map(tuple, inp0)) not in local_disc_inputs)):
        local_disc_inputs.add(tuple(map(tuple, inp0)))
        local_disc_inputs_list.append(inp0.tolist()[0])

    return not abs(out0 - out1) > threshold
    # for binary classification, we have found that the
    # following optimization function gives better results
    # return abs(out1 + out0)


initial_input = [7, 4, 26, 1, 4, 4, 0, 0, 0, 1, 5, 73, 1]
minimizer = {"method": "L-BFGS-B"}

global_discovery = Global_Discovery()
local_perturbation = Local_Perturbation()

basinhopping(evaluate_global, initial_input, stepsize=1.0, take_step=global_discovery, minimizer_kwargs=minimizer,
             niter=global_iteration_limit)

print "Finished Global Search"
print "Percentage discriminatory inputs - " + str(float(len(global_disc_inputs_list)
                                                        + len(local_disc_inputs_list)) / float(len(tot_inputs))*100)
print ""
print "Starting Local Search"

for inp in global_disc_inputs_list:
    basinhopping(evaluate_local, inp, stepsize=1.0, take_step=local_perturbation, minimizer_kwargs=minimizer,
                 niter=local_iteration_limit)
    print "Percentage discriminatory inputs - " + str(float(len(global_disc_inputs_list) + len(local_disc_inputs_list))
                                                      / float(len(tot_inputs))*100)

print ""
print "Local Search Finished"
print "Percentage discriminatory inputs - " + str(float(len(global_disc_inputs_list) + len(local_disc_inputs_list))
                                                  / float(len(tot_inputs))*100)

print ""
print "Total Inputs are " + str(len(tot_inputs))
print "Number of discriminatory inputs are " + str(len(global_disc_inputs_list)+len(local_disc_inputs_list))