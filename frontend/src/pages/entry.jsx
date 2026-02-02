import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/entry.css";

export default function Entry() {
  const [image, setImage] = useState(null);
  const [projectName, setProjectName] = useState("");
  const [loading, setLoading] = useState(false);
  const userId = localStorage.getItem("USER_ID");

  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!image || !projectName) {
      alert("All fields required");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);
    formData.append("project_name", projectName);
    formData.append("user_id", userId);
   
    try {
      setLoading(true);
      const res = await fetch("http://localhost:5000/api/ml/process", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      navigate("/editor", {
        state: {
          scene: data.scene,
          projectName,
        },
      });
    } catch (err) {
      alert("Backend error");
    } finally {
      setLoading(false);
    }
  };

return (
  <div className="entry-page">
    <div className="entry-container">

      <h1 className="entry-title">ROOMVIEW3D</h1>

      <div className="entry-card">

        <p>Upload your room image to generate 3D view</p>

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
        />

        <input
          type="text"
          placeholder="Project Name"
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
        />

        <button onClick={handleSubmit}>
          {loading ? "Processing..." : "Generate"}
        </button>

      </div>
    </div>
  </div>
);

}
