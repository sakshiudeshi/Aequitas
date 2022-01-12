from flask_restful import Api, Resource, reqparse
from flask import request, jsonify
import datetime
import os
import json
import csv

# secure file input!!
class RunHandler(Resource):
  def get(self):
    datasetName = request.args.get('filename')
    # run Aequitas

    # return the results
    return {
      'status': 'Success',
      'message': datasetName
    }