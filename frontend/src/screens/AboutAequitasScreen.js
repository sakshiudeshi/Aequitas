import React from "react";
import Header from "../components/Header";
import OurNavbar from "../components/OurNavbar";

export default function AboutAequitasScreen() {
  return (
    <div>
      <OurNavbar></OurNavbar>
      <Header child={<h1>About Aequitas</h1>}></Header>
    </div>
  );
}
