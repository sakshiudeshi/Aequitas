import uuid
from django.db import models

# Create your models here.
class AequitasJob(models.Model):
  dataset_name = models.CharField(max_length=100)
  sensitive_param = models.CharField(max_length=100)
  col_to_be_predicted = models.CharField(max_length=100)
  get_model = models.BooleanField()
  model_type = models.CharField(max_length=50)
  aequitas_mode = models.CharField(max_length=50)
  threshold = models.IntegerField()
  result_directory = models.CharField(max_length=100)
  dataset_dir = models.CharField(max_length=200)
  num_params = models.IntegerField()
  sensitive_param_idx = models.IntegerField()
  pkl_dir = models.CharField(max_length=200)
  improved_pkl_dir = models.CharField(max_length=200)
  retraining_inputs = models.CharField(max_length=200)
  improvement_graph = models.CharField(max_length=200)
  perturbation_unit = models.IntegerField()
  sample = models.IntegerField()
  num_trials = models.IntegerField()
  global_iteration_limit = models.IntegerField(null=True)
  local_iteration_limit = models.IntegerField(null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  owner_email = models.EmailField()
  