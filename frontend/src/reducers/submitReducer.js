import { SUBMIT_DATASET_FAIL, SUBMIT_DATASET_REQUEST, SUBMIT_DATASET_SUCCESS } from "../constants/submitConstants";

export const fileSubmitReducer = (state = {}, action) => {
  switch (action.type) {
    case SUBMIT_DATASET_REQUEST:
      return { loading: true };
    case SUBMIT_DATASET_SUCCESS:
      return { loading: false, submitResult: action.payload };
    case SUBMIT_DATASET_FAIL:
      return { loading: false, error: action.payload };
    default:
      return state;
  }
};