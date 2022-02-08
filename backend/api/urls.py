from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.uploadDataset, name='upload'),
    path('config', views.configureAequitas, name='config'),
    path('run', views.runAequitas, name='run'),
    path('getresult', views.getResult, name='getresult'),
    path('download', views.downloadFile, name='download')
]