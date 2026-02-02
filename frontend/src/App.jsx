
import React, { useEffect } from 'react';
import { Routes, Route } from "react-router-dom";
import { AuthPage } from './pages/AuthPage';
import Dashboard from "./pages/Dashboard";
import Entry from "./pages/entry";          
import CreateProject from "./pages/CreateProject"; 
import Editor from "./components/Scene/editor";  

function App() {
  return (
     <Routes>
      <Route path="/" element={<AuthPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/detect-room" element={<Entry />} />
      <Route path="/create-room" element={<CreateProject />} />
      <Route path="/editor" element={<Editor />} />
    </Routes>
  );
}

export default App;


