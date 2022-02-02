from django.core.files import File
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import json
from Phemus import *
import os
import sys

def runAequitas(request):
    if request.method == 'GET':
      datasetName = request.GET['filename']

      with open('api/aequitas/config.json') as json_file:
        metaData = json.load(json_file)

      num_params = metaData['num_params']
      sensitive_param_idx = metaData['sensitive_param_idx']
      sensitive_param_name = metaData['sensitive_param_name']
      col_to_be_predicted = metaData['col_to_be_predicted']
      dataset_dir = metaData['dataset_dir']

      # possibly refactor to just pass in the json file?
      dataset = Dataset(num_params, sensitive_param_idx,
                        sensitive_param_name, col_to_be_predicted, dataset_dir)

      pkl_dir = metaData['pkl_dir']
      retraining_inputs = metaData['retraining_inputs']
      improved_pkl_dir = metaData['improved_pkl_dir']

      threshold = metaData['threshold']
      perturbation_unit = metaData['perturbation_unit']
      # needs to be at least 1000 to be effective
      global_iteration_limit = metaData['global_iteration_limit']
      local_iteration_limit = metaData['local_iteration_limit']

      num_trials = metaData['num_trials']
      samples = metaData['sample']

      fairnessEstimation = None  # can we make this its own function
      aequitasMode = 'random'

      improvement_graph = metaData['improvement_graph']
      improvement_graph_name = improvement_graph.split('/')[-1]

      # if aequitasMode == "random":
      #   run_aequitas_fully_direct(dataset, perturbation_unit, pkl_dir, improved_pkl_dir, threshold,
      #                             global_iteration_limit, local_iteration_limit, num_trials, samples)
      # # elif aequitasMode == "semiDirected":
      # #   run_aequitas_fully_direct(dataset, perturbation_unit, pkl_dir, improved_pkl_dir, threshold,
      # #                             global_iteration_limit, local_iteration_limit, num_trials, samples)
      # # elif aequitasMode == "fullyDirected":
      # #   run_aequitas_fully_direct(dataset, perturbation_unit, pkl_dir, improved_pkl_dir, threshold,
      # #                             global_iteration_limit, local_iteration_limit, num_trials, samples)

      imageId = uploadImage(improvement_graph_name, improvement_graph)
      # https://dev.to/imamcu07/embed-or-display-image-to-html-page-from-google-drive-3ign
      sharingLink = f'https://drive.google.com/uc?id={imageId}'

      response = JsonResponse({
                              'status': 'Success',
                              'datasetName': datasetName,
                              'aequitasMode': aequitasMode,
                              'fairnessEstimation': fairnessEstimation,
                              'retrainFilename': retraining_inputs,
                              'retrainModelName': improved_pkl_dir,
                              'improvementGraph': sharingLink
                              })
      return response

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def uploadImage(filename, filepath):
  print(os.getcwd())
  os.chdir('api')
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
  
  os.chdir('..')
  sys.path.append(os.getcwd())

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

    print(os.getcwd())
    file_metadata = {'name': filename, 'parents': [folder_id]}
    media = MediaFileUpload(filepath, mimetype='image/png')
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    fileId = file.get('id')

    print('File ID: %s' % fileId)
    # if 'aequitas' not in os.getcwd():
    #   os.chdir('aequitas')
    #   sys.path.append(os.getcwd())
    return file.get('id')

  except HttpError as error:
    # if 'aequitas' not in os.getcwd():
    #   os.chdir('aequitas')
    #   sys.path.append(os.getcwd())
    # TODO(developer) - Handle errors from drive API.
    print(f'An error occurred: {error}')
