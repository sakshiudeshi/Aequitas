from __future__ import division
import random
import numpy as np
import random
import time
from scipy.optimize import basinhopping
from .mpFully_Direct import mp_basinhopping
from .Dataset import Dataset
import joblib
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

'''
This is a Aequitas Semi Directed Mode
'''

class Semi_Direct:
    def __init__(self, dataset: Dataset, perturbation_unit, threshold, global_iteration_limit, \
                        local_iteration_limit, input_pkl_dir, retrain_csv_dir):
        random.seed(time.time())
        self.start_time = time.time()

        self.init_prob = 0.5
        self.num_params = dataset.num_params
        self.direction_probability = [self.init_prob] * len(dataset.input_bounds)
        self.direction_probability[dataset.col_to_be_predicted_idx] = 0 # nullify the y col
        self.direction_probability_change_size = 0.001

        self.sensitive_param_idx = dataset.sensitive_param_idx
        self.name = dataset.sensitive_param_name
        self.col_to_be_predicted_idx = dataset.col_to_be_predicted_idx
        self.cov = 0

        self.perturbation_unit = perturbation_unit

        self.threshold = threshold

        self.global_disc_inputs = set()
        self.global_disc_inputs_list = []

        self.local_disc_inputs = set()
        self.local_disc_inputs_list = []

        self.tot_inputs = set()

        self.global_iteration_limit = global_iteration_limit 
        self.local_iteration_limit = local_iteration_limit

        self.input_bounds = dataset.input_bounds

        self.model = joblib.load(input_pkl_dir)
    
    def local_perturbation(self, x):
        idxes_of_non_y_columns = [i for i in range(len(self.input_bounds))] # we're only perturbing non-y columns right?
        idxes_of_non_y_columns.pop(self.col_to_be_predicted_idx) # if not no need to delete this idx
        param_choice = np.random.choice(idxes_of_non_y_columns)
        act = [-1, 1]
        direction_choice = np.random.choice(act, p=[self.direction_probability[param_choice], (1 - self.direction_probability[param_choice])])

        if (x[param_choice] == self.input_bounds[param_choice][0]) or (x[param_choice] == self.input_bounds[param_choice][1]):
            direction_choice = np.random.choice(act)

        x[param_choice] = x[param_choice] + (direction_choice * self.perturbation_unit)

        x[param_choice] = max(self.input_bounds[param_choice][0], x[param_choice])
        x[param_choice] = min(self.input_bounds[param_choice][1], x[param_choice])

        ei = self.evaluate_input(x)

        if (ei and direction_choice == -1) or (not ei and direction_choice == 1):
            self.direction_probability[param_choice] = min(
                self.direction_probability[param_choice] + (self.direction_probability_change_size * self.perturbation_unit), 1)

        elif (not ei and direction_choice == -1) or (ei and direction_choice == 1):
            self.direction_probability[param_choice] = max(
                self.direction_probability[param_choice] - (self.direction_probability_change_size * self.perturbation_unit), 0)

        return x
    
    def global_discovery(self, x):
        sensitive_param_idx = self.sensitive_param_idx
        random.seed(time.time())
        x = [random.randint(low,high) for [low, high] in self.input_bounds]
        x[sensitive_param_idx] = 0
        return x

    def evaluate_input(self, inp):
        inp0 = [int(k) for k in inp]
        sensValue = inp0[self.sensitive_param_idx]
        inp0 = np.asarray(inp0)
        inp0 = np.reshape(inp0, (1, -1))
        inp0delY = np.delete(inp0, [self.col_to_be_predicted_idx])
        inp0delY = np.reshape(inp0delY, (1, -1))
        out0 = self.model.predict(inp0delY)

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

                if abs(out1 - out0) > self.threshold:
                    return abs(out1 - out0)
        return False

    def evaluate_global(self, inp):
        inp0 = [int(i) for i in inp]
        sensValue = inp0[self.sensitive_param_idx]
        inp0np = np.asarray(inp0)
        inp0np = np.reshape(inp0, (1, -1))
        self.tot_inputs.add(tuple(map(tuple, inp0np)))

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
                    self.global_disc_inputs.add(tuple(map(tuple, inp0)))
                    self.global_disc_inputs_list.append(inp0.tolist()[0])
                    self.f.write(",".join(list(map(lambda x: str(x), inp0.tolist()[0]))) + "\n") # write inputs as they are generated
                    return abs(out0 - out1)
        return 0
        
    def evaluate_local(self,  inp):
        inp0 = [int(i) for i in inp]
        sensValue = inp0[self.sensitive_param_idx] 
        inp0np = np.asarray(inp0)
        inp0np = np.reshape(inp0, (1, -1))
        self.tot_inputs.add(tuple(map(tuple, inp0np)))
        
        # Returns early if input is already in the global or local discriminatory inputs set
        if ((tuple(map(tuple, inp0)) in self.global_disc_inputs) or (tuple(map(tuple, inp0)) in self.local_disc_inputs)):
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
                    self.local_disc_inputs.add(tuple(map(tuple, inp0)))
                    self.local_disc_inputs_list.append(inp0.tolist()[0])
                    return abs(out0 - out1)
        return 0

def aequitas_semi_directed_sklearn(dataset: Dataset, perturbation_unit, threshold, global_iteration_limit,\
         local_iteration_limit, input_pkl_dir, retrain_csv_dir):
    # initial_input = [7, 4, 26, 1, 4, 4, 0, 0, 0, 1, 5, 73, 1]
    initial_input = [random.randint(low,high) for [low, high] in dataset.input_bounds]
    minimizer = {"method": "L-BFGS-B"}

    semi_direct = Semi_Direct(dataset, perturbation_unit, threshold, global_iteration_limit, \
                        local_iteration_limit, input_pkl_dir, retrain_csv_dir)    

    basinhopping(semi_direct.evaluate_global, initial_input, stepsize=1.0, take_step=semi_direct.global_discovery, minimizer_kwargs=minimizer,
                niter=global_iteration_limit)

    print("Finished Global Search")
    print("Percentage discriminatory inputs - " + str(float(len(semi_direct.global_disc_inputs_list)
                                                            + len(semi_direct.local_disc_inputs_list)) / float(len(semi_direct.tot_inputs))*100))
    print()
    print("Starting Local Search")

    # for inp in semi_direct.global_disc_inputs_list:
    #     basinhopping(semi_direct.evaluate_local, inp, stepsize=1.0, take_step=semi_direct.local_perturbation, minimizer_kwargs=minimizer,
    #                 niter=semi_direct.local_iteration_limit)
    #     print("Percentage discriminatory inputs - " + str(float(len(semi_direct.global_disc_inputs_list) + len(semi_direct.local_disc_inputs_list))
                                                        # / float(len(semi_direct.tot_inputs))*100))

    semi_direct = mp_basinhopping(semi_direct, minimizer, local_iteration_limit)
                                         
    column_names = dataset.column_names
    f = open(retrain_csv_dir, 'w')
    f.write(",".join(column_names) + "\n") # write the column names on top first

    for inp in semi_direct.global_disc_inputs_list:
        f.write(",".join(list(map(lambda x: str(x), inp))) + "\n")
    
    for inp in semi_direct.local_disc_inputs_list:
        f.write(",".join(list(map(lambda x: str(x), inp))) + "\n")

    f.close()

    print()
    print("Local Search Finished")
    print("Percentage discriminatory inputs - " + str(float(len(semi_direct.global_disc_inputs_list) + len(semi_direct.local_disc_inputs_list))
                                                    / float(len(semi_direct.tot_inputs))*100))

    print()
    print("Total Inputs are " + str(len(semi_direct.tot_inputs)))
    print("Number of discriminatory inputs are " + str(len(semi_direct.global_disc_inputs_list)+len(semi_direct.local_disc_inputs_list)))

