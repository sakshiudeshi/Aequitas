from sklearn.externals import joblib
import config
import time
import random
import numpy as np

num_trials = 100
samples = 100

classifier_name = config.classifier_name
model = joblib.load(classifier_name)
input_bounds = config.input_bounds
params = config.params
sensitive_param = config.sensitive_param

def get_random_input():
    x = []
    for i in xrange(params):
        random.seed(time.time())
        x.append(random.randint(input_bounds[i][0], input_bounds[i][1]))

    x[sensitive_param - 1] = 0
    return x

def evaluate_input(inp):
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

def get_estimate_arrray():
    estimate_array = []
    rolling_average = 0.0
    for i in xrange(num_trials):
        disc_count = 0
        total_count = 0
        for j in xrange(samples):
            total_count = total_count + 1
            if(evaluate_input(get_random_input())):
                disc_count = disc_count + 1

        estimate = float(disc_count)/total_count
        rolling_average = ((rolling_average * i) + estimate)/(i + 1)
        estimate_array.append(estimate)
        print estimate, rolling_average
    return estimate_array

print "Getting Estimate array"

arr = get_estimate_arrray()

print "Estimate is " + str(np.mean(arr) * 100) + "%"