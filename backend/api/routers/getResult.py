from django.core.files import File
from django.http import HttpResponse, FileResponse, JsonResponse
from api.models import AequitasJob

def getResult(request):
  if request.method == 'GET':
      jobId = request.GET['jobId']
      job = AequitasJob.objects.get(id=jobId)
      
      response = JsonResponse({
                              'status': 'Success',
                              'jobId': jobId,
                              'datasetName': job.dataset_name,
                              'aequitasMode': job.aequitas_mode,
                              'fairnessEstimation': job.fairness_estimation,
                              'retrainFilename': job.retraining_inputs.split('/')[-1],
                              'retrainModelName': job.improved_pkl_dir.split('/')[-1],
                              'improvementGraph': job.improvement_graph
                              })
      return response