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

    """
    This section is, at the moment, a combination of the UploadHandler and
    ConfigHandler APIs. Will sort out after getting thoughts in order, 
    prior to code outlining stage of development.
    NOTE: Figure out which steps should be in UploadHandler intead
    """
    # TODO: Get information for user convenience
    # -- Make sure file with given name exists, throw error if not.
    # -- Check that file size does not exceed size limit.
    # -- Get column labels.
    #   -- Makes sure first non-empty row of csv contains only strings.
    #     -- Handle if user inputs label-less file.
    #     -- Handle if user inputs empty csv file.
    # -- Makes sure that each column contains identically typed values.
    #   -- Allow doubles and ints in same column?
    #   -- How should we handling empty column entries?
    # TODO: Get information for config menu setup 
    # -- Send Labels to configuration setup page
    #   -- Create dictionary/array with each column label "columnLabels"
    #   -- NOTE: Maybe also store the type of data within each column? This could
    #            allow for drop-downs (if not checkboxes) for chosen columns
    #            to "lock-out" options? For example, preventing the user
    #            from claiming a parameter of strings are numerical ranges?
    #      -- Also, do different model types require different sensitive or predicted params?
    #         If so, save information here as well.
    #   -- coulmn_ret = {"status": "Success", "message": columnLabels}
    #   -- Use this to create drop-down selectors for config page later.
    #   -- Return this and success message to the user.

    # TODO: Write drop-down values and previously saved values
    #   to the config file
    # -- Write to Config File
    #   -- Write the csv filename to config file
    #   -- Write machine learning model to config file 
    #   -- Write model file names to file
    #     -- Get machine learning model from drop-down
    #     -- classifier_name (example being "filename_DecisionTree_Original.pkl")
    #     -- retraining_inputs (example being "filename_Retraining_Dataset.csv")
    #   -- Write column information
    #     -- Get number of columns (excluding sensitive parameter) (autonomous)
    #     -- sensitive_param_name (from user)
    #     -- sensitive_param_idx (autonomous)
    #     -- col_to_be_predicted (from user)
    #     -- col_to_be_predicted_idx (autonomous)
    #   -- Whether sensitive_param is categorical
    #   -- Whether col_to_be_predicted is categorical
    #   -- Write Aequitas mode (Random, Fully_Directed, or Semi_Directed)
    #     -- NOTE: this is if RunHandler uses same code for all three: if different, have
    #        RunHandler be called differently from config page "run" button instead?
    # -- Save Config File
    #   -- Name Config File
    #   -- Check no identically named config file exists
    #   -- Save / Create config file
    #   -- Send name of config file to RunHandler
    
    # return the results
    return {
      'status': 'Success',
      'message': datasetName
      # Should this be the config name instead? Check how this works. 
    }