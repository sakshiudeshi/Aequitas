import React from "react";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import {
  downloadRetrainDataset,
  downloadRetrainModel,
} from "../actions/downloadActions";
import Header from "../components/Header";
import OurNavbar from "../components/OurNavbar";

export default function ResultScreen() {
  const { filename } = useParams();
  const result = useSelector((state) => state.aequitasRunResult);
  const { aequitasRunResult, loading, error } = result;

  const dispatch = useDispatch();

  const downloadDatasetHandler = () => {
    dispatch(downloadRetrainDataset(aequitasRunResult.retrainFilename));
  };

  const downloadRetrainedModelHandler = () => {
    dispatch(downloadRetrainModel(aequitasRunResult.retrainModelName));
  };

  return (
    <div>
      <OurNavbar></OurNavbar>
      <Header child={
        <h1>Aequitas Results for {filename}</h1>
      }></Header>
        
      <div className="container">
        <div className="row">
          Aequitas Mode: {aequitasRunResult.aequitasMode}
        </div>
        <div className="row">
          Fairness Estimation is: {aequitasRunResult.fairnessEstimation}
        </div>
        <div className="row">
          <img
            src={aequitasRunResult.improvementGraph}
            alt="improvementGraph"
          />
          {aequitasRunResult.improvementGraph}
        </div>
        <div className="row">
          <div className="col-lg-6">
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => downloadDatasetHandler()}
            >
              Download Retraining Dataset{" "}
            </button>
          </div>
          <div className="col-lg-6">
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => downloadRetrainedModelHandler()}
            >
              Download Retrained Model{" "}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
