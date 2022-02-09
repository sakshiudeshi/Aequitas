from Phemus import *

def main():
    num_param = 8
    sensitive_param_idx = 5 # Starts at O
    sensitive_param_name = "Gender"
    col_to_be_predicted = "LeaveOrNot"
    dataset_dir = "Employee.csv"
    model_type = "DecisionTree"

    dataset = Dataset(num_param, sensitive_param_idx, model_type, \
        sensitive_param_name, col_to_be_predicted, dataset_dir)

    pkl_dir = 'Employee_DecisionTree_Original.pkl'
    improved_pkl_dir = 'Employee_DecisionTree_Original_Improved.pkl'
    retrain_csv_dir = 'Employee_Retraining_Dataset.csv'
    plot_dir = 'Employee_Fairness_Plot.png'
    cleaned_csv_dir = 'Employee_cleaned.csv'
    
    threshold = 0
    perturbation_unit = 1
    global_iteration_limit = 1000 # needs to be at least 1000 to be effective
    local_iteration_limit = 100 

    num_trials = 100
    samples = 100

    run_aequitas_fully_direct(dataset, perturbation_unit, cleaned_csv_dir, pkl_dir, \
                    improved_pkl_dir, retrain_csv_dir, plot_dir, threshold,  \
                    global_iteration_limit, local_iteration_limit, num_trials, samples)

if __name__ == "__main__":
    main() 