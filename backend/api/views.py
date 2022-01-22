
from django.views.decorators.csrf import csrf_exempt
import os
import sys
os.chdir('api/aequitas')
sys.path.append(os.getcwd())
import Retrain_Sklearn
import Sklearn_Estimation
import config
import Aequitas_Random_Sklearn
import Aequitas_Semi_Directed_Sklearn
import Aequitas_Fully_Directed_Sklearn
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
from django.core.files import File

# Create your views here.


def index(request):
  return HttpResponse("Hello, world")

@csrf_exempt
def uploadDataset(request):
    if request.method == 'POST':
      dataset = request.FILES['dataset']
      filename = dataset.name
      print(filename)
      with open(f'TrainingInputs/{filename}', 'wb+') as destination:
        for chunk in dataset.chunks():
          destination.write(chunk)

      response = JsonResponse({'status': 'Success', 'message': filename})
      # response['status'] = 'Success'
      # response['message'] = filename
      return response


def configureAequitas(request):
    if request.method == 'GET':
      datasetName = request.GET['filename']
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

      response = JsonResponse({'status': 'Success',
                               'submittedFile': datasetName})
      return response


def runAequitas(request):
    if request.method == 'GET':
      datasetName = request.GET['filename']
      fairnessEstimation = Sklearn_Estimation.run()
      aequitasMode = 'random'

      # if aequitasMode == "random":
      #   Aequitas_Random_Sklearn.run()
      # elif aequitasMode == "semiDirected":
      #   Aequitas_Semi_Directed_Sklearn.run()
      # elif aequitasMode == "fullyDirected":
      #   Aequitas_Fully_Directed_Sklearn.run()

      # # User-input directed option 2
      # trainModel = True
      # modelType = "DecisionTree"

      # if modelType == "DecisionTree": # need to be modified
      #   Retrain_Sklearn.run()
      # else:
      #   Retrain_Sklearn.run()

      retrainFileName = config.retraining_inputs
      retrainModelName = config.improved_classfier_name

      response = JsonResponse({
                              'status': 'Success',
                              'datasetName': datasetName,
                              'aequitasMode': aequitasMode,
                              'fairnessEstimation': fairnessEstimation,
                              'retrainFilename': retrainFileName,
                              'retrainModelName': retrainModelName
                              })
      return response

def downloadFile(request):
    #https://farhanghazi17.medium.com/django-react-link-to-download-pdf-a4c8da48802a
    if request.method == 'GET':
      filename = request.GET['filename']
      downloadTarget = request.GET['target']
      if downloadTarget == "dataset":
        filepath = os.path.join(
            os.getcwd(), config.RETRAINING_DATASET_DIRECTORY, filename)
        f = open(filepath, "r")
        file = File(f, name=filename)
        response = HttpResponse(file.read())
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

      elif downloadTarget == "model":
        filepath = os.path.join(
            os.getcwd(), config.RETRAINED_MODEL_DIRECTORY, filename)
        f = open(filepath, "rb")
        file = File(f, name=filename)
        response = HttpResponse(file.read())
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
