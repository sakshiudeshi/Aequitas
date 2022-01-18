import { RUN_AEQUITAS_FAIL, RUN_AEQUITAS_REQUEST, RUN_AEQUITAS_RESET, RUN_AEQUITAS_SUCCESS } from "../constants/runConstants";

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