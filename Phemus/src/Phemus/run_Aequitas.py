from .Retrain_Sklearn import retrain_sklearn
from .Aequitas_Fully_Directed_Sklearn import aequitas_fully_directed_sklearn

def run_Aequitas_fully_direct(num_params, sensitive_param_idx, sensitive_param_name, perturbation_unit, threshold, \
                  global_iteration_limit, local_iteration_limit, input_bounds, input_pkl_dir, input_csv_dir, \
                  improved_pkl_dir, num_trials, samples, column_names, col_to_be_predicted_idx):

    aequitas_fully_directed_sklearn(num_params, sensitive_param_idx, sensitive_param_name, perturbation_unit, threshold, \
                  global_iteration_limit, local_iteration_limit, input_bounds, input_pkl_dir, input_csv_dir, column_names)

    retrain_sklearn(input_pkl_dir, improved_pkl_dir, input_csv_dir, num_trials, samples,\
                            sensitive_param_idx, num_params, input_bounds, col_to_be_predicted_idx)