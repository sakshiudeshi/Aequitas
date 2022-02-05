from django.core.files import File
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
import os
import sys
import json
from api.aequitas.utils import *


def sendColumnNames(request):
  datasetName = request.GET['filename']
  # figure out column names
  columnNames = get_column_names(f'api/aequitas/result/{datasetName}')

  response = JsonResponse({'status': 'Success',
                           'submittedFile': datasetName,
                           'columnNames': columnNames})
  return response


def configureAequitas(request):
    if request.method == 'GET':
      return sendColumnNames(request)

    if request.method == 'POST':
      dataset_name = request.POST['filename']
      sensitive_param = request.POST['sensitiveParam']
      col_to_be_predicted = request.POST['predictedCol']
      get_model = request.POST['getModel']
      model_type = request.POST['modelType']
      aequitasMode = request.POST['aequitasMode']
      threshold = request.POST['threshold']
      result_directory = 'api/aequitas/result'
      dataset_dir = f"{result_directory}/{dataset_name}"
      num_params = len(get_column_names(dataset_dir)) - 1 # exclude 'y' col
      sensitive_param_idx = get_idx_of_column(dataset_dir, sensitive_param)
      pkl_dir = f"{result_directory}/{dataset_name.split('.')[0]}_{model_type}_Original.pkl"
      improved_pkl_dir = f"{result_directory}/{dataset_name.split('.')[0]}_{model_type}_Improved.pkl"
      retraining_inputs = f"{result_directory}/{dataset_name.split('.')[0]}_Retraining_Dataset.csv"
      #improvement_graph = f"{result_directory}/{dataset_name.split('.')[0]}_Fairness_Improvement.png"
      improvement_graph = 'api/aequitas/result/employee_fairness_improvement.png'
      perturbation_unit = 1
      sample = 100
      num_trials = 100
      
      data = {
          'num_params': num_params,  # exclude "y" col
          'sensitive_param_idx': sensitive_param_idx,  # starts at O
          'sensitive_param_name': sensitive_param,
          'col_to_be_predicted': col_to_be_predicted,
          'result_directory': 'api/aequitas/result',
          'pkl_dir': pkl_dir,
          'dataset_dir': dataset_dir,
          'retraining_inputs': retraining_inputs,
          'improved_pkl_dir': improved_pkl_dir,
          'improvement_graph': improvement_graph,
          'aequitasMode': aequitasMode,
          'threshold': threshold,
          'perturbation_unit': 1,
          # need to be modified after running Aequitas
          'global_iteration_limit': 100,  # needs to be at least 1000 to be effective
          'local_iteration_limit': 100,
          'sample': sample,
          'num_trials': num_trials,
      }

      with open('api/aequitas/config.json', 'w') as outfile:
        json.dump(data, outfile)

      response = JsonResponse({'status': 'Success',
                               'submittedFile': dataset_name})
      return response


# TODO: Implement configuration
      """
      This section is, at the moment, a combination of the UploadHandler and
      ConfigHandler APIs. Will sort out after getting thoughts in order, 
      prior to code outlining stage of development.
      NOTE: Figure out which steps should be in UploadHandler intead
      """
      # TODO: Get information for user convenience
      # -- Make sure file with given name exists, throw error if not.
      # -- Check that file size does not exceed size limit.
      # -- Get column labels.
      #   -- Makes sure first non-empty row of csv contains only strings.
      #     -- Handle if user inputs label-less file.
      #     -- Handle if user inputs empty csv file.
      # -- Makes sure that each column contains identically typed values.
      #   -- Allow doubles and ints in same column?
      #   -- How should we handling empty column entries?
      # TODO: Get information for config menu setup
      # -- Send Labels to configuration setup page
      #   -- Create dictionary/array with each column label "columnLabels"
      #   -- NOTE: Maybe also store the type of data within each column? This could
      #            allow for drop-downs (if not checkboxes) for chosen columns
      #            to "lock-out" options? For example, preventing the user
      #            from claiming a parameter of strings are numerical ranges?
      #      -- Also, do different model types require different sensitive or predicted params?
      #         If so, save information here as well.
      #   -- coulmn_ret = {"status": "Success", "message": columnLabels}
      #   -- Use this to create drop-down selectors for config page later.
      #   -- Return this and success message to the user.

      # TODO: Write drop-down values and previously saved values
      #   to the config file
      # -- Write to Config File
      #   -- Write the csv filename to config file
      #   -- Write machine learning model to config file
      #   -- Write model file names to file
      #     -- Get machine learning model from drop-down
      #     -- classifier_name (example being "filename_DecisionTree_Original.pkl")
      #     -- retraining_inputs (example being "filename_Retraining_Dataset.csv")
      #   -- Write column information
      #     -- Get number of columns (excluding sensitive parameter) (autonomous)
      #     -- sensitive_param_name (from user)
      #     -- sensitive_param_idx (autonomous)
      #     -- col_to_be_predicted (from user)
      #     -- col_to_be_predicted_idx (autonomous)
      #   -- Whether sensitive_param is categorical
      #   -- Whether col_to_be_predicted is categorical
      #   -- Write Aequitas mode (Random, Fully_Directed, or Semi_Directed)
      #     -- NOTE: this is if RunHandler uses same code for all three: if different, have
      #        RunHandler be called differently from config page "run" button instead?
      # -- Save Config File
      #   -- Name Config File
      #   -- Check no identically named config file exists
      #   -- Save / Create config file
      #   -- Send name of config file to RunHandler