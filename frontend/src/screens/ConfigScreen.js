import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import OurNavbar from "../components/OurNavbar";
import { runAequitas } from "../actions/runActions";
import LoadingBox from "../components/LoadingBox";
import Header from "../components/Header";
import { updateUserConfig } from "../actions/submitActions";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Footer from "../components/Footer";

export default function ConfigScreen() {
  const { filename } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const clickHandler = (filename) => {
    dispatch(runAequitas(filename));
  };

  const fileSubmitResult = useSelector((state) => state.fileSubmit);
  const { submitResult, loading, error } = fileSubmitResult;
  const columnNames = submitResult.columnNames;

  const {
    configUpdateResult,
    loading: configUpdateLoading,
    error: configUpdateError,
  } = useSelector((state) => state.configUpdate);

  const modelTypes = ["DecisionTree", "RandomForest", "SVM"];
  const aequitasModes = ["Random", "SemiDirected", "FullyDirected"];

  const [sensitiveParam, setSensitiveParam] = useState("");
  const [predictedCol, setPredictedCol] = useState("");
  const [getModel, setGetModel] = useState(true);
  const [modelType, setModelType] = useState("DecisionTree");
  const [aequitasMode, setAequitasMode] = useState("FullyDirected");
  const [threshold, setThreshold] = useState(0);

  const result = useSelector((state) => state.aequitasRunResult);
  const {
    aequitasRunResult,
    loading: runAequitasLoading,
    error: runAequitasError,
  } = result;

  useEffect(() => {
    // make sure the dropdowns are set to default values
    setSensitiveParam(document.getElementById("sensitiveParamSelect").value);
    setPredictedCol(document.getElementById("predictedColSelect").value);
    setGetModel(document.getElementById("getModelCheck").checked);
    setModelType(document.getElementById("modelTypeSelect").value);
    setAequitasMode(document.getElementById("aequitasModeSelect").value);
    setThreshold(document.getElementById("inputThreshold").value);

    if (aequitasRunResult) {
      navigate(`/result/${filename}`);
    } else {
      navigate(`/config/${filename}`);
    }
  }, [aequitasRunResult, navigate]);

  const submitHandler = (e) => {
    e.preventDefault();
    const bodyFormData = new FormData();
    bodyFormData.append("filename", filename);
    bodyFormData.append("sensitiveParam", sensitiveParam);
    bodyFormData.append("predictedCol", predictedCol);
    bodyFormData.append("getModel", getModel);
    bodyFormData.append("modelType", modelType);
    bodyFormData.append("aequitasMode", aequitasMode);
    bodyFormData.append("threshold", threshold);
    dispatch(updateUserConfig(bodyFormData));
  };

  return (
    <div>
      <OurNavbar></OurNavbar>
      <Header
        child={
          <h1 className="display-4">Aequitas Configuration for {filename}</h1>
        }
      ></Header>
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
              <label for="inputThreshold" className="form-label">
                What is the threshold for 'bias' (How different is 'different')? <br/>
                (ex. for a binary classifier, threshold is 0 - any difference is difference)
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
                    info
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
              {configUpdateResult && (
                <div className="alert alert-success" role="alert">
                  {configUpdateResult.submittedFile} successfully configured!
                </div>
              )}
              <button type="submit" className="btn btn-primary mb-2">
                Configure
              </button>
            </div>
          </form>
        </div>
        {configUpdateResult && (
          <div>
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => clickHandler(filename)}
            >
              Run Aequitas
            </button>
            {runAequitasLoading && <LoadingBox></LoadingBox>}
          </div>
        )}
      </div>
      <Footer></Footer>
    </div>
  );
}
