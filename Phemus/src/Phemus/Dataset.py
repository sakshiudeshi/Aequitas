from .utils import *

class Dataset:
    def __init__(self, num_param, sensitive_param_idx, model_type,\
            sensitive_param_name, col_to_be_predicted, dataset_dir):
        self.model_type = model_type
        self.num_param = num_param
        self.sensitive_param_idx = sensitive_param_idx # Starts at O
        self.sensitive_param_name = sensitive_param_name
        self.col_to_be_predicted = col_to_be_predicted
        self.dataset_dir = dataset_dir

        self.column_names = get_column_names(dataset_dir)
        self.input_bounds = get_input_bounds(dataset_dir, col_to_be_predicted)
        self.col_to_be_predicted_idx = get_idx_of_col_to_be_predicted(dataset_dir, col_to_be_predicted)