import React, { useRef } from "react";
import emailjs from "@emailjs/browser";
import { init } from "@emailjs/browser";
import { format } from "path";
import dotenv from 'dotenv';
// dotenv.config();

export const sendEmail = (form) => {
  init(process.env.REACT_APP_MAIL_USER_ID);
  console.log(process.env);
  const SERVICE_ID = process.env.REACT_APP_EMAIL_SERVICE_ID;
  const TEMPLATE_ID = process.env.REACT_APP_EMAIL_TEMPLATE_ID;
  const USER_ID = process.env.REACT_APP_MAIL_USER_ID;
  // const SERVICE_ID = `service_ufah6qa`;
  // const TEMPLATE_ID = `template_hugpvka`;
  // const USER_ID = `user_TtNggOOcDvbOoOep1KkTz`;
  console.log(SERVICE_ID);
  console.log(TEMPLATE_ID);
  console.log(USER_ID);
  emailjs.sendForm(SERVICE_ID, TEMPLATE_ID, form, USER_ID).then(
    (result) => {
      console.log(result.text);
    },
    (error) => {
      console.log(error.text);
    }
  );
};
