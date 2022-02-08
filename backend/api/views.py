from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import api.routers.uploadDataset as uploadDatasetRouter
import api.routers.configureAequitas as configureAequitasRouter
import api.routers.runAequitas as runAequitasRouter
import api.routers.downloadFile as downloadFileRouter
import api.routers.getResult as getResultRouter

# Create your views here.
def index(request):
  return HttpResponse("Hello, world")

@csrf_exempt
def uploadDataset(request):
  return uploadDatasetRouter.uploadDataset(request)

@csrf_exempt
def configureAequitas(request):
  return configureAequitasRouter.configureAequitas(request)

def runAequitas(request):
  return runAequitasRouter.runAequitas(request)

def getResult(request):
  return getResultRouter.getResult(request)

def downloadFile(request):
  return downloadFileRouter.downloadFile(request)

  