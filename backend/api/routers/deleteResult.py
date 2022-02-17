from django.http import JsonResponse
import shutil


def deleteResult(request):
  if request.method == 'GET':
      jobId = request.GET['jobId']
      directory_path = f'api/aequitas/result_{jobId}'
      try:
        shutil.rmtree(directory_path)
        print("folder deleted")
      except:
        print("Folder already deleted")
      
      return JsonResponse({'success': True,
                           'message': f'Folder <result_{jobId}> deleted successfully.'});
      