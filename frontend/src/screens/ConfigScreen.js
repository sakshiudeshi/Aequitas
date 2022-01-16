import React, { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import OurNavbar from "../components/OurNavbar";
import Axios from 'axios';

export default function ConfigScreen() {

  const { filename } = useParams();
  const navigate = useNavigate();
  const [runStatus, setRunStatus] = useState("");

  const clickHandler = async () => {
    Axios.get(`http://localhost:5000/api/run?filename=${filename}`) // need to change it to post eventually, once we have the form
      .then((response) => {
        console.log("Success", response);
        setRunStatus(response);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  useEffect(() => {
    if (runStatus.status === 200) {
      navigate(`/result/${runStatus.data.message}`);
    }
  }, [runStatus, navigate]);

  return (
    <div>
      <OurNavbar></OurNavbar>
      <h1>Aequitas Configuration for {filename}</h1>
      <button type="button" className="btn btn-primary" onClick={clickHandler}>Run Aequitas</button>
    </div>
  );
}