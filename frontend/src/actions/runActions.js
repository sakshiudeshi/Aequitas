import Axios from "axios";
import { RUN_AEQUITAS_FAIL, RUN_AEQUITAS_REQUEST, RUN_AEQUITAS_SUCCESS } from "../constants/runConstants";

export const runAequitas = (datasetName) => async (dispatch, getState) => {
  dispatch({
    type: RUN_AEQUITAS_REQUEST,
    payload: {
      datasetName: datasetName
    },
  });
  try {
    const { data } = await Axios.get(
      `http://localhost:5000/api/run?filename=${datasetName}`
    );
    dispatch({ type: RUN_AEQUITAS_SUCCESS, payload: data });
  } catch (error) {
    const message =
      error.response && error.response.data.message
        ? error.response.data.message
        : error.message;
    dispatch({ type: RUN_AEQUITAS_FAIL, payload: message});
  }
};
