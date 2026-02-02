import React, { useState, useEffect } from 'react';
import { AuthLayout } from '../components/auth/AuthLayout';
import { SignInForm } from '../components/auth/SignInForm';
import { SignUpForm } from '../components/auth/SignUpForm';
import { GoogleAuthButton } from '../components/auth/GoogleAuthButton';
import { Divider } from '../components/ui/Divider';
import { useAuth } from '../hooks/useAuth';
import '../styles/AuthPage.css';
import { useNavigate } from "react-router-dom";

export const AuthPage = () => {
  const [isSignUp, setIsSignUp] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const tokenFromUrl = params.get("token");
    console.log("Token from URL:", tokenFromUrl);

    if (tokenFromUrl) {
      localStorage.setItem("token", tokenFromUrl);
      window.history.replaceState({}, document.title, "/");
      navigate("/dashboard");
      return;
    }

    const token = localStorage.getItem("token");

    if (token) {
      navigate("/dashboard");
    }
  }, []);

  const { formData, handleInputChange, handleSignIn, handleSignUp, handleGoogleAuth } = useAuth();

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {                                                   // yha pr e ka mtlb kya he or ye pura function kya kr rha he
      isSignUp ? handleSignUp() : handleSignIn();
    }
  };

  const toggleAuthMode = () => {
    setIsSignUp(!isSignUp);
  };

  return (
    <AuthLayout>
      {isSignUp ? (
        <>
          <SignUpForm
            formData={formData}
            onInputChange={handleInputChange}
            onSubmit={handleSignUp}
            onKeyPress={handleKeyPress}
          />

          <Divider />

          <GoogleAuthButton
            onGoogleAuth={handleGoogleAuth}
            isSignUp={true}
          />

          <p className="auth-toggle-text">
            Already have an account? {' '}
            <button onClick={toggleAuthMode} className="auth-toggle-link">
              Sign In
            </button>
          </p>
        </>
      ) :
        (
          <>
            <SignInForm
              formData={formData}
              onInputChange={handleInputChange}
              onSubmit={handleSignIn}
              onKeyPress={handleKeyPress}
            />

            <Divider />

            <GoogleAuthButton
              onGoogleAuth={handleGoogleAuth}
              isSignUp={false}
            />

            <p className="auth-toggle-text">
              Don't have an account?{' '}
              <button onClick={toggleAuthMode} className="auth-toggle-link">
                Sign Up
              </button>
            </p>
          </>
        )}
    </AuthLayout>
  );
};