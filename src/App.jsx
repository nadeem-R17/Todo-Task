import React from "react";
import Navbar from "./components/Navbar";
import Login from "./components/Login";
import "./index.css";
import Home from "./components/Home/Home";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useAuth } from "./AuthContext";

function App() {
  const { isLoggedIn } = useAuth();

  return (
    <>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Login />} />
          {isLoggedIn && (
            <>
              <Route path="/home" element={<Home />} />
            </>
          )}
        </Routes>
      </Router>
    </>
  );
}
export default App;
