import os, sys
os.chdir('..')
sys.path.append(os.getcwd())
from src.Phemus import *
#from Phemus import * <-- use this if loading Phemus from module

def main():
    
    # test with original config/files from saksudeshi
    num_params = 13
    sensitive_param_idx = 9 # Starts at O
    sensitive_param_name = "Gender"
    col_to_be_predicted = "n"
    dataset_dir = "cleaned_train.csv"
    model_type = "DecisionTree"
    os.chdir('Examples')
    sys.path.append(os.getcwd())

    dataset = Dataset(num_params=num_params, sensitive_param_idx=sensitive_param_idx, model_type=model_type, sensitive_param_name=sensitive_param_name, col_to_be_predicted=col_to_be_predicted, dataset_dir=dataset_dir)

    pkl_dir = 'Decision_tree_standard_unfair.pkl'
    improved_pkl_dir = 'cleaned_train_DecisionTree_Original_Improved.pkl'
    retrain_csv_dir = 'Retrain_Example_File.csv'
    plot_dir = 'clean_train_improvement.png'
    cleaned_csv_dir = 'clean_train_cleaned.csv'
    
    threshold = 0
    perturbation_unit = 1
    global_iteration_limit = 1000 # needs to be at least 1000 to be effective
    local_iteration_limit = 100

    num_trials = 100
    samples = 100

    #retrain_csv_dir = 'Employee_Retraining_Dataset_modified.csv'
    #run_aequitas_once(dataset=dataset, perturbation_unit=perturbation_unit, pkl_dir=pkl_dir, improved_pkl_dir=improved_pkl_dir, retrain_csv_dir=retrain_csv_dir, plot_dir=plot_dir, mode="Random")
    run_aequitas_once(dataset=dataset, perturbation_unit=perturbation_unit, pkl_dir=pkl_dir, improved_pkl_dir=improved_pkl_dir, retrain_csv_dir=retrain_csv_dir, plot_dir=plot_dir, mode="Semi")
    #run_aequitas_once(dataset=dataset, perturbation_unit=perturbation_unit, pkl_dir=pkl_dir, improved_pkl_dir=improved_pkl_dir, retrain_csv_dir=retrain_csv_dir, plot_dir=plot_dir, mode="Fully")
    #retrain_sklearn(dataset, pkl_dir, retrain_csv_dir, improved_pkl_dir, plot_dir, num_trials, samples)
    #get_fairness_estimation(dataset, pkl_dir, num_trials, samples)
    
if __name__ == "__main__":
    main() 