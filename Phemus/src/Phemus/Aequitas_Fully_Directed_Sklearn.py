from __future__ import division
import random
from re import X
import numpy as np
import random
import time
import joblib
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
from .mpFully_Direct import mp_basinhopping
from .Dataset import Dataset
from scipy.optimize import basinhopping

'''
This is a Aequitas Fully Directed Mode
'''

class Fully_Direct:
    def __init__(self, dataset: Dataset, perturbation_unit, threshold, global_iteration_limit, \
                        local_iteration_limit, input_pkl_dir, retrain_csv_dir):
        random.seed(time.time())
        self.start_time = time.time()

        self.column_names = dataset.column_names
        self.num_params = dataset.num_params
        self.input_bounds = dataset.input_bounds # contains the y column to preserve idxes!
        self.sensitive_param_idx = dataset.sensitive_param_idx
        self.sensitive_param_name = dataset.sensitive_param_name
        self.col_to_be_predicted_idx = dataset.col_to_be_predicted_idx

        self.input_pkl_dir = input_pkl_dir
        self.perturbation_unit = perturbation_unit
        self.threshold = threshold
        self.global_iteration_limit = global_iteration_limit
        self.local_iteration_limit = local_iteration_limit

        self.init_prob = 0.5
        self.cov = 0
        self.direction_probability_change_size = 0.001
        self.param_probability_change_size = 0.001

        self.direction_probability = [self.init_prob] * len(self.input_bounds)
        self.direction_probability[self.col_to_be_predicted_idx] = 0 # nullify the y col
        self.param_probability = [1.0/self.num_params] * len(self.input_bounds)
        self.param_probability[self.col_to_be_predicted_idx] = 0
 
        self.global_disc_inputs = set()
        self.global_disc_inputs_list = []

        self.local_disc_inputs = set()
        self.local_disc_inputs_list = []

        self.tot_inputs = set()

        self.model = joblib.load(input_pkl_dir)


    def normalise_probability(self):
        probability_sum = 0.0
        for prob in self.param_probability:
            probability_sum = probability_sum + prob

        for i in range(self.num_params):
            self.param_probability[i] = float(self.param_probability[i])/float(probability_sum) 


    def evaluate_input(self, inp):
        inp0 = [int(k) for k in inp]
        sensValue = inp0[self.sensitive_param_idx]
        inp0 = np.asarray(inp0)
        inp0 = np.reshape(inp0, (1, -1))
        inp0delY = np.delete(inp0, [self.col_to_be_predicted_idx])
        inp0delY = np.reshape(inp0delY, (1, -1))
        out0 = self.model.predict(inp0delY)
        
        # Loops through all values of the sensitive parameter
        for i in range(self.input_bounds[self.sensitive_param_idx][1] + 1):
            if sensValue != i:
                inp1 = [int(k) for k in inp]
                inp1[self.sensitive_param_idx] = i

                inp1 = np.asarray(inp1)
                inp1 = np.reshape(inp1, (1, -1))

                # drop y column here
                inp1delY = np.delete(inp1, [self.col_to_be_predicted_idx])
                inp1delY = np.reshape(inp1delY, (1, -1))

                out1 = self.model.predict(inp1delY)

                if abs(out1 - out0) > self.threshold:
                    return abs(out1 - out0)
        return False


    def evaluate_global(self, inp):
        inp0 = [int(i) for i in inp]
        sensValue = inp0[self.sensitive_param_idx]

        inp0np = np.asarray(inp0)
        inp0np = np.reshape(inp0, (1, -1))
        self.tot_inputs.add(tuple(map(tuple, inp0np)))

        inp0 = np.asarray(inp0)
        inp0 = np.reshape(inp0, (1, -1))

        # Returns early if input is already in the global discriminatory inputs set
        if (tuple(map(tuple, inp0)) in self.global_disc_inputs):
            return 0
        
        inp0delY = np.delete(inp0, [self.col_to_be_predicted_idx])
        inp0delY = np.reshape(inp0delY, (1, -1))
        out0 = self.model.predict(inp0delY)
        
        # Loops through all values of the sensitive parameter
        for i in range(self.input_bounds[self.sensitive_param_idx][1] + 1):   
            if i != sensValue: 
                inp1 = [int(k) for k in inp]
                inp1[self.sensitive_param_idx] = i
                inp1 = np.asarray(inp1)
                inp1 = np.reshape(inp1, (1, -1))
                
                # drop y column here 
                inp1delY = np.delete(inp1, [self.col_to_be_predicted_idx])
                inp1delY = np.reshape(inp1delY, (1, -1))
                out1 = self.model.predict(inp1delY)

                if (abs(out0 - out1) > self.threshold):
                    self.global_disc_inputs.add(tuple(map(tuple, inp0))) # add the entire input, including original y
                    self.global_disc_inputs_list.append(inp0.tolist()[0])
                    return abs(out0 - out1)
        return 0
        
    def evaluate_local(self,  inp):
        inp0 = [int(i) for i in inp]
        sensValue = inp0[self.sensitive_param_idx]

        inp0np = np.asarray(inp0)
        inp0np = np.reshape(inp0, (1, -1))

        self.tot_inputs.add(tuple(map(tuple, inp0np)))

        inp0 = np.asarray(inp0)
        inp0 = np.reshape(inp0, (1, -1))
        
        # Returns early if input is already in the global or local discriminatory inputs set
        if ((tuple(map(tuple, inp0)) in self.global_disc_inputs) or (tuple(map(tuple, inp0)) in self.local_disc_inputs)):
            return 0
        
        inp0delY = np.delete(inp0, [self.col_to_be_predicted_idx])
        inp0delY = np.reshape(inp0delY, (1, -1))
        out0 = self.model.predict(inp0delY)
        
        # Loops through all values of the sensitive parameter
        for i in range(self.input_bounds[self.sensitive_param_idx][1] + 1):
            if sensValue != i: 
                inp1 = [int(k) for k in inp]
                inp1[self.sensitive_param_idx] = i
                inp1 = np.asarray(inp1)
                inp1 = np.reshape(inp1, (1, -1))

                # drop y column here 
                inp1delY = np.delete(inp1, [self.col_to_be_predicted_idx])
                inp1delY = np.reshape(inp1delY, (1, -1))

                out1 = self.model.predict(inp1delY)

                if abs(out0 - out1) > self.threshold:
                    self.local_disc_inputs.add(tuple(map(tuple, inp0)))
                    self.local_disc_inputs_list.append(inp0.tolist()[0])
                    return abs(out0 - out1)
        return 0


    def global_discovery(self, x, stepsize = 1):
        s = stepsize
        try:
            sensitive_param_idx = self.sensitive_param_idx
            random.seed(time.time())
            x = [random.randint(low,high) for [low, high] in self.input_bounds]
            x[sensitive_param_idx] = 0
            return x
        except: # unknown error
            return x

    def local_perturbation(self, x, stepsize = 1):
        s = stepsize
        columns = [i for i in range(len(self.input_bounds))] # we're only perturbing non-y columns right?
        param_choice = np.random.choice(columns, p = self.param_probability) # self.param_probability of the y column is set to 0 in the constructor
        act = [-1, 1]
        direction_choice = np.random.choice(act, p=[self.direction_probability[param_choice],  
                                                (1 - self.direction_probability[param_choice])])

        if (x[param_choice] == self.input_bounds[param_choice][0]) or (x[param_choice] == self.input_bounds[param_choice][1]):
            direction_choice = np.random.choice(act)

        x[param_choice] = x[param_choice] + (direction_choice * self.perturbation_unit)

        x[param_choice] = max(self.input_bounds[param_choice][0], x[param_choice])
        x[param_choice] = min(self.input_bounds[param_choice][1], x[param_choice])

        ei = self.evaluate_input(x)

        if (ei and direction_choice == -1) or (not ei and direction_choice == 1):
            self.direction_probability[param_choice] = min(
                self.direction_probability[param_choice] 
                    + (self.direction_probability_change_size * self.perturbation_unit), 1)

        elif (not ei and direction_choice == -1) or (ei and direction_choice == 1):
            self.direction_probability[param_choice] = max(
                self.direction_probability[param_choice] 
                    - (self.direction_probability_change_size * self.perturbation_unit), 0)

        if ei:
            self.param_probability[param_choice] = self.param_probability[param_choice] + self.param_probability_change_size
            self.normalise_probability()
        else:
            self.param_probability[param_choice] = max(self.param_probability[param_choice] - self.param_probability_change_size, 0)
            self.normalise_probability()

        return x

def aequitas_fully_directed_sklearn(dataset: Dataset, perturbation_unit, threshold, global_iteration_limit,\
         local_iteration_limit, input_pkl_dir, retrain_csv_dir):

    print("Aequitas Fully Directed Started...\n")
    initial_input = [random.randint(low,high) for [low, high] in dataset.input_bounds]
    minimizer = {"method": "L-BFGS-B"}

    fully_direct = Fully_Direct(dataset, perturbation_unit, threshold, global_iteration_limit, \
            local_iteration_limit, input_pkl_dir, retrain_csv_dir)

    basinhopping(fully_direct.evaluate_global, initial_input, stepsize=1.0, take_step=fully_direct.global_discovery, minimizer_kwargs=minimizer,
                niter=global_iteration_limit)

    print("Finished Global Search")
    print("Percentage discriminatory inputs - " + str(float(len(fully_direct.global_disc_inputs_list)
                                                    + len(fully_direct.local_disc_inputs_list)) / float(len(fully_direct.tot_inputs))*100))
    print()
    print("Starting Local Search")

    # for inp in fully_direct.global_disc_inputs_list:
    #     basinhopping(fully_direct.evaluate_local, initial_input, stepsize=1.0, take_step=fully_direct.local_perturbation, minimizer_kwargs=minimizer,
    #             niter=local_iteration_limit)
    #     print("Percentage discriminatory inputs - " + str(float(len(fully_direct.global_disc_inputs_list) + len(fully_direct.local_disc_inputs_list))
    #                                                   / float(len(fully_direct.tot_inputs))*100))
    
    fully_direct = mp_basinhopping(fully_direct, minimizer, local_iteration_limit)
    # save the discriminatory inputs to file
    column_names = dataset.column_names
    f = open(retrain_csv_dir, 'w')
    f.write(",".join(column_names) + "\n") # write the column names on top first

    for inp in fully_direct.global_disc_inputs_list:
        f.write(",".join(list(map(lambda x: str(x), inp))) + "\n")
    
    for inp in fully_direct.local_disc_inputs_list:
        f.write(",".join(list(map(lambda x: str(x), inp))) + "\n")

    f.close()

    print()
    print("Local Search Finished")
    print("Percentage discriminatory inputs - " + str(float(len(fully_direct.global_disc_inputs_list) 
                                        + len(fully_direct.local_disc_inputs_list)) / float(len(fully_direct.tot_inputs))*100))

    print("")
    print("Total Inputs are " + str(len(fully_direct.tot_inputs)))
    print("Number of discriminatory inputs are " + str(len(fully_direct.global_disc_inputs_list)
                                                            +len(fully_direct.local_disc_inputs_list)))