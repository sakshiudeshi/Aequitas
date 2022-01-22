from flask_restful import Api, Resource, reqparse
from flask import request, Response, send_file, send_from_directory, safe_join
import config
import os, sys
print(os.getcwd())

class DownloadHandler(Resource):
  # https://flask.palletsprojects.com/en/2.0.x/api/?highlight=send_from_directory#flask.send_from_directory
  # disable cache from inspect element 'Network'
  def get(self):
    filename = request.args.get('filename')
    downloadTarget = request.args.get('target')
    if downloadTarget == "dataset":
      filepath = safe_join(os.getcwd(), config.RETRAINING_DATASET_DIRECTORY, filename)
      f = open(filepath, "r")
      #send_file(path_or_file=filepath, as_attachment=True)
      # return {
      #   "dataset": f
      # }
      #res = send_from_directory(directory=safe_join(os.getcwd(), config.RETRAINING_DATASET_DIRECTORY), path=filename, as_attachment=True)
      #res.direct_passthrough = False
      #file = safe_join(os.getcwd(), config.RETRAINING_DATASET_DIRECTORY, filename)
      #res = Response(file, direct_passthrough=False)
      #res.content_type = 'text/csv; charset=utf-8'
      # print(res.direct_passthrough)
      # print(res.content_type)
      # print(res.data)
      return {
              "datasetName": filename,
              "dataset": "hi"
              }
    elif downloadTarget == "model":
      return send_from_directory(directory=safe_join(os.getcwd(), config.RETRAINING_MODEL_DIRECTORY), path=filename, as_attachment=True)
    




