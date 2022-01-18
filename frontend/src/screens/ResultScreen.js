import React from "react";
import { useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import OurNavbar from "../components/OurNavbar";

export default function ResultScreen() {

  const { filename } = useParams();
  const result = useSelector(state => state.aequitasRunResult);
  const { aequitasRunResult, loading, error } = result;

  return (
    <div>
      <OurNavbar></OurNavbar>
      <h1>Aequitas Results for {filename}</h1>
      <div>
        Fairness Estimation is: {aequitasRunResult.fairnessEstimation}
      </div>
    </div>
  );
}
