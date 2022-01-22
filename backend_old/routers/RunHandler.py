from flask_restful import Api, Resource, reqparse
from flask import request, send_from_directory
import sys, os
os.chdir("../backend/aequitas")
sys.path.append(os.getcwd())
import Aequitas_Random_Sklearn 
import Aequitas_Semi_Directed_Sklearn 
import Aequitas_Fully_Directed_Sklearn
import Retrain_Sklearn
import Sklearn_Estimation
import config

# secure file input!!
class RunHandler(Resource):
  def post(self):
    return 

  def get(self):
    datasetName = request.args.get('filename')
    fairnessEstimation = Sklearn_Estimation.run()

    # User-input directed option 1
    aequitasMode = "random"; # this should be determined by the config file (aka user input)
    
    # if aequitasMode == "random":
    #   Aequitas_Random_Sklearn.run()
    # elif aequitasMode == "semiDirected":
    #   Aequitas_Semi_Directed_Sklearn.run()
    # elif aequitasMode == "fullyDirected":
    #   Aequitas_Fully_Directed_Sklearn.run()

    # # User-input directed option 2
    # trainModel = True 
    # modelType = "DecisionTree"

    # if modelType == "DecisionTree": # need to be modified
    #   Retrain_Sklearn.run()
    # else:
    #   Retrain_Sklearn.run()

    # how to return files from local directory
    # https://medium.com/analytics-vidhya/receive-or-return-files-flask-api-8389d42b0684
    
    retrainFileName = config.retraining_inputs
    retrainModelName = config.improved_classfier_name

    # return the results
    return {
      'status': 'Success',
      'datasetName': str(datasetName),
      'aequitasMode': aequitasMode,
      'fairnessEstimation': fairnessEstimation,
      'retrainFilename': retrainFileName,
      'retrainModelName': retrainModelName
    }