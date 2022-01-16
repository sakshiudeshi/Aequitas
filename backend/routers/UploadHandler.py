from flask_restful import Api, Resource, reqparse
from flask import request, jsonify
from datetime import datetime
import os
import json
import csv

# secure file input!!
class UploadHandler(Resource):
  def get(self):
    return {
      'status': 'Success',
      'message': "Api connected"
    }

  def post(self):
    dataset = request.files['dataset'] # key point!!! https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
    
    filename = f"{dataset.filename}"
    dataset.save(os.path.join('aequitas/TrainingInputs', filename)) # somehow this searches from the backend folder..okay
    
    final_ret = {"status": "Success", "message": filename}
    return final_ret