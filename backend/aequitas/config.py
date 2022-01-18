import utils as utils

'''
Employee
'''

num_params = 8 # exclude "y" col

sensitive_param_idx = 5 # Starts at O

sensitive_param_name = "Gender"

col_to_be_predicted = "LeaveOrNot"

classifier_name = 'Employee_DecisionTree_Original.pkl'

original_inputs = "Employee.csv"

column_names = utils.get_column_names(original_inputs)

input_bounds = utils.get_input_bounds(original_inputs, col_to_be_predicted)

col_to_be_predicted_idx = utils.get_idx_of_col_to_be_predicted(original_inputs, col_to_be_predicted)

threshold = 0

perturbation_unit = 1

retraining_inputs = "Employee_Retraining_Dataset.csv" # need to be modified after running Aequitas



'''
Original
'''

# num_params = 13

# sensitive_param_idx = 8 # Starts at 0.

# sensitive_param_name = "sex"

# col_to_be_predicted_idx = -1

# input_bounds = []
# input_bounds.append([1, 9])
# input_bounds.append([0, 7])
# input_bounds.append([0, 39])
# input_bounds.append([0, 15])
# input_bounds.append([0, 6])
# input_bounds.append([0, 13])
# input_bounds.append([0, 5])
# input_bounds.append([0, 4])
# input_bounds.append([0, 1])
# input_bounds.append([0, 99])
# input_bounds.append([0, 39])
# input_bounds.append([0, 99])
# input_bounds.append([0, 39])

# classifier_name = 'Decision_tree_standard_unfair.pkl'

# threshold = 0

# perturbation_unit = 1

# retraining_inputs = "Retrain_Example_File.txt"

# original_inputs = "cleaned_train"