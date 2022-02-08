import Axios from "axios";
import {
  GET_AEQUITAS_RESULT_FAIL,
  GET_AEQUITAS_RESULT_REQUEST,
  GET_AEQUITAS_RESULT_SUCCESS,
  RUN_AEQUITAS_FAIL,
  RUN_AEQUITAS_REQUEST,
  RUN_AEQUITAS_SUCCESS,
} from "../constants/runConstants";

export const runAequitas = (jobId) => async (dispatch, getState) => {
  dispatch({
    type: RUN_AEQUITAS_REQUEST,
    payload: {
      jobId: jobId,
    },
  });
  try {
    const { data } = await Axios.get(
      `http://localhost:8000/api/run?jobId=${jobId}`
    );
    dispatch({ type: RUN_AEQUITAS_SUCCESS, payload: data });
  } catch (error) {
    const message =
      error.response && error.response.data.message
        ? error.response.data.message
        : error.message;
    dispatch({ type: RUN_AEQUITAS_FAIL, payload: message });
  }
};

export const getAequitasResult = (jobId) => async (dispatch, getState) => {
  dispatch({
    type: GET_AEQUITAS_RESULT_REQUEST,
    payload: {
      jobId: jobId,
    },
  });
  try {
    const { data } = await Axios.get(
      `http://localhost:8000/api/getresult?jobId=${jobId}`
    );
    dispatch({ type: GET_AEQUITAS_RESULT_SUCCESS, payload: data });
  } catch (error) {
    const message =
      error.response && error.response.data.message
        ? error.response.data.message
        : error.message;
    dispatch({ type: GET_AEQUITAS_RESULT_FAIL, payload: message });
  }
};
