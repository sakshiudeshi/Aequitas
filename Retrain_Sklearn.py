from sklearn.externals import joblib
import config
import time
import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier

def extract_inputs(filename):
    X = []
    Y = []
    i = 0
    neg_count = 0
    pos_count = 0
    with open(filename, "r") as ins:
        for line in ins:
            line = line.strip()
            line1 = line.split(',')
            if (i == 0):
                i += 1
                continue
            L = map(int, line1[:-1])
            # L[sens_arg-1]=-1
            X.append(L)

            if (int(line1[-1]) == 0):
                Y.append(-1)
                neg_count = neg_count + 1
            else:
                Y.append(1)
                pos_count = pos_count + 1

    return X, Y

X, Y = extract_inputs("cleaned_train")
X_original = np.array(X)
Y_original = np.array(Y)

num_trials = 100
samples = 100

classifier_name = config.classifier_name
current_model = joblib.load(classifier_name)
input_bounds = config.input_bounds
params = config.params
sensitive_param = config.sensitive_param

retraining_inputs = config.retraining_inputs

def retrain(X_original, Y_original, X_additional, Y_additional):

    X = np.concatenate((X_original, X_additional), axis = 0)
    Y = np.concatenate((Y_original, Y_additional), axis = 0)

    current_model.fit(X, Y)
    return current_model

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

    inp0 = np.asarray(inp0)
    inp0 = np.reshape(inp0, (1, -1))

    inp1 = np.asarray(inp1)
    inp1 = np.reshape(inp1, (1, -1))

    out0 = model.predict(inp0)
    out1 = model.predict(inp1)

    return (abs(out0 + out1) == 0)

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

    print np.average(estimate_array)
    return np.average(estimate_array)

current_estimate = get_estimate(current_model)

def retrain_search():
    global current_estimate
    global current_model
    X_retrain, Y_retrain = extract_inputs(retraining_inputs)
    retrain_len = len(X_retrain)
    for i in xrange(7):
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
        retrained_model = retrain(X_original, Y_original, np.array(X_additional), np.array(Y_additional))
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