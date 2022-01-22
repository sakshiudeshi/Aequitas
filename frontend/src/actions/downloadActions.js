import Axios from "axios";
import {
  DOWNLOAD_DATASET_FAIL,
  DOWNLOAD_DATASET_REQUEST,
  DOWNLOAD_DATASET_SUCCESS,
  DOWNLOAD_MODEL_FAIL,
  DOWNLOAD_MODEL_REQUEST,
  DOWNLOAD_MODEL_SUCCESS,
} from "../constants/downloadConstants";

export const downloadRetrainDataset =
  (filename) => async (dispatch, getState) => {
    dispatch({
      type: DOWNLOAD_DATASET_REQUEST,
      payload: {
        filename: filename,
      },
    });
    try {
      var fileDownload = require("js-file-download");
      Axios.get(
        `http://localhost:8000/api/download?target=dataset&filename=${filename}`,
        {
          responseType: "blob",
        }
      )
        .then((res) => {
          fileDownload(res.data, filename);
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });

      dispatch({ type: DOWNLOAD_DATASET_SUCCESS, success: true});
    } catch (error) {
      const message =
        error.response && error.response.data.message
          ? error.response.data.message
          : error.message;
      dispatch({ type: DOWNLOAD_DATASET_FAIL, payload: message });
    }
  };

export const downloadRetrainModel =
  (filename) => async (dispatch, getState) => {
    dispatch({
      type: DOWNLOAD_MODEL_REQUEST,
      payload: {
        filename: filename,
      },
    });
    try {
      var fileDownload = require("js-file-download");
      Axios.get(
        `http://localhost:8000/api/download?target=model&filename=${filename}`,
        {
          responseType: "blob",
        }
      )
        .then((res) => {
          fileDownload(res.data, filename);
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
      dispatch({ type: DOWNLOAD_MODEL_SUCCESS, success: true });
    } catch (error) {
      const message =
        error.response && error.response.data.message
          ? error.response.data.message
          : error.message;
      dispatch({ type: DOWNLOAD_MODEL_FAIL, payload: message });
    }
  };
