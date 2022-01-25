import React, { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import OurNavbar from "../components/OurNavbar";
import { runAequitas } from "../actions/runActions";
import LoadingBox from "../components/LoadingBox";
import Header from "../components/Header";

export default function ConfigScreen() {
  const { filename } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const clickHandler = (filename) => {
    dispatch(runAequitas(filename));
  };

  const result = useSelector((state) => state.aequitasRunResult);
  const { aequitasRunResult, loading: runAequitasLoading, error } = result;

  useEffect(() => {
    if (aequitasRunResult) {
      navigate(`/result/${filename}`);
    }
  }, [aequitasRunResult, navigate]);

  return (
    <div>
      <OurNavbar></OurNavbar>
      <Header child={
        <h1>Aequitas Configuration for {filename}</h1>
      }></Header>
      <div className="col-md-12 text-center">
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => clickHandler(filename)}
        >
          Run Aequitas
        </button>
      </div>
      {runAequitasLoading && <LoadingBox></LoadingBox>}
    </div>
  );
}
