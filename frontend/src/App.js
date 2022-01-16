import "./App.css";
import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import HomeScreen from "./screens/HomeScreen";
import ResultScreen from "./screens/ResultScreen";
import AboutAequitasScreen from "./screens/AboutAequitasScreen";
import AequitasDocumentationScreen from "./screens/AequitasDocumentationScreen";
import AboutUsScreen from "./screens/AboutUsScreen";

function App() {
  return (
    <BrowserRouter>
      <main>
        <Routes>
          <Route path="/" element={<HomeScreen></HomeScreen>}></Route>
          <Route path="/aboutaequitas" element={<AboutAequitasScreen></AboutAequitasScreen>}></Route>
          <Route path="/aequitasdocs" element={<AequitasDocumentationScreen></AequitasDocumentationScreen>}></Route>
          <Route path="/aboutus" element={<AboutUsScreen></AboutUsScreen>}></Route>
          <Route
            path="/result/:filename"
            element={<ResultScreen></ResultScreen>}
          ></Route>
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
