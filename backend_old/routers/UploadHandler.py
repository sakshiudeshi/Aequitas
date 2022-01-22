from flask_restful import Api, Resource, reqparse
from flask import request, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import json
import csv


class UploadHandler(Resource):
  def get(self):
    return {
        'status': 'Success',
        'message': "Api connected"
    }

  def post(self):
    # key point!!! https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
    dataset = request.files['dataset']

    filename = f"{dataset.filename}"
    # somehow this searches from the backend folder..okay
    dataset.save(os.path.join('TrainingInputs', secure_filename(filename)))

    final_ret = {"status": "Success", "message": filename}
    return final_ret
