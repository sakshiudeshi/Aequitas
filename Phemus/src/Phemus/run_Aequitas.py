from .Retrain_Sklearn import retrain_sklearn
from .Aequitas_Fully_Directed_Sklearn import aequitas_fully_directed_sklearn
from .Generate_Sklearn_Classifier import generate_sklearn_classifier
from .utils import get_input_bounds
from .utils import get_column_names
from .utils import get_idx_of_col_to_be_predicted

from .Dataset import Dataset

def run_aequitas_fully_direct(dataset: Dataset, perturbation_unit, pkl_dir, improved_pkl_dir, retrain_csv_dir, plot_dir, \
        threshold = 0, global_iteration_limit = 1000, local_iteration_limit = 100, num_trials = 100, samples = 100):
    generate_sklearn_classifier(dataset, pkl_dir)
    aequitas_fully_directed_sklearn(dataset, perturbation_unit, threshold, global_iteration_limit, local_iteration_limit, pkl_dir, retrain_csv_dir)
    retrain_sklearn(dataset, pkl_dir, improved_pkl_dir, plot_dir, num_trials, samples)