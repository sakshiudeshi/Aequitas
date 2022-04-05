from .utils import *

class Dataset:
    def __init__(self, num_params, sensitive_param_idx, model_type, sensitive_param_name,
            col_to_be_predicted, dataset_dir, sensitive_param_idx_list = [], sensitive_param_name_list = []):
        
        self.sensitive_param_idx_list = sensitive_param_idx_list
        self.sensitive_param_name_list = sensitive_param_name_list
        if len(self.sensitive_param_idx_list) == 0:
            self.sensitive_param_idx_list.append(sensitive_param_idx)
            self.sensitive_param_name_list.append(sensitive_param_name)
        
        self.model_type = model_type
        self.num_params = num_params
        self.sensitive_param_idx = sensitive_param_idx # Starts at O
        self.sensitive_param_name = sensitive_param_name
        self.col_to_be_predicted = col_to_be_predicted
        self.dataset_dir = dataset_dir

        self.column_names = get_column_names(dataset_dir)
        self.input_bounds = get_input_bounds(dataset_dir)
        self.col_to_be_predicted_idx = get_idx_of_col_to_be_predicted(dataset_dir, col_to_be_predicted)
    
    def update_sensitive_parameter(self, id):
        self.sensitive_param_idx = self.sensitive_param_idx_list[id]
        self.sensitive_param_name = self.sensitive_param_name_list[id]