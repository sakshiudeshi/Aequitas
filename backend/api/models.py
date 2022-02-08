import uuid
from django.db import models

# Create your models here.
class AequitasJob(models.Model):
  dataset_name = models.CharField(max_length=100)
  sensitive_param = models.CharField(max_length=100, null=True)
  col_to_be_predicted = models.CharField(max_length=100, null=True)
  get_model = models.BooleanField(null=True)
  model_type = models.CharField(max_length=50, null=True)
  aequitas_mode = models.CharField(max_length=50, null=True)
  threshold = models.IntegerField(null=True)
  result_directory = models.CharField(max_length=100, null=True)
  dataset_dir = models.CharField(max_length=200, null=True)
  num_params = models.IntegerField(null=True)
  sensitive_param_idx = models.IntegerField(null=True)
  pkl_dir = models.CharField(max_length=200, null=True)
  improved_pkl_dir = models.CharField(max_length=200, null=True)
  retraining_inputs = models.CharField(max_length=200, null=True)
  improvement_graph = models.CharField(max_length=200, null=True)
  fairness_estimation = models.DecimalField(decimal_places=2, max_digits=2, null=True)
  perturbation_unit = models.IntegerField(null=True)
  sample = models.IntegerField(null=True)
  num_trials = models.IntegerField(null=True)
  global_iteration_limit = models.IntegerField(null=True)
  local_iteration_limit = models.IntegerField(null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  owner_email = models.EmailField(null=True)
  