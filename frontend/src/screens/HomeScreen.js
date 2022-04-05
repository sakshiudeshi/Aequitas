import React, { useEffect, useState } from "react";
import Axios from "axios";
import { useNavigate } from "react-router-dom";
import OurNavbar from "../components/OurNavbar";
import { useDispatch, useSelector } from "react-redux";
import { submitFile } from "../actions/submitActions";
import DragAndDrop from "../components/DragAndDrop";
import Footer from "../components/Footer";

export default function HomeScreen() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [uploadSuccess, setUploadSuccess] = useState(false);
  const uploadFileHandler = async (file=null, example=false) => {
    // Upload the model training data
    const bodyFormData = new FormData();
    if (file && !example) {
      bodyFormData.append("dataset", file);
      bodyFormData.append("filename", file.name);
    }
    Axios.post("http://localhost:8000/api/upload", bodyFormData)
      .then((response) => {
        console.log("Success", response);
        setUploadSuccess(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const submitHandler = async (e) => {
    if (uploadSuccess) {
      const jobId = uploadSuccess.data.jobId;
      dispatch(submitFile(jobId));
      setUploadSuccess(false);
    }
  };

  const exampleDatasetSubmitHandler = async (e) => {
    uploadFileHandler(null, true);
    if (uploadSuccess) {
      const jobId = uploadSuccess.data.jobId;
      dispatch(submitFile(jobId));
      setUploadSuccess(false);
    }
  };

  const fileSubmitResult = useSelector((state) => state.fileSubmit);
  const { submitResult, loading, error } = fileSubmitResult;

  useEffect(() => {
    if (submitResult) {
      navigate(`/config/${submitResult.jobId}`);
    }
  }, [submitResult, navigate]);

  return (
    <div className="main">
      <OurNavbar></OurNavbar>
      <DragAndDrop handleDrop={uploadFileHandler}>
        <div className="jumbotron">
          <div className="container">
            <div className="row">
              <div className="col-md-8">
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
                    onChange={(e) => uploadFileHandler(e.target.files[0])}
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
              <div className="col-md-4" style={{ marginTop: "1rem" }}>
                <button
                  className="btn btn-lg btn-link"
                  type="button"
                  onClick={exampleDatasetSubmitHandler}
                >
                  Or..try this example! <br />
                </button>
                <label className="text-center">
                  <strong>Employee.csv</strong> <br />
                  Dataset to determine the retention factor of employees within
                  two years
                </label>
              </div>
            </div>
          </div>
        </div>
      </DragAndDrop>
      <Footer style="fixed"></Footer>
    </div>
  );
}
