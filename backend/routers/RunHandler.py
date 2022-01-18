from flask_restful import Api, Resource, reqparse
from flask import request, jsonify
import sys, os
os.chdir("../backend/aequitas")
sys.path.append(os.getcwd())
import Aequitas_Random_Sklearn
import Sklearn_Estimation as Sklearn_Estimation
os.chdir("../")

# secure file input!!
class RunHandler(Resource):
  def post(self):
    return 

  def get(self):
    datasetName = request.args.get('filename')
    print(str(datasetName))
    # TODO: Run Aequitas
    # Aequitas_Random_Sklearn.run() # By this point, config file should have been populated with relevant info
    fairnessEstimation = Sklearn_Estimation.run()

    # return the results
    return {
      'status': 'Success',
      'datasetName': str(datasetName),
      'fairnessEstimation': fairnessEstimation,
    }