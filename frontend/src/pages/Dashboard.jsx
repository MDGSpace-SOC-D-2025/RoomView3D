import React from "react";
import logo from "../assets/logo.png";
import "../styles/Dashboard.css";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";


const Dashboard = () => {

  const navigate = useNavigate();
  useEffect(() => {
  const token = localStorage.getItem("token");

  if (!token) {
    navigate("/");
    return;
  }

  fetch("http://localhost:5000/auth/me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Unauthorized");
      }
      return res.json();
    })
    .catch(() => {
      localStorage.removeItem("token");
      navigate("/");
    });
}, [navigate]);

  const handleUploadImage = () => {
    console.log("Upload Image clicked");
    navigate("/detect-room");
  };

  const handleFreeSpace = () => {
    console.log("Free Space clicked");
    navigate("/create-room");
  };

  return (
    <div className="dashboard-wrapper">
      <div className="dashboard-overlay"></div>

      <div className="dashboard-content">
        <img src={logo} alt="RoomView3D Logo" className="dashboard-logo" />

        <div className="dashboard-cards">
          <div className="dashboard-card" onClick={handleUploadImage}>
            <h2>Upload Image</h2>
            <p>Upload your room image to generate 3D view</p>
          </div>

          <div className="dashboard-card" onClick={handleFreeSpace}>
            <h2>Free Space</h2>
            <p>Start with an empty room and design freely</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
