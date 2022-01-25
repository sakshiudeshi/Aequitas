import React from "react";
import Header from "../components/Header";
import OurNavbar from "../components/OurNavbar";
export default function AequitasDocumentationScreen() {
  return (
    <div>
      <OurNavbar></OurNavbar>
      <Header child={<h1>Aequitas Documentations</h1>}></Header>
    </div>
  );
}
