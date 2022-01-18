from flask_restful import Api, Resource, reqparse
from flask import request, jsonify
import datetime
import os
import json
import csv

# secure file input!!
class ConfigHandler(Resource):
  def get(self):
    datasetName = request.args.get('filename')
    # configure Aequitas 

    # TODO: Implement configuration 

    # return the results
    return {
      'status': 'Success',
      'submittedFile': str(datasetName)
    }