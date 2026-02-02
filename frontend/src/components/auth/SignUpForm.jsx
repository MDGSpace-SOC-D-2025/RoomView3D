import React from 'react';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import '../../styles/Forms.css';

export const SignUpForm = ({ 
  formData, 
  onInputChange, 
  onSubmit, 
  onKeyPress 
}) => {
  return (
    <div className="form-container">
      <Input
        type="text"
        name="firstName"
        placeholder="First Name"
        value={formData.firstName}
        onChange={onInputChange}
        onKeyPress={onKeyPress}
      />
      
      <Input
        type="text"
        name="lastName"
        placeholder="Last Name"
        value={formData.lastName}
        onChange={onInputChange}
        onKeyPress={onKeyPress}
      />
      
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
        Sign Up
      </Button>
    </div>
  );
};