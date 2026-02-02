// components/FurnitureDropdown.jsx
import React, { useState } from "react";
import FurnitureItem from "./FurnitureItem";
import { furnitureList } from "./FurnitureData";
import "../../styles/FurnitureDropdown.css";

const FurnitureDropdown = ({ onSelect }) => {
  const [open, setOpen] = useState(false);

  return (
    <div className="furniture-dropdown">
      <button className="dropdown-btn" onClick={() => setOpen(!open)}>
        Furniture &#11167;
      </button>

      {open && (
        <div className="dropdown-menu">
          {furnitureList.map((item, index) => (
            <FurnitureItem
              key={index}
              image={item.image}
              title={item.title}
              onClick={() => {
                onSelect(item);
                setOpen(false);
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default FurnitureDropdown;
