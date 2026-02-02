import React from 'react';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import '../../styles/Forms.css';

export const SignInForm = ({ 
  formData, 
  onInputChange, 
  onSubmit, 
  onKeyPress 
}) => {
  return (
    <div className="form-container">
      <Input
        type="email"
        name="email"
        placeholder="Email"
        value={formData.email}
        onChange={onInputChange}
        onKeyPress={onKeyPress}
      />
      
      <Input
        type="password"
        name="password"
        placeholder="Password"
        value={formData.password}
        onChange={onInputChange}
        onKeyPress={onKeyPress}
      />
      
      <Button onClick={onSubmit}>
        Sign In
      </Button>
    </div>
  );
};