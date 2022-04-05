import React, { useEffect, useState } from "react";
import Axios from "axios";
import { useNavigate } from "react-router-dom";
import OurNavbar from "../components/OurNavbar";

export default function HomeScreen() {
  const [uploadStatus, setUploadStatus] = useState("");
  const [configStatus, setConfigStatus] = useState("");

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
      // Axios.get(`http://localhost:5000/api/run?filename=${filename}`)
      Axios.get(`http://localhost:5000/api/config?filename=${filename}`) // for flask: /api/config is the api address, after ? is the arguments <argument_name>=<argument_value>
        .then((response) => {
          console.log("Success", response);
          setConfigStatus(response);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  useEffect(() => {
    if (configStatus.status === 200) {
      navigate(`/config/${configStatus.data.message}`);
    }
  }, [configStatus, navigate]);

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
              <label htmlFor="modelFile">Model Training Dataset</label>
              <input
                type="file"
                id="modelFile"
                label="Choose File"
                onChange={uploadFileHandler}
              ></input>
            </div>
            {uploadStatus.status === 200 ? (
              <div className="alert alert-success" role="alert">
                {uploadStatus.data.message} uploaded successfully.{" "}
              </div>
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
                Continue
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
