import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./Pages/HomePage";
import Register from "./Pages/Register";
import Login from "./Pages/Login";
import Dashboard from "./Pages/Dashboard";
import CatalogueBuilder from "./Pages/CatalogueBuilder";
import BusinessSetup from "./Pages/BusinessSetup";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route path="/business-setup" element={<BusinessSetup />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/catalogueBuilder" element={<CatalogueBuilder />} />
    </Routes>
  );
};

export default App;
