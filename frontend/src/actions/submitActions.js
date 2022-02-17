import Axios from "axios";
import {
  CREATE_CONFIG_FAIL,
  CREATE_CONFIG_REQUEST,
  CREATE_CONFIG_SUCCESS,
  SUBMIT_DATASET_FAIL,
  SUBMIT_DATASET_REQUEST,
  SUBMIT_DATASET_SUCCESS,
  UPDATE_CONFIG_FAIL,
  UPDATE_CONFIG_REQUEST,
  UPDATE_CONFIG_SUCCESS,
  UPDATE_USER_EMAIL_FAIL,
  UPDATE_USER_EMAIL_REQUEST,
  UPDATE_USER_EMAIL_SUCCESS,
} from "../constants/submitConstants";

export const submitFile = (jobId) => async (dispatch, getState) => {
  dispatch({
    type: SUBMIT_DATASET_REQUEST,
    payload: {
      jobId: jobId,
    },
  });
  try {
    const { data } = await Axios.get(
      `http://localhost:8000/api/config?jobId=${jobId}&example=True`
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

export const createUserConfig = (config) => async (dispatch, getState) => {
  dispatch({ type: CREATE_CONFIG_REQUEST, payload: config });
  try {
    const { data } = await Axios.post(
      `http://localhost:8000/api/config?jobId=${config.get("jobId")}`,
      config
    );
    dispatch({ type: CREATE_CONFIG_SUCCESS, payload: data });
  } catch (error) {
    const message =
      error.response && error.response.data.message
        ? error.response.data.message
        : error.message;
    dispatch({ type: CREATE_CONFIG_FAIL, payload: message });
  }
};

export const updateUserConfig = (config) => async (dispatch, getState) => {
  dispatch({ type: UPDATE_CONFIG_REQUEST, payload: config });
  try {
    const { data } = await Axios.post(
      `http://localhost:8000/api/config`,
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
