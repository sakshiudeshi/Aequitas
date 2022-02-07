import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import OurNavbar from "../components/OurNavbar";
import { runAequitas } from "../actions/runActions";
import LoadingBox from "../components/LoadingBox";
import Header from "../components/Header";
import { createUserConfig } from "../actions/submitActions";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Footer from "../components/Footer";

export default function ConfigScreen() {
  const { jobId } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const fileSubmitResult = useSelector((state) => state.fileSubmit);
  const { submitResult, loading, error } = fileSubmitResult;
  const filename = submitResult.submittedFile;
  const columnNames = submitResult.columnNames;

  const {
    configCreateResult,
    loading: configUpdateLoading,
    error: configUpdateError,
  } = useSelector((state) => state.configCreate);

  const modelTypes = ["DecisionTree", "RandomForest", "SVM"];
  const aequitasModes = ["Random", "SemiDirected", "FullyDirected"];

  const [sensitiveParam, setSensitiveParam] = useState("");
  const [predictedCol, setPredictedCol] = useState("");
  const [getModel, setGetModel] = useState(true);
  const [modelType, setModelType] = useState("DecisionTree");
  const [aequitasMode, setAequitasMode] = useState("FullyDirected");
  const [threshold, setThreshold] = useState(0);

  useEffect(() => {
    setSensitiveParam(document.getElementById("sensitiveParamSelect").value);
    setPredictedCol(document.getElementById("predictedColSelect").value);
    setGetModel(document.getElementById("getModelCheck").checked);
    setModelType(document.getElementById("modelTypeSelect").value);
    setAequitasMode(document.getElementById("aequitasModeSelect").value);
    setThreshold(document.getElementById("inputThreshold").value);
  }, [document]);

  const submitHandler = (e) => {
    e.preventDefault();
    const bodyFormData = new FormData();
    bodyFormData.append("jobId", jobId);
    bodyFormData.append("filename", filename);
    bodyFormData.append("sensitiveParam", sensitiveParam);
    bodyFormData.append("predictedCol", predictedCol);
    bodyFormData.append("getModel", getModel);
    bodyFormData.append("modelType", modelType);
    bodyFormData.append("aequitasMode", aequitasMode);
    bodyFormData.append("threshold", threshold);
    dispatch(createUserConfig(bodyFormData));
  };

  const clickHandler = () => {
    dispatch(runAequitas(jobId));
    navigate(`/email/${jobId}`);
  };

  return (
    <div>
      <OurNavbar></OurNavbar>
      <Header>Aequitas Configuration for {filename}</Header>
      <div className="container">
        <div>
          <form onSubmit={submitHandler}>
            <div className="form-group">
              <label htmlFor="sensitiveParamSelect">
                What is the sensitive parameter you would like to check the
                biasedness of?
              </label>
              <select
                className="form-control"
                id="sensitiveParamSelect"
                onChange={(e) => setSensitiveParam(e.target.value)}
                defaultValue={
                  filename === "Employee.csv" ? "Gender" : columnNames[0]
                }
              >
                {columnNames.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <div className="row">
                <div className="col">
                  <label htmlFor="predictedColSelect">
                    What are you trying to predict? (aka what is your 'y'?)
                  </label>
                  <select
                    className="form-control"
                    id="predictedColSelect"
                    onChange={(e) => setPredictedCol(e.target.value)}
                    defaultValue={
                      filename === "Employee.csv"
                        ? "LeaveOrNot"
                        : columnNames[0]
                    }
                  >
                    {columnNames.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
            <div className="form-group">
              <label htmlFor="inputThreshold" className="form-label">
                What is the threshold for 'bias' (How different is 'different')?{" "}
                <br />
                (ex. for a binary classifier, threshold is 0 - any difference is
                difference)
              </label>
              <input
                type="text"
                className="form-control"
                id="inputThreshold"
                defaultValue={0}
                onChange={(e) => setThreshold(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label htmlFor="aequitasModeSelect">
                <div>
                  What type of Aequitas would you like to run?{" "}
                  <a
                    role="button"
                    data-toggle="modal"
                    data-target="#exampleModal"
                    className="primary"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      className="bi bi-info-circle"
                      viewBox="0 0 16 16"
                    >
                      <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
                      <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z" />
                    </svg>
                    {" "} info
                  </a>
                </div>
              </label>
              <div
                className="modal fade"
                id="exampleModal"
                tabIndex="-1"
                aria-labelledby="exampleModalLabel"
                aria-hidden="true"
              >
                <div className="modal-dialog">
                  <div className="modal-content">
                    <div className="modal-header">
                      <h5
                        className="modal-title primary"
                        id="exampleModalLabel"
                      >
                        Different Aequitas Types
                      </h5>
                    </div>
                    <div className="modal-body">
                      <strong>Aequitas Random</strong>: No directionality in
                      searching for inputs
                      <div className="dropdown-divider"></div>
                      <strong>Aequitas Semi-Directed:</strong> Some
                      directionality in searching for inputs
                      <div className="dropdown-divider"></div>
                      <strong>Aequitas Fully-Directed:</strong> Fully
                      incorprates directionality in searching for inputs
                    </div>
                    <div className="modal-footer">
                      <button
                        type="button"
                        className="btn btn-secondary"
                        data-dismiss="modal"
                      >
                        Close
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <select
                className="form-control"
                id="aequitasModeSelect"
                onChange={(e) => setAequitasMode(e.target.value)}
                defaultValue={aequitasModes[2]}
              >
                {aequitasModes.map((m) => (
                  <option key={m} value={m}>
                    {m}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-check">
              <input
                className="form-check-input"
                type="checkbox"
                checked={getModel}
                id="getModelCheck"
                onChange={(e) => setGetModel(e.target.checked)}
              />
              <label className="form-check-label" htmlFor="getModelCheck">
                Do you want to train a model with the improved dataset?
              </label>
            </div>
            {getModel && (
              <div className="form-group">
                <label htmlFor="modelTypeSelect">Select a model type.</label>
                <select
                  className="form-control"
                  id="modelTypeSelect"
                  onChange={(e) => setModelType(e.target.value)}
                  defaultValue={modelTypes[0]}
                >
                  {modelTypes.map((m) => (
                    <option key={m} value={m}>
                      {m}
                    </option>
                  ))}
                </select>
              </div>
            )}
            <div>
              {configUpdateLoading && <LoadingBox></LoadingBox>}
              {configCreateResult && (
                <div className="alert alert-success" role="alert">
                  {configCreateResult.submittedFile} successfully configured!
                </div>
              )}
              <button type="submit" className="btn btn-primary mb-2">
                Configure
              </button>
            </div>
          </form>
        </div>
        {configCreateResult && (
          <div>
            <button
              type="button"
              className="btn btn-primary"
              onClick={clickHandler}
            >
              Run Aequitas
            </button>
            {/* {runAequitasLoading && <LoadingBox></LoadingBox>} */}
          </div>
        )}
      </div>
      <Footer></Footer>
    </div>
  );
}
