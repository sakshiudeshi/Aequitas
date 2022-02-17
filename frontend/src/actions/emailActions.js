import emailjs from "@emailjs/browser";
import { init } from "@emailjs/browser";
import {
  SEND_EMAIL_FAIL,
  SEND_EMAIL_REQUEST,
  SEND_EMAIL_SUCCESS,
} from "../constants/emailConstants";

export const sendEmail = (form) => async (dispatch, getState) => {
  init(process.env.REACT_APP_MAIL_USER_ID);
  dispatch({
    type: SEND_EMAIL_REQUEST,
    payload: { email: form },
  });
  try {
    const SERVICE_ID = process.env.REACT_APP_EMAIL_SERVICE_ID;
    const TEMPLATE_ID = process.env.REACT_APP_EMAIL_TEMPLATE_ID;
    const USER_ID = process.env.REACT_APP_MAIL_USER_ID;
    emailjs.sendForm(SERVICE_ID, TEMPLATE_ID, form, USER_ID).then(
      (result) => {
        console.log(result.text);
        dispatch({ type: SEND_EMAIL_SUCCESS });
      },
      (error) => {
        console.log(error.text);
      }
    );
  } catch (error) {
    const message =
      error.response && error.response.data.message
        ? error.response.data.message
        : error.message;
    dispatch({ type: SEND_EMAIL_FAIL, payload: message });
  }
};
