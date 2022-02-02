from django.core.files import File
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
import sys

def uploadDataset(request):
    if request.method == 'POST':
      print("inside uploadDataset.py", os.getcwd())
      os.chdir('api/aequitas')
      sys.path.append(os.getcwd())
      dataset = request.FILES['dataset']
      filename = dataset.name
      with open(f'result/{filename}', 'wb+') as destination:
        for chunk in dataset.chunks():
          destination.write(chunk)
      os.chdir('../../')

      response = JsonResponse({'status': 'Success', 'message': filename})
      return response