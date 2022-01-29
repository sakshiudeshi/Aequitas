import Axios from "axios";
import {
  GET_IMPROVEMENT_GRAPH_FAIL,
  GET_IMPROVEMENT_GRAPH_REQUEST,
  GET_IMPROVEMENT_GRAPH_SUCCESS,
  RUN_AEQUITAS_FAIL,
  RUN_AEQUITAS_REQUEST,
  RUN_AEQUITAS_SUCCESS,
} from "../constants/runConstants";
import path from "path";

export const runAequitas = (datasetName) => async (dispatch, getState) => {
  dispatch({
    type: RUN_AEQUITAS_REQUEST,
    payload: {
      datasetName: datasetName,
    },
  });
  try {
    const { data } = await Axios.get(
      `http://localhost:8000/api/run?filename=${datasetName}`
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
