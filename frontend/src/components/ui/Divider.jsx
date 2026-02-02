// checked
import React from 'react';
import '../../styles/Divider.css';

export const Divider = ({ text = 'or' }) => {
  return (
    <div className="divider-container">
      <div className="divider-line"></div>
      <span className="divider-text">
        {text}
      </span>
    </div>
  );
};

