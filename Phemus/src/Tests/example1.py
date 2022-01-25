from Phemus import *
import utils

def main():
    num_param = 8
    sensitive_param_idx = 5 # Starts at O
    sensitive_param_name = "Gender"
    col_to_be_predicted = "LeaveOrNot"
    input_pkl_dir = 'Employee_DecisionTree_Original.pkl'
    improved_pkl_dir = 'Employee_DecisionTree_Original_Improved.pkl'
    input_csv_dir = "Employee.csv"
    column_names = utils.get_column_names(input_csv_dir)
    input_bounds = utils.get_input_bounds(input_csv_dir, col_to_be_predicted)
    col_to_be_predicted_idx = utils.get_idx_of_col_to_be_predicted(input_csv_dir, col_to_be_predicted)
    threshold = 0
    perturbation_unit = 1
    global_iteration_limit = 100 # needs to be at least 1000 to be effective
    local_iteration_limit = 100 

    num_trials = 100
    samples = 100

    print("running")
    run_Aequitas_fully_direct(num_param, sensitive_param_idx, sensitive_param_name, perturbation_unit, threshold, \
                  global_iteration_limit, local_iteration_limit, input_bounds, input_pkl_dir, input_csv_dir, \
                  improved_pkl_dir, num_trials, samples, column_names, col_to_be_predicted_idx)

if __name__ == "__main__":
    main() 