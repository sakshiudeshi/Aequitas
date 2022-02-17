import { DOWNLOAD_DATASET_FAIL, DOWNLOAD_DATASET_REQUEST, DOWNLOAD_DATASET_RESET, DOWNLOAD_DATASET_SUCCESS, DOWNLOAD_MODEL_FAIL, DOWNLOAD_MODEL_REQUEST, DOWNLOAD_MODEL_RESET, DOWNLOAD_MODEL_SUCCESS } from "../constants/downloadConstants";

export const downloadDatasetReducer = (state = {}, action) => {
  switch (action.type) {
    case DOWNLOAD_DATASET_REQUEST:
      return { loading: true };
    case DOWNLOAD_DATASET_SUCCESS:
      return { loading: false, success: action.success };
    case DOWNLOAD_DATASET_FAIL:
      return { loading: false, error: action.payload };
    case DOWNLOAD_DATASET_RESET:
      return {};
    default:
      return state;
  }
};

export const downloadModelReducer = (state = {}, action) => {
  switch (action.type) {
    case DOWNLOAD_MODEL_REQUEST:
      return { loading: true };
    case DOWNLOAD_MODEL_SUCCESS:
      return { loading: false, success: action.success };
    case DOWNLOAD_MODEL_FAIL:
      return { loading: false, error: action.payload };
    case DOWNLOAD_MODEL_RESET:
      return {};
    default:
      return state;
  }
};