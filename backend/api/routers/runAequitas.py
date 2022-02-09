from django.http import JsonResponse
from api.models import AequitasJob
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
      jobId = request.GET['jobId']
      job = AequitasJob.objects.get(id=jobId)
      dataset_name = job.dataset_name
      num_params = job.num_params
      sensitive_param_idx = job.sensitive_param_idx
      sensitive_param = job.sensitive_param
      col_to_be_predicted = job.col_to_be_predicted
      dataset_dir = job.dataset_dir

      # possibly refactor to just pass in the json file?
      dataset = Dataset(num_params, sensitive_param_idx,
                        sensitive_param, col_to_be_predicted, dataset_dir)

      pkl_dir = job.pkl_dir
      retraining_inputs = job.retraining_inputs
      improved_pkl_dir = job.improved_pkl_dir

      threshold = job.threshold
      perturbation_unit = job.perturbation_unit
      
      # needs to be at least 1000 to be effective
      global_iteration_limit = job.global_iteration_limit
      local_iteration_limit = job.local_iteration_limit

      num_trials = job.num_trials
      samples = job.sample
      aequitasMode = job.aequitas_mode

      improvement_graph = job.improvement_graph
      improvement_graph_name = improvement_graph.split('/')[-1]
      retrainFilename = retraining_inputs.split('/')[-1]
      retrainModelName = improved_pkl_dir.split('/')[-1]

    #   if aequitasMode == "Random":
    #     run_aequitas_fully_direct(dataset, perturbation_unit, pkl_dir, improved_pkl_dir, threshold,
    #                               global_iteration_limit, local_iteration_limit, num_trials, samples)
    #   # elif aequitasMode == "SemiDirected":
    #   #   run_aequitas_fully_direct(dataset, perturbation_unit, pkl_dir, improved_pkl_dir, threshold,
    #   #                             global_iteration_limit, local_iteration_limit, num_trials, samples)
    #   # elif aequitasMode == "FullyDirected":
    #   #   run_aequitas_fully_direct(dataset, perturbation_unit, pkl_dir, improved_pkl_dir, threshold,
    #   #                             global_iteration_limit, local_iteration_limit, num_trials, samples)
    
      fairnessEstimation = get_fairness_estimation(dataset, pkl_dir, num_trials, samples)  # can we make this its own function
      imageId = uploadImage(improvement_graph_name, improvement_graph, jobId)
      # https://dev.to/imamcu07/embed-or-display-image-to-html-page-from-google-drive-3ign
      sharingLink = f'https://drive.google.com/uc?id={imageId}'
      job.improvement_graph = sharingLink
      job.fairness_estimation = fairnessEstimation
      job.save()

      response = JsonResponse({
                              'status': 'Success',
                              'jobId': jobId,
                              'datasetName': dataset_name,
                              'aequitasMode': aequitasMode,
                              'fairnessEstimation': fairnessEstimation,
                              'retrainFilename': retrainFilename,
                              'retrainModelName': retrainModelName,
                              'improvementGraph': sharingLink
                              })
      return response

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def uploadImage(filename, filepath, jobId):
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

    file_metadata = {'name': jobId, 'parents': [folder_id]}
    media = MediaFileUpload(filepath, mimetype='image/png')
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    fileId = file.get('id')

    print('File ID: %s' % fileId)
    return file.get('id')

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f'An error occurred: {error}')
