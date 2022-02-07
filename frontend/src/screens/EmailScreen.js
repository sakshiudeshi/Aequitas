import React, { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import { sendEmail } from "../actions/emailActions";
import { updateUserConfig } from "../actions/submitActions";
import Header from "../components/Header";
import OurNavbar from "../components/OurNavbar";

export default function EmailScreen() {
  const { jobId } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const {
    aequitasRunResult,
    loading: runAequitasLoading,
    error: runAequitasError,
  } = useSelector((state) => state.aequitasRunResult);

  const {
    configUpdateResult,
    loading: configUpdateLoading,
    error: configUpdateError,
  } = useSelector((state) => state.configUpdate);

  const sendEmailResult = useSelector((state) => state.sendEmail);
  const {
    loading: sendEmailLoading,
    success: sendEmailSuccess,
    error: sendEmailError,
  } = sendEmailResult;

  useEffect(() => {
    // if (aequitasRunResult) {
    //   e.preventDefault();
    //   const form = useRef();
    //   form.to_name = "User";
    //   form.message = "Aequitas successfully run!";
    //   sendEmail(form);
    //   navigate(`/result/${filename}`);
    // }
    // setEmail(document.getElementById("inputEmail").value);
  }, [aequitasRunResult]);

  const [email, setEmail] = useState("");

  // https://www.emailjs.com/docs/tutorial/creating-contact-form/
  const submitHandler = (e) => {
    e.preventDefault();
    setEmail(document.getElementById("inputEmail").value);
    const bodyFormData = new FormData();
    bodyFormData.append("jobId", jobId);
    bodyFormData.append("email", email);
    dispatch(updateUserConfig(bodyFormData));
    if (aequitasRunResult) {
      const form = document.getElementById("emailForm");
      form.message.value = `Aequitas successfully run! This is the jobId ${jobId}`;
      form.to_name.value = "User";
      dispatch(sendEmail(form));
      //navigate(`/result/${jobId}`);
    }
  };

  return (
    <div>
      <OurNavbar></OurNavbar>
      <Header>Email</Header>
      <div className="container">
        {!sendEmailSuccess ? (
          <form id="emailForm" onSubmit={(e) => submitHandler(e)}>
            <div className="mb-3">
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
                onChange={(e) => setEmail(e.target.value)}
              />
              <div id="emailHelp" className="form-text">
                We'll never share your email with anyone else.
              </div>
            </div>
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </form>
        ) : (
          <div className="alert alert-success" role="alert">
            Email will be sent to you shortly (~appx 15 minutes) with the summary
            and improved dataset. Thank you!
          </div>
        )}
      </div>
    </div>
  );
}
