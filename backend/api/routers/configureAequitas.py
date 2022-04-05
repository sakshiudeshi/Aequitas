from turtle import update
from unittest import result
from django.core.files import File
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
import os
import sys
import json
from api.aequitas.utils import *
from api.models import AequitasJob

def sendColumnNames(request):
  jobId = request.GET['jobId']
  example = True if request.GET['example'] == "True" else False
  if example:
    job = AequitasJob.objects.get(id=jobId)
    result_directory = "api/aequitas/result"
    datasetName = "Employee.csv"
  else:
    job = AequitasJob.objects.get(id=jobId)
    result_directory = job.result_directory
    datasetName = job.dataset_name
  
  columnNames = get_column_names(f'{result_directory}/{datasetName}')

  response = JsonResponse({'status': 'Success',
                           'submittedFile': datasetName,
                           'jobId': jobId,
                           'columnNames': columnNames})
  return response

def updateConfig(request):
    jobId = request.POST['jobId']
    email = request.POST['email']
    
    job = AequitasJob.objects.get(id=jobId)
    job.owner_email = email # update user email
    job.save()
    
    return HttpResponse(job.owner_email)

def configureAequitas(request):
    if request.method == 'GET':
      return sendColumnNames(request)

    if request.method == 'POST':
      if 'email' in request.POST: # if it's an update request
        return updateConfig(request)
      
      jobId = request.POST['jobId']
      if jobId != 1: 
        job = AequitasJob.objects.get(id=jobId)
        dataset_name = request.POST['filename']
        job.dataset_name = dataset_name
        sensitive_param = request.POST['sensitiveParam']
        job.sensitive_param = sensitive_param
        job.col_to_be_predicted = request.POST['predictedCol']
        job.get_model = True if request.POST['getModel'] == "true" else False
        model_type = request.POST['modelType']
        job.model_type = model_type
        job.aequitas_mode = request.POST['aequitasMode']
        job.threshold = request.POST['threshold']
        job.perturbation_unit = 1
        job.sample = 100
        job.num_trials = 100
        job.global_iteration_limit = 100
        job.local_iteration_limit = 100
        
        result_directory = f'api/aequitas/result_{jobId}'
        dataset_dir = f"{result_directory}/{dataset_name}"
        job.dataset_dir = dataset_dir
        job.num_params = len(get_column_names(dataset_dir)) - 1 # exclude 'y' col
        job.sensitive_param_idx = get_idx_of_column(dataset_dir, sensitive_param)
        job.pkl_dir = f"{result_directory}/{dataset_name.split('.')[0]}_{model_type}_Original.pkl"
        job.improved_pkl_dir = f"{result_directory}/{dataset_name.split('.')[0]}_{model_type}_Improved.pkl"
        job.retraining_inputs = f"{result_directory}/{dataset_name.split('.')[0]}_Retraining_Dataset.csv"
        #job.improvement_graph = f"{result_directory}/{dataset_name.split('.')[0]}_Fairness_Improvement.png"
        job.improvement_graph = 'api/aequitas/result/employee_fairness_improvement.png'
        
        job.save()

      response = JsonResponse({'status': 'Success',
                               'submittedFile': dataset_name,
                               'id': job.id})
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