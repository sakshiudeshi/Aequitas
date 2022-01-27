import React, { useEffect, useState } from "react";
import Axios from "axios";
import { useNavigate } from "react-router-dom";
import OurNavbar from "../components/OurNavbar";
import { useDispatch, useSelector } from "react-redux";
import { submitFile } from "../actions/submitActions";

export default function HomeScreen() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [uploadSuccess, setUploadSuccess] = useState(false);
  const uploadFileHandler = async (e) => {
    // Upload the model training data
    const file = e.target.files[0];
    const bodyFormData = new FormData();
    bodyFormData.append("dataset", file);
    bodyFormData.append("filename", file.name);
    Axios.post("http://localhost:8000/api/upload", bodyFormData)
      .then((response) => {
        console.log("Success", response);
        setUploadSuccess(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const fileSubmitResult = useSelector((state) => state.fileSubmit);
  const { submitResult, loading, error } = fileSubmitResult;
  const submitHandler = async (e) => {
    if (uploadSuccess) {
      const filename = uploadSuccess.data.message;
      dispatch(submitFile(filename));
      setUploadSuccess(false);
    }
  };

  useEffect(() => {
    if (submitResult) {
      navigate(`/config/${submitResult.submittedFile}`);
    }
  }, [submitResult, navigate]);

  return (
    <div className="main">
      <OurNavbar></OurNavbar>
      <div className="jumbotron">
        <div className="container">
          <div className="row">
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
            {uploadSuccess.status === 200 ? (
              <div className="alert alert-success" role="alert">
                {uploadSuccess.data.message} uploaded successfully.{" "}
              </div>
            ) : (
              <div></div>
            )}
            {uploadSuccess ? (
              <button
                className="btn btn-primary btn-lg"
                type="button"
                disabled={!uploadSuccess}
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
