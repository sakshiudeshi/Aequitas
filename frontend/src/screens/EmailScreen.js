import React, { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import { sendEmail } from "../actions/emailActions";
import Header from "../components/Header";
import OurNavbar from "../components/OurNavbar";

export default function EmailScreen() {
  const { filename } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const {
    aequitasRunResult,
    loading: runAequitasLoading,
    error: runAequitasError,
  } = useSelector((state) => state.aequitasRunResult);

  useEffect(() => {
    // if (aequitasRunResult) {
    //   e.preventDefault();
    //   const form = useRef();
    //   form.to_name = "User";
    //   form.message = "Aequitas successfully run!";
    //   sendEmail(form);
    //   navigate(`/result/${filename}`);
    // }
  }, [aequitasRunResult]);

  const [email, setEmail] = useState("");

  // https://www.emailjs.com/docs/tutorial/creating-contact-form/
  const submitHandler = (e) => {
    e.preventDefault();
    setEmail(document.getElementById("inputEmail").value);
    if (aequitasRunResult) {
      const form = document.getElementById('emailForm')
      form.message.value = "Aequitas successfully run!";
      form.to_name.value = "User";
      console.log(form);
      sendEmail(form);
      navigate(`/result/${filename}`);
    }
  };

  return (
    <div>
      <OurNavbar></OurNavbar>
      <Header>Email</Header>
      <div className="container">
        <form id="emailForm" onSubmit={(e) => submitHandler(e)}>
          <div class="mb-3">
            <input type="hidden" name="message"></input>
            <input type="hidden" name="to_name"></input>
            <label htmlFor="inputEmail" className="form-label">
              Please enter the email address you would like to receive the
              improved dataset to.
            </label>
            <input
              name="user_email"
              type="email"
              className="form-control"
              id="inputEmail"
              aria-describedby="emailHelp"
            />
            <div id="emailHelp" className="form-text">
              We'll never share your email with anyone else.
            </div>
          </div>
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>
      </div>
    </div>
  );
}
