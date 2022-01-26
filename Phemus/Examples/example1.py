from Phemus import *

def main():
    num_param = 8
    sensitive_param_idx = 5 # Starts at O
    sensitive_param_name = "Gender"
    col_to_be_predicted = "LeaveOrNot"
    dataset_dir = "Employee.csv"

    dataset = Dataset(num_param, sensitive_param_idx, sensitive_param_name, col_to_be_predicted, dataset_dir)

    pkl_dir = 'Employee_DecisionTree_Original.pkl'
    improved_pkl_dir = 'Employee_DecisionTree_Original_Improved.pkl'
    
    threshold = 0
    perturbation_unit = 1
    global_iteration_limit = 1000 # needs to be at least 1000 to be effective
    local_iteration_limit = 100 

    num_trials = 100
    samples = 100

    run_aequitas_fully_direct(dataset, perturbation_unit, pkl_dir, improved_pkl_dir, threshold,  \
                    global_iteration_limit, local_iteration_limit, num_trials, samples)

if __name__ == "__main__":
    main() 