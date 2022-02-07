import { CREATE_CONFIG_FAIL, CREATE_CONFIG_REQUEST, CREATE_CONFIG_SUCCESS, SUBMIT_DATASET_FAIL, SUBMIT_DATASET_REQUEST, SUBMIT_DATASET_SUCCESS, UPDATE_CONFIG_FAIL, UPDATE_CONFIG_REQUEST, UPDATE_CONFIG_SUCCESS } from "../constants/submitConstants";

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

export const configCreateReducer = (state = {}, action) => {
  switch (action.type) {
    case CREATE_CONFIG_REQUEST:
      return { loading: true };
    case CREATE_CONFIG_SUCCESS:
      return { loading: false, configCreateResult: action.payload };
    case CREATE_CONFIG_FAIL:
      return { loading: false, error: action.payload};
    default:
      return state;
  }
}

export const configUpdateReducer = (state = {}, action) => {
  switch (action.type) {
    case UPDATE_CONFIG_REQUEST:
      return { loading: true };
    case UPDATE_CONFIG_SUCCESS:
      return { loading: false, configUpdateResult: action.payload };
    case UPDATE_CONFIG_FAIL:
      return { loading: false, error: action.payload};
    default:
      return state;
  }
}