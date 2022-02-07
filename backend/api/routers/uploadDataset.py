from django.http import JsonResponse
from api.models import AequitasJob 
import os

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
        os.mkdir(j.result_directory)
        with open(j.result_directory + "/" + filename, 'w') as destination:
          for line in dataset.readlines():
            destination.write(line)

      response = JsonResponse(
          {'status': 'Success', 'jobId': j.id, 'filename': filename})
      return response
