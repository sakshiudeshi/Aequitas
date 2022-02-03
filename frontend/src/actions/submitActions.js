import Axios from "axios";
import {
  SUBMIT_DATASET_FAIL,
  SUBMIT_DATASET_REQUEST,
  SUBMIT_DATASET_SUCCESS,
  UPDATE_CONFIG_FAIL,
  UPDATE_CONFIG_REQUEST,
  UPDATE_CONFIG_SUCCESS,
} from "../constants/submitConstants";

export const submitFile = (datasetName) => async (dispatch, getState) => {
  dispatch({
    type: SUBMIT_DATASET_REQUEST,
    payload: {
      datasetName: datasetName,
    },
  });
  try {
    const { data } = await Axios.get(
      `http://localhost:8000/api/config?filename=${datasetName}`
    );
    dispatch({ type: SUBMIT_DATASET_SUCCESS, payload: data });
  } catch (error) {
    const message =
      error.response && error.response.data.message
        ? error.response.data.message
        : error.message;
    dispatch({ type: SUBMIT_DATASET_FAIL, payload: message });
  }
};

export const updateUserConfig = (config) => async (dispatch, getState) => {
  console.log(config.get('predictedCol'));
  dispatch({ type: UPDATE_CONFIG_REQUEST, payload: config });
  try {
    const { data } = await Axios.post(
      `http://localhost:8000/api/config?filename=${config.get('filename')}`,
      config
    );
    dispatch({ type: UPDATE_CONFIG_SUCCESS, payload: data });
  } catch (error) {
    const message =
      error.response && error.response.data.message
        ? error.response.data.message
        : error.message;
    dispatch({ type: UPDATE_CONFIG_FAIL, payload: message });
  }
};
