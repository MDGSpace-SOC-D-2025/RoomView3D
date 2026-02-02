import React from 'react';
import logo from "../../assets/logo.png";
import '../../styles/AuthLayout.css';

export const AuthLayout = ({ children }) => {
  return (
    <div className="auth-layout">
      <div className="auth-background"></div>
      <div className="auth-overlay"></div>
      <div className="auth-content">
        <div className="auth-container">
          <div className="glass-card">
            <div className="auth-logo">
              <img src={logo} alt="RoomView3D Logo" />
            </div>
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};