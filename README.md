# Aequitas

We present Aequitas, a directed fairness testing framework machine learning models. See the paper [Automated Directed Fairness Testing](https://arxiv.org/abs/1807.00468) for more details.



## Prerequisites

* Python 2.7.15
* numpy 1.14.5
* scipy 1.1.0
* scikit-learn 1.19.0

The authors used Pycharm CE 2017.2.3 as the development IDE.

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


## Citation 
If you use any part of this code, please cite the following paper

```
@inproceedings{aequitas,
  title={Automated directed fairness testing},
  author={Udeshi, Sakshi and Arora, Pryanshu and Chattopadhyay, Sudipta},
  booktitle={Proceedings of the 33rd ACM/IEEE International Conference on Automated Software Engineering},
  pages={98--108},
  year={2018}
}
```



