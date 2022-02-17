from django.core.files import File
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
import os
import sys
import json
from api.models import AequitasJob

def downloadFile(request):
    #https://farhanghazi17.medium.com/django-react-link-to-download-pdf-a4c8da48802a
    if request.method == 'GET':
      jobId = request.GET['jobId']
      downloadTarget = request.GET['target']
      j = AequitasJob.objects.get(id=jobId)
      
      if downloadTarget == "dataset":
        f = open(j.retraining_inputs, "r")
        filename = j.retraining_inputs.split("/")[-1]
        file = File(f, name=filename)
        response = HttpResponse(file.read())
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

      elif downloadTarget == "model":
        f = open(j.improved_pkl_dir, "rb")
        filename = j.improved_pkl_dir.split("/")[-1]
        file = File(f, name=filename)
        response = HttpResponse(file.read())
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response