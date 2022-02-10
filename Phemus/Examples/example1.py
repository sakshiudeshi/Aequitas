import os, sys
os.chdir('..')
sys.path.append(os.getcwd())
from src.Phemus import *
#from Phemus import * <-- use this if loading Phemus from local folder

def main():
    num_params = 8
    sensitive_param_idx = 5 # Starts at O
    sensitive_param_name = "Gender"
    col_to_be_predicted = "LeaveOrNot"
    dataset_dir = "Employee.csv"
    model_type = "DecisionTree"
    os.chdir('Examples')
    sys.path.append(os.getcwd())

    dataset = Dataset(num_params=num_params, sensitive_param_idx=sensitive_param_idx, model_type=model_type, sensitive_param_name=sensitive_param_name, col_to_be_predicted=col_to_be_predicted, dataset_dir=dataset_dir)

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

    # run_aequitas_once(dataset, perturbation_unit, cleaned_csv_dir, pkl_dir, \
    #                 improved_pkl_dir, retrain_csv_dir, plot_dir, "Random", threshold,  \
    #                 global_iteration_limit, local_iteration_limit, num_trials, samples)

    run_aequitas_once(dataset=dataset, perturbation_unit=perturbation_unit, pkl_dir=pkl_dir, improved_pkl_dir=improved_pkl_dir, retrain_csv_dir=retrain_csv_dir, plot_dir=plot_dir, mode="Fully")
    
if __name__ == "__main__":
    main() 