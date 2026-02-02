# RoomView3D

RoomView3D is a full-stack web application that provides an interactive 3D room visualization experience.  
It combines a **Python backend** with a **React (Vite) frontend** to simulate and render room views in real time, enabling users to explore and interact with 3D environments through the browser.

---

## About the Project

RoomView3D is designed to bridge data-driven logic with modern 3D visualization on the web.  
The backend handles core logic, APIs, and data processing, while the frontend focuses on rendering interactive 3D scenes and UI controls.

### Key Highlights
- Modular **Python backend**
- Modern **React + Vite frontend**
- Interactive 3D visualization (Three.js based)
- Clean separation of backend and frontend
- Easy local setup for development

---

## Tech Stack

### Backend
- Python  
- Flask (API layer)
- Managed using `requirements.txt`

### Frontend
- React
- Vite
- Three.js
- Managed using `package.json`

---


---

## Getting Started

Follow the steps below to run RoomView3D locally.

---

## 1. Clone the Repository
```bash
git clone https://github.com/MDGSpace-SOC-D-2025/RoomView3D.git
```
## 2. Run Backend
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Make your env folder as per env exampple file given in main directory. 
Backend will start on http://localhost:5000 (or the configured port)

## 3. Frontend Setup (React)
```bash
cd frontend
npm install
npm run dev
```
Frontend will be available at http://localhost:5173

## Future Improvements:
Improve Model accuracy 
Persistent room configurations
User authentication and saved projects
Performance optimization for large 3D scenes

## Acknowledgements
I would like to express my sincere gratitude to **MDG Space – IIT Roorkee** for organizing the month-long mentorship program **Season of Code**.  
This project, *RoomView3D*, was developed as a part of this program.
The guidance, mentorship, and structured learning environment provided throughout Season of Code made this a valuable and enriching experience.  
I am truly thankful for this opportunity to learn, build, and grow as a developer.

## Results
<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/dfdea158-c2c8-4d8d-8e88-6f2c4fc6dd74" />
