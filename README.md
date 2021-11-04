# Aequitas

We present Aequitas, a directed fairness testing framework machine learning models. See the paper [Automated Directed Fairness Testing](https://arxiv.org/abs/1807.00468) for more details.

## Prerequisites

1. Creat a new virtual environment.

* `python3 -m venv <name of environment>`

* `source <name of environment>/bin/activate`

2. Download all the necessary modules straight from the requirements.txt.

* `pip install -r requirements.txt`

* replace the file `_numdiff.py` in the directory `<environment_name>/lib/scipy/optimize` with the file `_numdiff.py` that is in this root directory

## Background
There are 3 test generation strategies in our suite, namely Aequitas Random, Aequitas Semi-Directed and Aequitas Fully Directed. There are files to evaluate [Fair SVM](https://github.com/mbilalzafar/fair-classification) and Scikit-Learn classifiers trained on the same [dataset](http://archive.ics.uci.edu/ml/datasets/Adult).

## Config
The [config](config.py) file has the following data:

* params : The number of parameters in the data
* sensitive_param: The parameter under test.
* input_bounds: The bounds of each parameter
* classifier_name: Pickled scikit-learn classifier under test (only applicable to the sklearn files)
* threshold: Discrimination threshold.
* perturbation_unit: By what unit would the user like to perturb the input in the local search.
* retraining_inputs: Inputs to be used for the retraining. Please see [this file](Retrain_Example_File.txt).

## Demo
`python <filename>`

eg. `python Aequitas_Fully_Directed.py`

## Contact
* Please contact sakshi_udeshi@mymail.sutd.edu.sg for any comments/questions



