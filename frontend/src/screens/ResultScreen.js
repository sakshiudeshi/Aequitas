import React from "react";
import { Link, useParams } from "react-router-dom";
import OurNavbar from "../components/OurNavbar";

export default function ResultScreen() {

  const { filename } = useParams();

  return (
    <div>
      <OurNavbar></OurNavbar>
      <h1>Aequitas Results for {filename}</h1>
    </div>
  );
}
