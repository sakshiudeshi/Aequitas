from django.core.files import File
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
import os
import sys
import json

def downloadFile(request):
    #https://farhanghazi17.medium.com/django-react-link-to-download-pdf-a4c8da48802a
    if request.method == 'GET':
      filename = request.GET['filename']
      downloadTarget = request.GET['target']
      with open('api/aequitas/config.json') as json_file:
        metaData = json.load(json_file)
        
      if downloadTarget == "dataset":
        # filepath = os.path.join(
        #     os.getcwd(), config.RETRAINING_DATASET_DIRECTORY, filename)
        f = open(metaData['retraining_inputs'], "r")
        file = File(f, name=filename)
        response = HttpResponse(file.read())
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

      elif downloadTarget == "model":
        # filepath = os.path.join(
        #     os.getcwd(), config.RETRAINED_MODEL_DIRECTORY, filename)
        f = open(metaData['improved_pkl_dir'], "rb")
        file = File(f, name=filename)
        response = HttpResponse(file.read())
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response