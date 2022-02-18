from .Retrain_Sklearn import retrain_sklearn
from .Aequitas_Fully_Directed_Sklearn import aequitas_fully_directed_sklearn
from .Aequitas_Semi_Directed_Sklearn import aequitas_semi_directed_sklearn
from .Aequitas_Random_Sklearn import aequitas_random_sklearn
from .Generate_Sklearn_Classifier import generate_sklearn_classifier

from .Dataset import Dataset

def run_aequitas_once(dataset, perturbation_unit, pkl_dir, improved_pkl_dir, retrain_csv_dir, 
                        plot_dir, mode = "Random", threshold = 0, global_iteration_limit = 1000, 
                        local_iteration_limit = 100, num_trials = 100, samples = 100):

    if mode == "Random":
        aequitas_random_sklearn(dataset, perturbation_unit, threshold, global_iteration_limit, 
                                    local_iteration_limit, pkl_dir, retrain_csv_dir)
    elif mode == "Semi":
        aequitas_semi_directed_sklearn(dataset, perturbation_unit, threshold, global_iteration_limit, 
                                    local_iteration_limit, pkl_dir, retrain_csv_dir)
    elif mode == "Fully":
        aequitas_fully_directed_sklearn(dataset, perturbation_unit, threshold, global_iteration_limit, 
                                    local_iteration_limit, pkl_dir, retrain_csv_dir)
    else:
        raise ValueError("Mode of Aequitas selected is not valid. Possible modes are Random, Semi and Fully")
    
    retrain_sklearn(dataset, pkl_dir, retrain_csv_dir, improved_pkl_dir, plot_dir, threshold, num_trials, samples)

def run_aequitas(dataset: Dataset, perturbation_unit, pkl_dir, improved_pkl_dir, retrain_csv_dir, plot_dir, \
        mode = "Random", threshold = 0, global_iteration_limit = 1000, local_iteration_limit = 100, num_trials = 100, samples = 100):

    num_of_sens_param = len(dataset.sensitive_param_idx_list)

    generate_sklearn_classifier(dataset, pkl_dir)

    # print(num_of_sens_param)
    for i in range(num_of_sens_param):
        # print(i)
        dataset.update_sensitive_parameter(i)
        run_aequitas_once(dataset, perturbation_unit, pkl_dir, improved_pkl_dir, \
            retrain_csv_dir, plot_dir, mode, threshold, \
            global_iteration_limit, local_iteration_limit, num_trials, samples)


