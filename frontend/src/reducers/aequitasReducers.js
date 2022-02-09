import { DELETE_AEQUITAS_RESULT_FAIL, DELETE_AEQUITAS_RESULT_REQUEST, DELETE_AEQUITAS_RESULT_RESET, DELETE_AEQUITAS_RESULT_SUCCESS, GET_AEQUITAS_RESULT_FAIL, GET_AEQUITAS_RESULT_REQUEST, GET_AEQUITAS_RESULT_SUCCESS, GET_IMPROVEMENT_GRAPH_FAIL, GET_IMPROVEMENT_GRAPH_REQUEST, GET_IMPROVEMENT_GRAPH_SUCCESS, RUN_AEQUITAS_FAIL, RUN_AEQUITAS_REQUEST, RUN_AEQUITAS_RESET, RUN_AEQUITAS_SUCCESS } from "../constants/aequitasConstants";

export const aequitasRunReducer = (state = {}, action) => {
  switch (action.type) {
    case RUN_AEQUITAS_REQUEST:
      return { loading: true };
    case RUN_AEQUITAS_SUCCESS:
      return { loading: false, aequitasRunResult: action.payload };
    case RUN_AEQUITAS_FAIL:
      return { loading: false, error: action.payload };
    case RUN_AEQUITAS_RESET:
      return {};
    default:
      return state;
  }
};

export const getAequitasResultReducer = (state = {}, action) => {
  switch (action.type) {
    case GET_AEQUITAS_RESULT_REQUEST:
      return { loading: true };
    case GET_AEQUITAS_RESULT_SUCCESS:
      return { loading: false, aequitasRunResult: action.payload };
    case GET_AEQUITAS_RESULT_FAIL:
      return { loading: false, error: action.payload };
    default:
      return state;
  }
};

export const deleteAequitasResultReducer = (state = {}, action) => {
  switch (action.type) {
    case DELETE_AEQUITAS_RESULT_REQUEST:
      return { loading: true };
    case DELETE_AEQUITAS_RESULT_SUCCESS:
      return { loading: false, success: action.payload.success, message: action.payload.message };
    case DELETE_AEQUITAS_RESULT_FAIL:
      return { loading: false, error: action.payload };
    case DELETE_AEQUITAS_RESULT_RESET:
      return {};
    default:
      return state;
  }
}