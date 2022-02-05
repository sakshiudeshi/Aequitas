import React from "react";
import Header from "../components/Header";
import OurNavbar from "../components/OurNavbar";

export default function EmailScreen() {

  const submitHandler = () => {

  }
  
  return (
    <div>
      <OurNavbar></OurNavbar>
      <Header>Email</Header>
      <div className="container">
      <form onSubmit={submitHandler}>
        <div class="mb-3">
          <label htmlFor="exampleInputEmail1" className="form-label">
            Please enter the email address you would like to receive the improved dataset to.
          </label>
          <input
            type="email"
            className="form-control"
            id="exampleInputEmail1"
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
