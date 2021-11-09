import pandas as pd

'''
Employee
'''

params = 8 # exclude "y" col

sensitive_param = 6 # Starts at 0

classifier_name = 'Employee_DecisionTree_Original.pkl'

original_inputs = "Employee.csv"
input_bounds = []
df=pd.read_csv(original_inputs)
for col in df:
    # not sure if I should exclude 'LeaveOrNot' here or not
    if col == "LeaveOrNot":
        continue
    numUniqueVals = df[col].nunique()
    input_bounds.append([0, numUniqueVals - 1]) # bound is inclusive
print(input_bounds)

threshold = 0

perturbation_unit = 1

retraining_inputs = "Retrain_Example_File.txt"






'''
Original
'''

# params = 13

# sensitive_param = 9 # Starts at 1.

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