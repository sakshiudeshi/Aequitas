import { SEND_EMAIL_FAIL, SEND_EMAIL_REQUEST, SEND_EMAIL_SUCCESS } from "../constants/emailConstants";

export const sendEmailReducer = (state = {}, action) => {
  switch (action.type) {
    case SEND_EMAIL_REQUEST:
      return { loading: true};
    case SEND_EMAIL_SUCCESS:
      return { loading: false, success: true};
    case SEND_EMAIL_FAIL:
      return { loading: false, error: action.payload};
    default:
      return state;
  }
}