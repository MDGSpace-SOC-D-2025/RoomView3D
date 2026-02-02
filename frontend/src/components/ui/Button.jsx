import React from 'react';
import '../../styles/Button.css';

export const Button = ({ 
  children, 
  onClick, 
  variant = 'primary',
  className = ''
}) => {
  return (
    <button
      onClick={onClick}
      className={`glass-button glass-button-${variant} ${className}`}
    >
      {children}
    </button>
  );
};