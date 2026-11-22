import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

interface Hero3DSceneProps {
  className?: string;
  onNodeClick?: (sector: string) => void;
}

export const Hero3DScene: React.FC<Hero3DSceneProps> = ({ className = '', onNodeClick }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const mouseRef = useRef({ x: 0, y: 0, targetX: 0, targetY: 0 });
  const [webglSupported, setWebglSupported] = useState<boolean>(true);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let renderer: THREE.WebGLRenderer | null = null;
    let animationFrameId: number;

    try {
      // --- 1. Scene & Camera Setup ---
      const width = container.clientWidth || window.innerWidth || 800;
      const height = container.clientHeight || window.innerHeight || 600;

      const scene = new THREE.Scene();
      scene.fog = new THREE.FogExp2(0x050811, 0.035);

      const camera = new THREE.PerspectiveCamera(45, width / Math.max(1, height), 0.1, 1000);
      camera.position.set(0, 1.2, 7.5);

      // Try creating WebGLRenderer
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.2;

      // Ensure container is empty before appending
      while (container.firstChild) {
        container.removeChild(container.firstChild);
      }
      container.appendChild(renderer.domElement);

      // --- 2. Lighting ---
      const ambientLight = new THREE.AmbientLight(0x00f0ff, 0.7);
      scene.add(ambientLight);

      const dirLight1 = new THREE.DirectionalLight(0x00ffff, 2.5);
      dirLight1.position.set(5, 8, 5);
      scene.add(dirLight1);

      const alertLight = new THREE.PointLight(0xff3366, 3, 20);
      alertLight.position.set(-3, 2, 4);
      scene.add(alertLight);

      // --- 3. Digital Tactical Globe Group ---
      const globeGroup = new THREE.Group();
      scene.add(globeGroup);

      // Wireframe Sphere (Earth Base)
      const sphereRadius = 2.4;
      const sphereGeo = new THREE.SphereGeometry(sphereRadius, 32, 32);
      const sphereMat = new THREE.MeshBasicMaterial({
        color: 0x004466,
        wireframe: true,
        transparent: true,
        opacity: 0.22,
      });
      const sphereMesh = new THREE.Mesh(sphereGeo, sphereMat);
      globeGroup.add(sphereMesh);

      // Inner Dark Core
      const coreGeo = new THREE.SphereGeometry(sphereRadius * 0.98, 28, 28);
      const coreMat = new THREE.MeshBasicMaterial({
        color: 0x061126,
        transparent: true,
        opacity: 0.85,
      });
      const coreMesh = new THREE.Mesh(coreGeo, coreMat);
      globeGroup.add(coreMesh);

      // Orbital Rings
      const ringGeo = new THREE.RingGeometry(3.1, 3.14, 48);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0x00f0ff,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.45,
      });
      const orbitalRing1 = new THREE.Mesh(ringGeo, ringMat);
      orbitalRing1.rotation.x = Math.PI / 2.3;
      orbitalRing1.rotation.y = 0.3;
      globeGroup.add(orbitalRing1);

      const ringGeo2 = new THREE.RingGeometry(3.4, 3.42, 48);
      const ringMat2 = new THREE.MeshBasicMaterial({
        color: 0xff3366,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.3,
      });
      const orbitalRing2 = new THREE.Mesh(ringGeo2, ringMat2);
      orbitalRing2.rotation.x = Math.PI / 1.7;
      orbitalRing2.rotation.y = -0.4;
      globeGroup.add(orbitalRing2);

      // --- 4. Pulsing Disaster Beacons on Surface ---
      const beaconCoords = [
        { lat: 12.8, lon: 74.8, color: 0xff3366, size: 0.1 },
        { lat: 25.0, lon: 45.0, color: 0xffb020, size: 0.08 },
        { lat: -15.0, lon: 120.0, color: 0x00f0ff, size: 0.08 },
        { lat: 35.0, lon: -95.0, color: 0xff3366, size: 0.09 },
        { lat: 51.5, lon: 0.1, color: 0x00e676, size: 0.07 },
      ];

      const beaconPings: THREE.Mesh[] = [];

      beaconCoords.forEach((coord) => {
        const phi = (90 - coord.lat) * (Math.PI / 180);
        const theta = (coord.lon + 180) * (Math.PI / 180);

        const x = -(sphereRadius * Math.sin(phi) * Math.cos(theta));
        const z = sphereRadius * Math.sin(phi) * Math.sin(theta);
        const y = sphereRadius * Math.cos(phi);

        // Core point
        const pGeo = new THREE.SphereGeometry(coord.size, 12, 12);
        const pMat = new THREE.MeshBasicMaterial({ color: coord.color });
        const pMesh = new THREE.Mesh(pGeo, pMat);
        pMesh.position.set(x, y, z);
        globeGroup.add(pMesh);

        // Alert Ping Wave Ring
        const pingGeo = new THREE.RingGeometry(coord.size * 1.2, coord.size * 1.5, 20);
        const pingMat = new THREE.MeshBasicMaterial({
          color: coord.color,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.9,
        });
        const pingMesh = new THREE.Mesh(pingGeo, pingMat);
        pingMesh.position.set(x * 1.02, y * 1.02, z * 1.02);
        pingMesh.lookAt(x * 2, y * 2, z * 2);
        globeGroup.add(pingMesh);
        beaconPings.push(pingMesh);
      });

      // --- 5. Reconnaissance UAV / Drone Mesh in 3D ---
      const droneGroup = new THREE.Group();
      const chassisGeo = new THREE.BoxGeometry(0.24, 0.06, 0.36);
      const chassisMat = new THREE.MeshStandardMaterial({
        color: 0x112233,
        metalness: 0.8,
        roughness: 0.2,
        emissive: 0x00f0ff,
        emissiveIntensity: 0.3,
      });
      const chassis = new THREE.Mesh(chassisGeo, chassisMat);
      droneGroup.add(chassis);

      // Sensor Radar Cone
      const coneGeo = new THREE.ConeGeometry(0.8, 1.8, 16, 1, true);
      const coneMat = new THREE.MeshBasicMaterial({
        color: 0x00f0ff,
        wireframe: true,
        transparent: true,
        opacity: 0.2,
      });
      const scanCone = new THREE.Mesh(coneGeo, coneMat);
      scanCone.rotation.x = Math.PI;
      scanCone.position.y = -0.9;
      droneGroup.add(scanCone);

      droneGroup.position.set(2.6, 1.5, 1.8);
      droneGroup.scale.set(0.9, 0.9, 0.9);
      scene.add(droneGroup);

      // --- 6. Telemetry Particle Cloud ---
      const particlesCount = 500;
      const posArray = new Float32Array(particlesCount * 3);
      for (let i = 0; i < particlesCount * 3; i += 3) {
        posArray[i] = (Math.random() - 0.5) * 16;
        posArray[i + 1] = (Math.random() - 0.5) * 16;
        posArray[i + 2] = (Math.random() - 0.5) * 16;
      }
      const particlesGeo = new THREE.BufferGeometry();
      particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
      const particlesMat = new THREE.PointsMaterial({
        size: 0.035,
        color: 0x00e5ff,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending,
      });
      const particleSystem = new THREE.Points(particlesGeo, particlesMat);
      scene.add(particleSystem);

      // --- 7. Mouse Event Listeners for Parallax ---
      const handleMouseMove = (e: MouseEvent) => {
        const rect = container.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) return;
        const clientX = e.clientX - rect.left;
        const clientY = e.clientY - rect.top;
        mouseRef.current.targetX = (clientX / rect.width) * 2 - 1;
        mouseRef.current.targetY = -(clientY / rect.height) * 2 + 1;
      };

      window.addEventListener('mousemove', handleMouseMove);

      // --- 8. Animation Loop ---
      let clock = new THREE.Clock();

      const animate = () => {
        animationFrameId = requestAnimationFrame(animate);
        const elapsedTime = clock.getElapsedTime();

        mouseRef.current.x += (mouseRef.current.targetX - mouseRef.current.x) * 0.04;
        mouseRef.current.y += (mouseRef.current.targetY - mouseRef.current.y) * 0.04;

        globeGroup.rotation.y = elapsedTime * 0.12 + mouseRef.current.x * 0.5;
        globeGroup.rotation.x = 0.15 + mouseRef.current.y * 0.3;
        orbitalRing1.rotation.z = elapsedTime * 0.18;
        orbitalRing2.rotation.z = -elapsedTime * 0.22;

        beaconPings.forEach((ping, idx) => {
          const s = 1 + (Math.sin(elapsedTime * 4 + idx) + 1) * 0.65;
          ping.scale.set(s, s, s);
          (ping.material as THREE.MeshBasicMaterial).opacity = Math.max(0, 1 - (s - 1));
        });

        const droneAngle = elapsedTime * 0.6;
        droneGroup.position.x = Math.cos(droneAngle) * 3.4;
        droneGroup.position.z = Math.sin(droneAngle) * 3.4;
        droneGroup.position.y = 1.0 + Math.sin(elapsedTime * 1.5) * 0.35;
        droneGroup.lookAt(0, 0, 0);
        scanCone.rotation.y = elapsedTime * 3.5;

        particleSystem.rotation.y = -elapsedTime * 0.02;

        if (renderer) {
          renderer.render(scene, camera);
        }
      };

      animate();

      const handleResize = () => {
        if (!container || !renderer) return;
        const newW = container.clientWidth || window.innerWidth || 800;
        const newH = container.clientHeight || window.innerHeight || 600;
        camera.aspect = newW / Math.max(1, newH);
        camera.updateProjectionMatrix();
        renderer.setSize(newW, newH);
      };

      window.addEventListener('resize', handleResize);

      return () => {
        window.removeEventListener('mousemove', handleMouseMove);
        window.removeEventListener('resize', handleResize);
        cancelAnimationFrame(animationFrameId);
        if (renderer) {
          if (renderer.domElement && renderer.domElement.parentNode === container) {
            container.removeChild(renderer.domElement);
          }
          renderer.dispose();
        }
      };
    } catch (err) {
      console.warn('WebGL initialization failed, using high-tech CSS HUD fallback:', err);
      setWebglSupported(false);
      return () => {
        cancelAnimationFrame(animationFrameId);
        if (renderer && renderer.domElement && renderer.domElement.parentNode === container) {
          container.removeChild(renderer.domElement);
        }
      };
    }
  }, [onNodeClick]);

  return (
    <div 
      className={`relative w-full h-full min-h-[500px] overflow-hidden select-none pointer-events-none ${className}`}
    >
      {/* 3D Canvas Mounting Point */}
      <div ref={containerRef} className="absolute inset-0 w-full h-full pointer-events-none" />

      {/* Fallback Holographic Grid if WebGL is disabled */}
      {!webglSupported && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="relative w-80 h-80 rounded-full border border-cyan-500/30 animate-spin-slow flex items-center justify-center">
            <div className="w-64 h-64 rounded-full border border-dashed border-cyan-400/40 animate-radar-sweep" />
            <div className="absolute w-48 h-48 rounded-full border border-red-500/30" />
            <div className="absolute w-4 h-4 bg-red-500 rounded-full animate-ping" />
          </div>
        </div>
      )}

      {/* Tactical HUD Overlay Elements inside 3D Scene */}
      <div className="absolute top-6 left-6 pointer-events-none flex flex-col gap-1 font-mono text-xs text-cyan-400/80 bg-slate-950/60 p-3 rounded-lg border border-cyan-500/20 backdrop-blur-md">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
          <span className="font-bold tracking-widest text-cyan-300">GRID TELEMETRY: ACTIVE</span>
        </div>
        <div className="text-[10px] text-slate-400">GEO-COORD: 12.8715° N, 74.8450° E</div>
        <div className="text-[10px] text-slate-400">GLOBAL SATELLITE MESH: 32 NODES SYNCED</div>
        <div className="text-[10px] text-emerald-400">ORBITAL CONFIDENCE: 99.4%</div>
      </div>

      <div className="absolute bottom-6 right-6 pointer-events-none flex flex-col items-end gap-1 font-mono text-xs text-slate-400 bg-slate-950/60 p-3 rounded-lg border border-slate-700/30 backdrop-blur-md">
        <span className="text-[10px] tracking-wider text-slate-300">INTERACTIVE 3D PROJECTION</span>
        <span className="text-[9px] text-cyan-400">MOVE CURSOR TO ROTATE TACTICAL GLOBE</span>
      </div>
    </div>
  );
};
