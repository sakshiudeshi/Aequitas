from sklearn.externals import joblib
import config
import time
import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import utils as ut
import loss_funcs as lf


sensitive = {}
sens = []
name = 'sex'
cov = 0

input_bounds = config.input_bounds
params = config.params
sensitive_param = config.sensitive_param

num_trials = 100
samples = 100

def extractor(filename):

    X = []
    Y = []
    sens = []
    i = 0
    with open(filename, "r") as ins:
        for line in ins:
            line = line.strip()
            line1 = line.split(',')
            if (i == 0):
                i += 1
                continue
            L = map(int, line1[:-1])
            sens.append(L[sensitive_param - 1])
            # L[sens_arg-1]=-1
            X.append(L)

            if (int(line1[-1]) == 0):
                Y.append(-1)
            else:
                Y.append(1)

    return X, Y, sens

def extractor_retrain(filename, num_additional):
    X = []
    Y = []
    sens = []
    i = 0
    with open(filename, "r") as ins:
        for line in ins:
            line = line.strip()
            line1 = line.split(',')
            if (i == 0):
                i += 1
                continue
            L = map(int, line1[:-1])
            sens.append(L[sensitive_param - 1])
            # L[sens_arg-1]=-1
            X.append(L)

            if (int(line1[-1]) == 0):
                Y.append(-1)
            else:
                Y.append(1)

    if (num_additional > len(X)):
        raise ValueError('Number of inputs in retraining are not enough. Please add more inputs')

    retrain_len = len(X)
    retraining_input_set = set()
    while (len(retraining_input_set) < num_additional):
        retraining_input_set.add(random.randint(0, retrain_len - 1))


    X_additional = []
    Y_additional = []
    sens_additional = []
    for i in retraining_input_set:
        X_additional.append(X[i])
        Y_additional.append(Y[i])
        sens_additional.append(sens[i])

    return X_additional, Y_additional, sens_additional


def train():
    sensitive = {}
    X, Y, sens = extractor("cleaned_train")

    X = np.array(X, dtype=float)
    Y = np.array(Y, dtype=float)
    sensitive[name] = np.array(sens, dtype=float)
    loss_function = lf._logistic_loss
    sep_constraint = 0
    sensitive_attrs = [name]
    sensitive_attrs_to_cov_thresh = {name: cov}

    gamma = None

    model = ut.train_model(X, Y, sensitive, loss_function, 1, 0, sep_constraint, sensitive_attrs,
                           sensitive_attrs_to_cov_thresh,
                           gamma)
    return model


current_model = train()


retraining_inputs = config.retraining_inputs

def retrain(num_additional):
    sensitive = {}
    X_original, Y_original, sens_original = extractor("cleaned_train")
    X_additional, Y_additional, sens_additional = extractor(retraining_inputs)

    X = X_additional + X_original
    Y = Y_additional + Y_original
    sens = sens_additional + sens_original

    X = np.array(X, dtype=float)
    Y = np.array(Y, dtype=float)
    sensitive[name] = np.array(sens, dtype=float)
    loss_function = lf._logistic_loss
    sep_constraint = 0
    sensitive_attrs = [name]
    sensitive_attrs_to_cov_thresh = {name: cov}

    gamma = None

    model = ut.train_model(X, Y, sensitive, loss_function, 1, 0, sep_constraint, sensitive_attrs,
                           sensitive_attrs_to_cov_thresh,
                           gamma)
    return model

def get_random_input():
    x = []
    for i in xrange(params):
        random.seed(time.time())
        x.append(random.randint(input_bounds[i][0], input_bounds[i][1]))

    x[sensitive_param - 1] = 0
    return x

def evaluate_input(inp, model):
    inp0 = [int(i) for i in inp]
    inp1 = [int(i) for i in inp]

    inp0[sensitive_param - 1] = 0
    inp1[sensitive_param - 1] = 1
    out0 = np.sign(np.dot(model, inp0))
    out1 = np.sign(np.dot(model, inp1))


    return (abs(out1 + out0) == 0)

def get_estimate(model):
    estimate_array = []
    rolling_average = 0.0
    for i in xrange(num_trials):
        disc_count = 0
        total_count = 0
        for j in xrange(samples):
            total_count = total_count + 1
            if(evaluate_input(get_random_input(), model)):
                disc_count = disc_count + 1

        estimate = float(disc_count)/total_count
        rolling_average = ((rolling_average * i) + estimate)/(i + 1)
        estimate_array.append(estimate)

        # print estimate, rolling_average

    return np.average(estimate_array)

current_estimate = get_estimate(current_model)


def retrain_search():
    global current_estimate
    global current_model
    X, Y, sens = extractor("cleaned_train")
    for i in xrange(7):
        additive_percentage = random.uniform(pow(2, i), pow(2, i + 1))
        num_inputs_for_retrain = int((additive_percentage * len(X))/100)


        retrained_model = retrain(num_inputs_for_retrain)
        retrained_estimate = get_estimate(retrained_model)

        if (retrained_estimate > current_estimate):
            return current_model
        else:
            current_model = retrained_model
            current_estimate = retrained_estimate
            del retrained_estimate
            del retrained_model
    return current_model

retrain_search()