import emailjs from "@emailjs/browser";
import { init } from "@emailjs/browser";

export const sendEmail = (form) => {
  init(process.env.REACT_APP_MAIL_USER_ID);
  const SERVICE_ID = process.env.REACT_APP_EMAIL_SERVICE_ID;
  const TEMPLATE_ID = process.env.REACT_APP_EMAIL_TEMPLATE_ID;
  const USER_ID = process.env.REACT_APP_MAIL_USER_ID;
  emailjs.sendForm(SERVICE_ID, TEMPLATE_ID, form, USER_ID).then(
    (result) => {
      console.log(result.text);
    },
    (error) => {
      console.log(error.text);
    }
  );
};
