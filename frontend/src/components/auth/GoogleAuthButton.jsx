import React from 'react';
import { Button } from '../ui/Button';

export const GoogleAuthButton = ({ onGoogleAuth, isSignUp }) => {
  return (
    <Button 
      variant="secondary" 
      onClick={onGoogleAuth}
    >
      {isSignUp ? 'Sign up with Google' : 'Sign in with Google'}
    </Button>
  );
};