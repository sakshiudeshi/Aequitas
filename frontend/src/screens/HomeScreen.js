import React, { useEffect, useState } from "react";
import Axios from "axios";
import { useNavigate } from "react-router-dom";
import OurNavbar from "../components/OurNavbar";

export default function HomeScreen() {
  const [uploadStatus, setUploadStatus] = useState("");
  const [runStatus, setRunStatus] = useState("");

  const navigate = useNavigate();

  const uploadFileHandler = async (e) => {
    // Upload the model training data
    const file = e.target.files[0];
    const bodyFormData = new FormData();
    bodyFormData.append("dataset", file);

    Axios.post("http://localhost:5000/api/upload", bodyFormData)
      .then((response) => {
        console.log("Success", response);
        setUploadStatus(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const submitHandler = async (e) => {
    // Todo
    // Actually run Aequitas
    if (uploadStatus) {
      const filename = uploadStatus.data.message;
      Axios.get(`http://localhost:5000/api/run?filename=${filename}`)
        .then((response) => {
          console.log("Success", response);
          setRunStatus(response);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  useEffect(() => {
    if (runStatus.status === 200) {
      navigate(`/result/${runStatus.data.message}`);
    }
  }, [runStatus, navigate]);

  return (
    <div className="main">
      <OurNavbar></OurNavbar>
      <div className="container">
        <div className="row">
          <div className="jumbotron">
            <h1 className="display-4">Aequitas Web</h1>
            <p className="lead">
              Upload your training data to find out about its fairness!
            </p>
            <div>
              <label htmlFor="modelFile">Model Training Dataset </label>
              <input
                type="file"
                id="modelFile"
                label="Choose File"
                onChange={uploadFileHandler}
              ></input>
            </div>
            {uploadStatus.status === 200 ? (
              <div>{uploadStatus.data.message} uploaded successfully. </div>
            ) : (
              <div></div>
            )}
            {uploadStatus ? (
              <button
                className="btn btn-primary btn-lg"
                type="button"
                disabled={uploadStatus === ""}
                onClick={submitHandler}
              >
                Get Started
              </button>
            ) : (
              ""
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
