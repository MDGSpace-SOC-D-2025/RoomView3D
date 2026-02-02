import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/createProject.css";

export default function CreateProject() {
  const [projectName, setProjectName] = useState("");
  const navigate = useNavigate();

  const handleCreate = () => {
    if (!projectName) {
      alert("Project name required");
      return;
    }

    navigate("/editor", {
      state: {
        scene: null,
        projectName,
      },
    });
  };

return (
  <div className="create-page">
    <div className="create-container">
      <div className="create-card">

        <h2>Free Space</h2>
        <p>Start with an empty room and design freely</p>

        <input
          type="text"
          placeholder="Project Name"
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
        />

        <button onClick={handleCreate}>
          Create
        </button>

      </div>
    </div>
  </div>
);

}
