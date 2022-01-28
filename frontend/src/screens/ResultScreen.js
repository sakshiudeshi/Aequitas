import React, {useEffect, useState} from "react";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
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
      <Header
        child={<h1 className="display-4">Aequitas Results for {filename}</h1>}
      ></Header>
      <div className="container">
        <div className="row">
          Aequitas Mode: {aequitasRunResult.aequitasMode}
        </div>
        <div className="row">
          Fairness Estimation is: {aequitasRunResult.fairnessEstimation}
        </div>
        <div className="row">
          <figure className="figure justify-center">
            <img
            className="figure-img img-fluid rounded"
              src={aequitasRunResult.improvementGraph}
              alt="improvementGraph"
            />
            <figcaption className="figure-caption">Fairness Improvement Graph</figcaption>
          </figure>
        </div>
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => downloadDatasetHandler()}
              >
                Download Retraining Dataset{" "}
              </button>
            </div>
            <div className="col-md-6">
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
    </div>
  );
}
