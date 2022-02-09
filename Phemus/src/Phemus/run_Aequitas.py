from .Retrain_Sklearn import retrain_sklearn
from .Aequitas_Fully_Directed_Sklearn import aequitas_fully_directed_sklearn
from .Aequitas_Semi_Directed_Sklearn import aequitas_semi_directed_sklearn
from .Aequitas_Random_Sklearn import aequitas_random_sklearn
from .Generate_Sklearn_Classifier import generate_sklearn_classifier

from .Dataset import Dataset

def run_aequitas_fully_direct(dataset: Dataset, perturbation_unit, cleaned_csv_dir, pkl_dir, improved_pkl_dir, retrain_csv_dir, plot_dir, \
        threshold = 0, global_iteration_limit = 1000, local_iteration_limit = 100, num_trials = 100, samples = 100):
    generate_sklearn_classifier(dataset, cleaned_csv_dir, pkl_dir)
    aequitas_fully_directed_sklearn(dataset, perturbation_unit, threshold, global_iteration_limit, local_iteration_limit, pkl_dir, retrain_csv_dir)
    retrain_sklearn(dataset, pkl_dir, retrain_csv_dir, improved_pkl_dir, plot_dir, num_trials, samples)

def run_aequitas_semi_direct(dataset: Dataset, perturbation_unit, cleaned_csv_dir, pkl_dir, improved_pkl_dir, retrain_csv_dir, plot_dir, \
        threshold = 0, global_iteration_limit = 1000, local_iteration_limit = 100, num_trials = 100, samples = 100):
    generate_sklearn_classifier(dataset, cleaned_csv_dir, pkl_dir)
    aequitas_semi_directed_sklearn(dataset, perturbation_unit, threshold, global_iteration_limit, local_iteration_limit, pkl_dir, retrain_csv_dir)
    retrain_sklearn(dataset, pkl_dir, retrain_csv_dir, improved_pkl_dir, plot_dir, num_trials, samples)

def run_aequitas_random(dataset: Dataset, perturbation_unit, cleaned_csv_dir, pkl_dir, improved_pkl_dir, retrain_csv_dir, plot_dir, \
        threshold = 0, global_iteration_limit = 1000, local_iteration_limit = 100, num_trials = 100, samples = 100):
    generate_sklearn_classifier(dataset, cleaned_csv_dir, pkl_dir)
    aequitas_random_sklearn(dataset, perturbation_unit, threshold, global_iteration_limit, local_iteration_limit, pkl_dir, retrain_csv_dir)
    retrain_sklearn(dataset, pkl_dir, retrain_csv_dir, improved_pkl_dir, plot_dir, num_trials, samples)