import React, { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import {
  downloadRetrainDataset,
  downloadRetrainModel,
} from "../actions/downloadActions";
import { deleteAequitasResult, getAequitasResult } from "../actions/aequitasActions";
import Footer from "../components/Footer";
import Header from "../components/Header";
import LoadingBox from "../components/LoadingBox";
import OurNavbar from "../components/OurNavbar";
import { DELETE_AEQUITAS_RESULT_RESET } from "../constants/aequitasConstants";

export default function ResultScreen() {
  const { jobId } = useParams();

  const dispatch = useDispatch();
  const result = useSelector((state) => state.getAequitasResult);
  const { aequitasRunResult, loading, error } = result;
  const deleteResult = useSelector((state) => state.deleteAequitasResult);
  const {
    loading: deleteResultLoading,
    success: deleteResultSuccess,
    message: deleteResultMessage,
  } = deleteResult;

  const [resultReady, setResultReady] = useState(false);
  useEffect(() => {
    if (!aequitasRunResult) {
      dispatch(getAequitasResult(jobId));
    } else {
      setResultReady(true);
    }
  }, [aequitasRunResult]);
  
  const downloadDatasetHandler = () => {
    dispatch(downloadRetrainDataset(aequitasRunResult.retrainFilename, jobId));
  };

  const downloadRetrainedModelHandler = () => {
    dispatch(downloadRetrainModel(aequitasRunResult.retrainModelName, jobId));
  };

  window.addEventListener("beforeunload", function (e) {
    e.preventDefault();
    e.returnValue = "";
    dispatch(deleteAequitasResult(jobId));
  });

  return resultReady ? (
    <div>
      <OurNavbar></OurNavbar>
      <Header>
        Aequitas Results for {aequitasRunResult.datasetName} JobId: {jobId}
      </Header>
      <div className="container-md">
        <div className="row">
          <div className="col">
            <h4>
              <span className="badge bg-light text-dark">
                <strong>Aequitas Mode:</strong> {"  "}
                {aequitasRunResult.aequitasMode}
              </span>
            </h4>
          </div>
          <div className="col">
            <h4>
              <div className="badge bg-light text-dark">
                <strong>Initial Fairness Estimation is:</strong> {"  "}
                {aequitasRunResult.fairnessEstimation}
              </div>
            </h4>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-4">
            <figure className="figure justify-center">
              <img
                className="figure-img img-fluid rounded"
                src={aequitasRunResult.improvementGraph}
                alt="improvementGraph"
              />
              <figcaption className="figure-caption">
                Fairness Improvement Graph
              </figcaption>
            </figure>
          </div>
          <div className="row">
            <div className="col">
              <div className="card" style={{ width: "18rem" }}>
                <div className="card-body">
                  <h5 className="card-title">Improved Dataset</h5>
                  <p className="card-text">
                    This is the dataset containing the discriminatory inputs
                    discovered by Aequitas. Add this to your dataset as
                    adversarial input to improve your fairness.
                  </p>
                  <button
                    type="button"
                    className="btn btn-primary"
                    data-bs-toggle="tooltip"
                    data-bs-placement="bottom"
                    title="This is the dataset containing the discriminatory inputs discovered by Aequitas. Add this to your dataset as adversarial input to improve your fairness."
                    onClick={() => downloadDatasetHandler()}
                  >
                    Download Retraining Dataset{" "}
                  </button>
                </div>
              </div>
            </div>
            <div className="col">
              <div className="card" style={{ width: "18rem" }}>
                <div className="card-body">
                  <h5 className="card-title">Improved Dataset</h5>
                  <p className="card-text">
                    This is the model that has been improved fairness by
                    retraining it with the adversarial inputs.
                  </p>
                  <button
                    type="button"
                    className="btn btn-primary"
                    data-bs-toggle="tooltip"
                    data-bs-placement="bottom"
                    title="This is the model that has been improved fairness by retraining it with the adversarial inputs."
                    onClick={() => downloadRetrainedModelHandler()}
                  >
                    Download Retrained Model{" "}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <br/><br/>
      </div>
      <Footer></Footer>
    </div>
  ): "";
}
