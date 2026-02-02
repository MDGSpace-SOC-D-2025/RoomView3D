import React, { useState, useMemo, useRef, useEffect } from "react";
import { useGLTF, TransformControls } from "@react-three/drei";
import * as THREE from "three";

const ROOM_LIMITS = {
  x: { min: -9.0, max: 9.0 },
  y: { min: 0.1,    max: 2   },
  z: { min: -9.0, max: 9.0 }
};

export function Furniture({ modelPath, position, orbitRef }) {
  const { scene } = useGLTF(modelPath);
  const groupRef = useRef();
  const controlsRef = useRef();
  const [active, setActive] = useState(false);
  const [mode, setMode] = useState("translate");

  const clonedScene = useMemo(() => {
    const clone = scene.clone(true);
    clone.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
      }
    });
    return clone;
  }, [scene]);

  useEffect(() => {
    const controls = controlsRef.current;
    if (!controls) return;

    const handleChange = () => {
      if (groupRef.current && mode === "translate") {
        const obj = groupRef.current;
        
        // Check and Clamp X
        if (obj.position.x < ROOM_LIMITS.x.min) obj.position.x = ROOM_LIMITS.x.min;
        if (obj.position.x > ROOM_LIMITS.x.max) obj.position.x = ROOM_LIMITS.x.max;

        // Check and Clamp Y (Zamin se niche na jaye)
        if (obj.position.y < ROOM_LIMITS.y.min) obj.position.y = ROOM_LIMITS.y.min;
        if (obj.position.y > ROOM_LIMITS.y.max) obj.position.y = ROOM_LIMITS.y.max;

        // Check and Clamp Z
        if (obj.position.z < ROOM_LIMITS.z.min) obj.position.z = ROOM_LIMITS.z.min;
        if (obj.position.z > ROOM_LIMITS.z.max) obj.position.z = ROOM_LIMITS.z.max;
      }
    };

    controls.addEventListener("change", handleChange);
    return () => controls.removeEventListener("change", handleChange);
  }, [mode, active]);

  useEffect(() => {
    if (!active) return;
    const handler = (e) => {
      if (e.key === "g") setMode("translate");
      if (e.key === "r") setMode("rotate");
      if (e.key === "s") setMode("scale");
      if (e.key === "Escape") setActive(false); // Deselect karne ke liye
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [active]);

  return (
    <>
      {active && (
        <TransformControls
          ref={controlsRef}
          object={groupRef.current} 
          mode={mode}
          onMouseDown={() => (orbitRef.current.enabled = false)}
          onMouseUp={() => (orbitRef.current.enabled = true)}
        />
      )}
      
      <group
        ref={groupRef}
        position={position}
        onClick={(e) => {
          e.stopPropagation();
          setActive(true);
        }}
      >
        <primitive object={clonedScene} />
      </group>
    </>
  );
}