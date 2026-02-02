import React, { useState, useEffect, Suspense, useRef } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Grid, Sky, ContactShadows } from "@react-three/drei";
import { useLocation } from "react-router-dom";
import FurnitureDropdown from "./FurnitureDropdown";
import { Furniture } from "./Furniture";
import * as THREE from "three";

const Room = () => (
  <group>
    <mesh rotation-x={-Math.PI / 2} position={[0, -0.0, 0]}>
      <planeGeometry args={[20, 20]} />
      <meshStandardMaterial color="#be9a9a" side={THREE.DoubleSide} />
    </mesh>

    <mesh position={[0, 4, -10]}>
      <planeGeometry args={[20, 8]} />
      <meshStandardMaterial color="#e0e0e0" side={THREE.DoubleSide} />
    </mesh>

    <mesh position={[-10, 4, 0]} rotation-y={Math.PI / 2}>
      <planeGeometry args={[20, 8]} />
      <meshStandardMaterial color="#e0e0e0" side={THREE.DoubleSide}/>
    </mesh>
  </group>
);

export default function Editor() {
  const { state } = useLocation();
  const scene = state ? state.scene : undefined;
  const projectName = state ? state.projectName : undefined;
  
  const [items, setItems] = useState([]);
  const orbitRef = useRef();

  useEffect(() => {
    if (!scene?.furniture) return;

    const mapped = scene.furniture.map((f) => ({
      id: f.id,
      modelPath: `/models/${f.type}.glb`,
      position: [f.position.x, f.position.y, f.position.z],
    }));

    setItems(mapped);
  }, [scene]);

  const handleFurnitureSelect = (item) => {
    setItems((prev) => [
      ...prev,
      {
        id: Date.now(),
        modelPath: `/models/${item.type}.glb`,
        position: [0, 0, 0],
      },
    ]);
  };

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <div style={{ position: "absolute", zIndex: 10, padding: 10 }}>
        <strong>{projectName}</strong>
      </div>  

      <FurnitureDropdown onSelect={handleFurnitureSelect} />

      <Canvas camera={{ position: [12, 12, 12], fov: 55 }}>
        <ambientLight intensity={1.5} />

        <Suspense fallback={null}>
          <Room />
          {items.map((item) => (
            <Furniture key={item.id} {...item} orbitRef={orbitRef} />
          ))}
        </Suspense>

        <Grid infiniteGrid position={[0, 0.01, 0]}/>
        <ContactShadows opacity={0.4} />
        <OrbitControls ref={orbitRef} minPolarAngle={Math.PI / 4} maxPolarAngle={Math.PI / 2.2}   minDistance={5} maxDistance={25}/>
      </Canvas>
    </div>
  );
}
