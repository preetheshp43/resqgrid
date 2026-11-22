import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface TacticalRadar3DProps {
  severity?: number;
  threatLevel?: 'CRITICAL' | 'HIGH' | 'MODERATE';
}

export const TacticalRadar3D: React.FC<TacticalRadar3DProps> = ({
  severity = 85,
  threatLevel = 'CRITICAL'
}) => {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;

    const width = mount.clientWidth || 280;
    const height = mount.clientHeight || 280;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(0, 3.5, 4.2);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    mount.appendChild(renderer.domElement);

    // Colors based on threat level
    const radarColor = threatLevel === 'CRITICAL' ? 0xff3366 : threatLevel === 'HIGH' ? 0xffb020 : 0x00f0ff;

    // Tactical concentric rings
    const ringRadii = [0.6, 1.2, 1.8, 2.4];
    ringRadii.forEach((r, idx) => {
      const ringGeo = new THREE.RingGeometry(r - 0.015, r + 0.015, 48);
      const ringMat = new THREE.MeshBasicMaterial({
        color: radarColor,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.15 + idx * 0.1,
      });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.rotation.x = Math.PI / 2;
      scene.add(ring);
    });

    // Crosshairs
    const lineMat = new THREE.LineBasicMaterial({ color: radarColor, transparent: true, opacity: 0.25 });
    const lineGeoX = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-2.4, 0, 0),
      new THREE.Vector3(2.4, 0, 0),
    ]);
    const lineGeoZ = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0, -2.4),
      new THREE.Vector3(0, 0, 2.4),
    ]);
    scene.add(new THREE.Line(lineGeoX, lineMat));
    scene.add(new THREE.Line(lineGeoZ, lineMat));

    // Rotating Sweep Wedge
    const sweepGeo = new THREE.CircleGeometry(2.4, 32, 0, Math.PI / 4);
    const sweepMat = new THREE.MeshBasicMaterial({
      color: radarColor,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.35,
    });
    const sweepMesh = new THREE.Mesh(sweepGeo, sweepMat);
    sweepMesh.rotation.x = Math.PI / 2;
    scene.add(sweepMesh);

    // Hazard Nodes on the radar
    const blipGeo = new THREE.SphereGeometry(0.08, 12, 12);
    const blipMat = new THREE.MeshBasicMaterial({ color: 0xff3366 });
    const blip = new THREE.Mesh(blipGeo, blipMat);
    blip.position.set(1.1, 0.05, -0.9);
    scene.add(blip);

    let frameId: number;
    let angle = 0;

    const animate = () => {
      frameId = requestAnimationFrame(animate);
      angle += 0.04;
      sweepMesh.rotation.z = angle;
      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(frameId);
      if (renderer) {
        if (renderer.domElement && renderer.domElement.parentNode === mount) {
          mount.removeChild(renderer.domElement);
        }
        renderer.dispose();
      }
    };
  }, [severity, threatLevel]);

  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <div ref={mountRef} className="w-[280px] h-[280px]" />
      <div className="absolute bottom-2 text-center font-mono text-[11px] text-slate-400">
        SCAN FREQUENCY: 2.4 GHz | SEVERITY: <span className="text-red-400 font-bold">{severity}%</span>
      </div>
    </div>
  );
};

