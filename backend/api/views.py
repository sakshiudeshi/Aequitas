
from django.core.files import File
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
import os
import sys
os.chdir('api/aequitas')
sys.path.append(os.getcwd())
import Aequitas_Fully_Directed_Sklearn
import Aequitas_Semi_Directed_Sklearn
import Aequitas_Random_Sklearn
import config
import Sklearn_Estimation
import Retrain_Sklearn
from django.views.decorators.csrf import csrf_exempt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

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
      improvementGraph = config.improvement_graph
      
      
      filepath = os.path.join(
      os.getcwd(), config.IMPROVEMENT_GRAPH_DIRECTORY, improvementGraph)
      imageId = uploadImage(improvementGraph, filepath)
      # https://dev.to/imamcu07/embed-or-display-image-to-html-page-from-google-drive-3ign
      sharingLink = f'https://drive.google.com/uc?id={imageId}'

      response = JsonResponse({
                              'status': 'Success',
                              'datasetName': datasetName,
                              'aequitasMode': aequitasMode,
                              'fairnessEstimation': fairnessEstimation,
                              'retrainFilename': retrainFileName,
                              'retrainModelName': retrainModelName,
                              'improvementGraph': sharingLink
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

def uploadImage(filename, filepath):
  os.chdir('../')
  sys.path.append(os.getcwd())
  creds = None
  
  if os.path.exists('token.json'):
      creds = Credentials.from_authorized_user_file('token.json', SCOPES)
      
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=5000)
      # Save the credentials for the next run
      with open('token.json', 'w') as token:
          token.write(creds.to_json())
          
  try:
    service = build('drive', 'v3', credentials=creds)
    # get the Aequitas Folder 
    folder_id = None
    page_token = None
    while True:
      response = service.files().list(q="name = 'Aequitas' and mimeType = 'application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()
      for file in response.get('files', []):
        folder_id = file.get('id')

      page_token = response.get('nextPageToken', None)
      if page_token is None:
        break
        
    # give permission to folder first
    folder_permission = {
      'type': 'anyone',
      'role': 'reader'
    }
    
    service.permissions().create(
      fileId=folder_id,
      body=folder_permission,
      fields='id',
    ).execute()
      
    file_metadata = {'name': filename, 'parents': [folder_id]}
    media = MediaFileUpload(filepath, mimetype='image/png')
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    fileId = file.get('id')
    
    print('File ID: %s' % fileId)
    if 'aequitas' not in os.getcwd():
      os.chdir('aequitas')
      sys.path.append(os.getcwd())
    return file.get('id')

  except HttpError as error:
    if 'aequitas' not in os.getcwd():
      os.chdir('aequitas')
      sys.path.append(os.getcwd())
    # TODO(developer) - Handle errors from drive API.
    print(f'An error occurred: {error}')

  
