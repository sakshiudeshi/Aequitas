import React from "react";
import { Link, useParams } from "react-router-dom";

export default function ResultScreen() {

  const { filename } = useParams();

  return (
    <div>
      <Link to="/">Back</Link>
      <h1>Aequitas Results for {filename}</h1>
    </div>
  );
}
