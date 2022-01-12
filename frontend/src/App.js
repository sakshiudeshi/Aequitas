import "./App.css";
import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import HomeScreen from "./screens/HomeScreen";
import ResultScreen from "./screens/ResultScreen";

function App() {
  return (
    <BrowserRouter>
      <main>
        <Routes>
          <Route path="/" element={<HomeScreen></HomeScreen>}></Route>
          <Route path="/result/:filename" element={<ResultScreen></ResultScreen>}></Route>
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
