from django.http import JsonResponse
from api.models import AequitasJob 
import os
import shutil

def uploadDataset(request):
    if request.method == 'POST':
      if 'dataset' in request.FILES:
        dataset = request.FILES['dataset']
        filename = dataset.name
        j = AequitasJob(dataset_name=filename)
        j.save()
        j.result_directory = f'api/aequitas/result_{j.id}'
        j.save()
        os.mkdir(j.result_directory)
        with open(j.result_directory + "/" + filename, 'wb+') as destination:
          for chunk in dataset.chunks():
            destination.write(chunk)
      else:
        dataset = open("api/aequitas/result/Employee.csv", "r")
        filename = "Employee.csv"
        j = AequitasJob(dataset_name=filename)
        j.save()
        j.result_directory = f'api/aequitas/result_{j.id}'
        j.save()
        shutil.copytree("api/aequitas/result", j.result_directory) # for now just copy entire sample directory over
        # with open(j.result_directory + "/" + filename, 'w') as destination:
        #   for line in dataset.readlines():
        #     destination.write(line)

      response = JsonResponse(
          {'status': 'Success', 'jobId': j.id, 'filename': filename})
      return response
