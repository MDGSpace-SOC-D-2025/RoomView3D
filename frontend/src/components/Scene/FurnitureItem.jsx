import React from "react";
import "../../styles/FurnitureItem.css";


const FurnitureItem = ({ image, title, onClick }) => {
  return (
    <div className="furniture-item" onClick={onClick}>
      <img src={image} alt={title} className="furniture-image" />
      <span className="furniture-title">{title}</span>
    </div>
  );
};

export default FurnitureItem;
``