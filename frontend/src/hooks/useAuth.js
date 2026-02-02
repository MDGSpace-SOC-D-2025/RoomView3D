import { useState } from 'react';
import { useNavigate } from "react-router-dom";

export const useAuth = () => {
  const [formData, setFormData] = useState({ firstName: '', lastName: '', email: '', password: '' });

  const API_BASE_URL = 'http://127.0.0.1:5000/auth'; 
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 1. Sign Up Logic
  const handleSignUp = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      if (response.ok) {
        localStorage.setItem('token', data.token); 
        localStorage.setItem("USER_ID", data.user.id);  
        alert('Signup Successful!');
        navigate("/dashboard");
      } else {
        alert(data.error);
      }
    } catch (err) {
      console.error("Signup Error:", err);
    }
  };

  // 2. Sign In Logic
  const handleSignIn = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: formData.email, password: formData.password }),
      });
      const data = await response.json();
      if (response.ok) {
        localStorage.setItem('token', data.token);
        localStorage.setItem("USER_ID", data.user.id); 
        alert('Login Successful!');
        navigate("/dashboard");
      } else {
        alert(data.error);
      }
    } catch (err) {
      console.error("Login Error:", err);
    }
  };

  // 3. Google Auth Logic
  const handleGoogleAuth = () => {
    window.location.href = `${API_BASE_URL}/google/login`;
     navigate("/dashboard");
  };

  return { formData, handleInputChange, handleSignIn, handleSignUp, handleGoogleAuth };
};