import React from 'react';
import '../../styles/Input.css';

export const Input = ({ 
  type = 'text', 
  name, 
  placeholder, 
  value, 
  onChange, 
  onKeyPress 
}) => {
  return (
    <input
      type={type}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      onKeyPress={onKeyPress}
      className="glass-input"
    />
  );
};