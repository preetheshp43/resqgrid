import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import streamlit.components.v1 as components
from PIL import Image, ImageDraw
import datetime
import time
import math
import random

# ==============================================================================
# 1. PAGE SETUP & CYBER-WAR-ROOM THEME
# ==============================================================================
st.set_page_config(
    page_title="RESQGRID // TACTICAL CRISIS WAR ROOM",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cyberpunk / Palantir Command HUD Styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=JetBrains+Mono:wght@400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0c162d 0%, #060a14 70%, #02040a 100%);
        color: #e2e8f0;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Top HUD Header */
    .hud-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 24px;
        background: rgba(10, 20, 42, 0.7);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 14px;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.15), inset 0 0 15px rgba(0, 240, 255, 0.05);
        backdrop-filter: blur(20px);
        margin-bottom: 20px;
    }
    
    .hud-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 20px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #fff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.8);
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background: rgba(12, 22, 45, 0.8);
        border: 1px solid rgba(0, 240, 255, 0.25);
        padding: 14px 20px;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 0 10px rgba(0, 240, 255, 0.05);
    }
    div[data-testid="stMetricValue"] {
        color: #00f0ff !important;
        font-weight: 800;
        font-size: 32px !important;
        font-family: 'Orbitron', monospace;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: bold;
    }

    /* Custom Tactical Cards */
    .crisis-card {
        background: linear-gradient(135deg, rgba(16, 28, 58, 0.7) 0%, rgba(8, 14, 28, 0.9) 100%);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.2s ease;
    }
    .crisis-card:hover {
        border-color: rgba(0, 240, 255, 0.6);
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.25);
        transform: translateY(-2px);
    }
    
    .status-pill-p1 {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: bold;
        letter-spacing: 1px;
        animation: pulse 1.5s infinite;
    }
    
    .status-pill-dispatched {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid #10b981;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00f0ff 0%, #0077ff 100%);
        color: #030712;
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 12px;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.8);
        transform: scale(1.02);
        color: #000;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. AUDIO SYNTHESIZER & TACTICAL SFX
# ==============================================================================
def trigger_sfx(sound_name):
    """Generates realistic synthetic tactical radio / siren sound effects in the browser."""
    sound_js = {
        "siren": """
            var osc1 = ctx.createOscillator();
            var osc2 = ctx.createOscillator();
            var gain = ctx.createGain();
            osc1.type = 'sawtooth'; osc2.type = 'square';
            osc1.frequency.setValueAtTime(550, now);
            osc1.frequency.exponentialRampToValueAtTime(880, now + 0.25);
            osc1.frequency.exponentialRampToValueAtTime(550, now + 0.5);
            osc2.frequency.setValueAtTime(554, now);
            osc2.frequency.exponentialRampToValueAtTime(884, now + 0.25);
            osc2.frequency.exponentialRampToValueAtTime(554, now + 0.5);
            gain.gain.setValueAtTime(0.12, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.55);
            osc1.connect(gain); osc2.connect(gain); gain.connect(ctx.destination);
            osc1.start(now); osc2.start(now); osc1.stop(now + 0.55); osc2.stop(now + 0.55);
        """,
        "dispatch": """
            [440, 554.37, 659.25, 880].forEach((f, i) => {
                var osc = ctx.createOscillator();
                var g = ctx.createGain();
                var t = now + i * 0.08;
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(f, t);
                g.gain.setValueAtTime(0.1, t);
                g.gain.exponentialRampToValueAtTime(0.001, t + 0.25);
                osc.connect(g); g.connect(ctx.destination);
                osc.start(t); osc.stop(t + 0.25);
            });
        """,
        "ping": """
            var osc = ctx.createOscillator();
            var g = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(1400, now);
            osc.frequency.exponentialRampToValueAtTime(2200, now + 0.1);
            g.gain.setValueAtTime(0.08, now);
            g.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
            osc.connect(g); g.connect(ctx.destination);
            osc.start(now); osc.stop(now + 0.12);
        """
    }
    action_code = sound_js.get(sound_name, sound_js["ping"])
    components.html(f"""
    <script>
    try {{
        var AudioContext = window.AudioContext || window.webkitAudioContext;
        var ctx = new AudioContext();
        var now = ctx.currentTime;
        {action_code}
    }} catch(e) {{}}
    </script>
    """, height=0, width=0)


# ==============================================================================
# 3. INTERACTIVE 3D HOLOGRAPHIC RADAR CANVAS (THREE.JS)
# ==============================================================================
def render_cinematic_3d_radar():
    """Renders a fully interactive holographic 3D globe with real-time orbiting UAVs and shockwave pings."""
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            body, html { margin:0; padding:0; overflow:hidden; background:#060a14; width:100%; height:100%; font-family:monospace; }
            #radar-view { width:100%; height:280px; position:relative; }
            .badge-hud { position:absolute; top:12px; left:16px; color:#00f0ff; font-size:11px; font-weight:bold; background:rgba(6,10,20,0.8); padding:5px 12px; border:1px solid rgba(0,240,255,0.4); border-radius:6px; box-shadow:0 0 10px rgba(0,240,255,0.3); pointer-events:none; }
            .grid-coords { position:absolute; bottom:12px; right:16px; color:#64748b; font-size:10px; background:rgba(6,10,20,0.8); padding:4px 10px; border-radius:4px; pointer-events:none; }
        </style>
    </head>
    <body>
        <div id="radar-view">
            <div class="badge-hud">
                <span style="color:#ef4444; animation: blink 1s infinite;">●</span> SATELLITE MESH: 32 NODES SYNCED // LIVE TELEMETRY
            </div>
            <div class="grid-coords">DRAG TO ORBIT TACTICAL PROJECTION // SCROLL TO ZOOM</div>
        </div>
        <script>
            const container = document.getElementById('radar-view');
            const w = container.clientWidth || window.innerWidth;
            const h = 280;

            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x060a14, 0.035);
            const camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 1000);
            camera.position.set(0, 1.2, 6.5);

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(w, h);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(renderer.domElement);

            scene.add(new THREE.AmbientLight(0x00f0ff, 0.8));
            const sun = new THREE.DirectionalLight(0xffffff, 2.0);
            sun.position.set(5, 8, 5);
            scene.add(sun);

            const globe = new THREE.Group();
            scene.add(globe);

            // Wireframe Cyber Globe
            const earthMesh = new THREE.Mesh(
                new THREE.SphereGeometry(2.2, 32, 32),
                new THREE.MeshBasicMaterial({ color: 0x007799, wireframe: true, transparent: true, opacity: 0.3 })
            );
            globe.add(earthMesh);

            // Dark inner core with glowing aura
            globe.add(new THREE.Mesh(
                new THREE.SphereGeometry(2.15, 26, 26),
                new THREE.MeshBasicMaterial({ color: 0x091428, transparent: true, opacity: 0.85 })
            ));

            // Concentric Radar Scan Rings
            const ring1 = new THREE.Mesh(
                new THREE.RingGeometry(2.6, 2.63, 64),
                new THREE.MeshBasicMaterial({ color: 0x00f0ff, side: THREE.DoubleSide, transparent: true, opacity: 0.45 })
            );
            ring1.rotation.x = Math.PI / 2.3;
            globe.add(ring1);

            const ring2 = new THREE.Mesh(
                new THREE.RingGeometry(2.9, 2.93, 64),
                new THREE.MeshBasicMaterial({ color: 0xef4444, side: THREE.DoubleSide, transparent: true, opacity: 0.35 })
            );
            ring2.rotation.x = Math.PI / 1.7;
            ring2.rotation.y = -0.3;
            globe.add(ring2);

            // Disaster Beacons with Expanding Waves
            const coords = [
                { lat: 12.8, lon: 74.8, c: 0xef4444 }, // Flash flood
                { lat: 25.0, lon: 45.0, c: 0xf59e0b },
                { lat: -15.0, lon: 120.0, c: 0x00f0ff },
                { lat: 35.0, lon: -95.0, c: 0xef4444 }
            ];
            const pings = [];
            coords.forEach(b => {
                const phi = (90 - b.lat) * (Math.PI / 180);
                const theta = (b.lon + 180) * (Math.PI / 180);
                const x = -(2.2 * Math.sin(phi) * Math.cos(theta));
                const z = 2.2 * Math.sin(phi) * Math.sin(theta);
                const y = 2.2 * Math.cos(phi);

                const pin = new THREE.Mesh(new THREE.SphereGeometry(0.08, 12, 12), new THREE.MeshBasicMaterial({ color: b.c }));
                pin.position.set(x, y, z);
                globe.add(pin);

                const ring = new THREE.Mesh(new THREE.RingGeometry(0.1, 0.16, 20), new THREE.MeshBasicMaterial({ color: b.c, side: THREE.DoubleSide, transparent: true, opacity: 0.9 }));
                ring.position.set(x * 1.01, y * 1.01, z * 1.01);
                ring.lookAt(x * 2, y * 2, z * 2);
                globe.add(ring);
                pings.push(ring);
            });

            // Reconnaissance Drone with Sensor Cone
            const drone = new THREE.Group();
            drone.add(new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.05, 0.35), new THREE.MeshBasicMaterial({ color: 0x00f0ff })));
            const cone = new THREE.Mesh(new THREE.ConeGeometry(0.6, 1.4, 16, 1, true), new THREE.MeshBasicMaterial({ color: 0x00f0ff, wireframe: true, transparent: true, opacity: 0.25 }));
            cone.rotation.x = Math.PI;
            cone.position.y = -0.7;
            drone.add(cone);
            scene.add(drone);

            let mouseX = 0, mouseY = 0;
            window.addEventListener('mousemove', e => {
                mouseX = (e.clientX / window.innerWidth) * 2 - 1;
                mouseY = -(e.clientY / 280) * 2 + 1;
            });

            const clock = new THREE.Clock();
            function animate() {
                requestAnimationFrame(animate);
                const t = clock.getElapsedTime();
                globe.rotation.y = t * 0.12 + mouseX * 0.4;
                globe.rotation.x = 0.15 + mouseY * 0.2;
                ring1.rotation.z = t * 0.2;
                ring2.rotation.z = -t * 0.25;

                pings.forEach((p, idx) => {
                    const s = 1 + (Math.sin(t * 4 + idx) + 1) * 0.6;
                    p.scale.set(s, s, s);
                    p.material.opacity = Math.max(0, 1 - (s - 1));
                });

                drone.position.x = Math.cos(t * 0.5) * 3.2;
                drone.position.z = Math.sin(t * 0.5) * 3.2;
                drone.position.y = 0.8 + Math.sin(t * 1.4) * 0.3;
                drone.lookAt(0, 0, 0);

                renderer.render(scene, camera);
            }
            animate();
        </script>
    </body>
    </html>
    """, height=290, scrolling=False)


# ==============================================================================
# 4. CRISIS DATA ENGINE
# ==============================================================================
if "incidents" not in st.session_state:
    st.session_state.incidents = [
        {
            "id": "CRISIS-DELTA-1",
            "title": "Catastrophic Flash Flood: Submerged Urban Settlement",
            "type": "Flash Flood",
            "lat": 12.8465,
            "lng": 74.8624,
            "sector": "Jeppinamogaru River Corridor",
            "priority": "CRITICAL P1",
            "status": "IMMEDIATE DISPATCH REQUIRED",
            "trapped": 16,
            "threat_water_rise": "+0.45 m/hr",
            "time_to_crest": "28 Mins",
            "damage_pct": 94,
            "ai_action": "Deploy NDRF Inflatable Gemini Alpha + Drone Recon Eagle-X (drop acoustic vests).",
            "units_needed": ["NDRF Gemini Boat Alpha", "Eagle-X Recon Drone"]
        },
        {
            "id": "CRISIS-ALPHA-2",
            "title": "Industrial Toxic Hydrocarbon Explosion & Fire Plume",
            "type": "Chemical Fire",
            "lat": 12.9512,
            "lng": 74.8021,
            "sector": "Baikampady Petrochemical Block",
            "priority": "CRITICAL P1",
            "status": "IMMEDIATE DISPATCH REQUIRED",
            "trapped": 6,
            "threat_water_rise": "Plume 36 km/h NNE",
            "time_to_crest": "18 Mins",
            "damage_pct": 89,
            "ai_action": "Deploy Heavy Foam Tender FT-07 (AFFF) + Hazmat Decontamination Van.",
            "units_needed": ["Heavy Foam Tender FT-07", "Hazmat Trauma Unit"]
        },
        {
            "id": "CRISIS-ECHO-3",
            "title": "Ghat Slope Failure & Highway Bus Trapped",
            "type": "Landslide",
            "lat": 12.9056,
            "lng": 74.9124,
            "sector": "Gurupura Mountain Pass",
            "priority": "ELEVATED P2",
            "status": "UNITS EN ROUTE",
            "trapped": 4,
            "threat_water_rise": "Secondary Slump 72%",
            "time_to_crest": "45 Mins",
            "damage_pct": 74,
            "ai_action": "Heavy hydraulic cutters + SDRF Mountain Rescue Squad.",
            "units_needed": ["SDRF Rescue Squad 3"]
        }
    ]

if "fleet" not in st.session_state:
    st.session_state.fleet = [
        {"id": "RESCUE-01", "name": "NDRF Gemini Boat Alpha", "type": "Inflatable Watercraft", "status": "AVAILABLE", "crew": 6, "capacity": 12, "battery": 96},
        {"id": "RESCUE-02", "name": "Eagle-X Recon Drone", "type": "FLIR Thermal UAV", "status": "AVAILABLE", "crew": 2, "capacity": 2, "battery": 89},
        {"id": "RESCUE-03", "name": "Heavy Foam Tender FT-07", "type": "Fire Suppression", "status": "AVAILABLE", "crew": 6, "capacity": 4, "battery": 92},
        {"id": "RESCUE-04", "name": "Hazmat Trauma Unit", "type": "Advanced Life Support", "status": "AVAILABLE", "crew": 4, "capacity": 3, "battery": 85},
        {"id": "RESCUE-05", "name": "SDRF Rescue Squad 3", "type": "Heavy Shoring", "status": "EN ROUTE", "crew": 8, "capacity": 8, "battery": 78}
    ]

if "survivors_extracted" not in st.session_state:
    st.session_state.survivors_extracted = 38


# ==============================================================================
# 5. HEADER HUD
# ==============================================================================
st.markdown("""
<div class="hud-header">
    <div style="display:flex; align-items:center; gap:16px;">
        <span style="font-size:28px; filter: drop-shadow(0 0 10px #00f0ff);">🚨</span>
        <div>
            <div class="hud-title">RESQGRID <span style="color:#00f0ff;">WAR ROOM</span></div>
            <div style="font-size:11px; color:#64748b;">AUTONOMOUS INCIDENT DISPATCH & COMBINATORIAL RESOURCE RESCUE MESH</div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
        <span class="status-pill-p1">DEFCON 1: MAXIMUM ALERT</span>
        <span style="color:#00f0ff; font-weight:bold; font-size:12px;">SYSTEM INTEGRITY: 100%</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 3D Interactive WebGL Scene
render_cinematic_3d_radar()

# Live Mission Counters
open_incidents = [i for i in st.session_state.incidents if i["status"] != "RESOLVED"]
trapped_lives = sum(i["trapped"] for i in open_incidents)
units_deployed = len([f for f in st.session_state.fleet if f["status"] in ["EN ROUTE", "ON SCENE"]])

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Critical Sectors", f"{len(open_incidents)} Active")
m2.metric("Lives in Direct Peril", f"{trapped_lives} Trapped", delta="Critical", delta_color="inverse")
m3.metric("Fleet Deployed", f"{units_deployed} / {len(st.session_state.fleet)} Units", delta="Active")
m4.metric("Survivors Rescued", f"{st.session_state.survivors_extracted} Saved", delta="+4 this turn")
m5.metric("Decision Latency", "0.85s", delta="Real-time")

st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# 6. ACTION-PACKED TABS
# ==============================================================================
tab_ops, tab_drone, tab_sim, tab_fleet = st.tabs([
    "⚡ Live Crisis Response & Triage",
    "🛸 FLIR Thermal Drone Recon Cockpit",
    "🌊 Environmental Surge Simulator",
    "🚒 Fleet Readiness & Dispatch Matrix"
])


# ==============================================================================
# TAB 1: LIVE CRISIS RESPONSE & TRIAGE
# ==============================================================================
with tab_ops:
    col_map, col_actions = st.columns([7, 5])

    with col_map:
        st.markdown("##### 🗺️ 3D Battleground Elevation Map")
        
        # PyDeck 3D Layer
        pts = []
        for inc in open_incidents:
            pts.append({
                "title": inc["title"],
                "lat": inc["lat"],
                "lng": inc["lng"],
                "elevation": inc["damage_pct"] * 35,
                "color": [239, 68, 68, 220] if "CRITICAL" in inc["priority"] else [245, 158, 11, 220],
                "radius": inc["trapped"] * 60 + 180
            })

        view = pdk.ViewState(latitude=12.8950, longitude=74.8500, zoom=11.3, pitch=45, bearing=-10)

        cols_3d = pdk.Layer(
            "ColumnLayer",
            data=pd.DataFrame(pts),
            get_position=["lng", "lat"],
            get_elevation="elevation",
            elevation_scale=1,
            radius=220,
            get_fill_color="color",
            pickable=True,
            auto_highlight=True
        )

        rings = pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame(pts),
            get_position=["lng", "lat"],
            get_color="color",
            get_radius="radius",
            opacity=0.6,
            pickable=True,
            filled=True
        )

        st.pydeck_chart(pdk.Deck(
            layers=[cols_3d, rings],
            initial_view_state=view,
            map_style="mapbox://styles/mapbox/dark-v11",
            tooltip={"text": "🚨 {title}\nDamage: {elevation}"}
        ), use_container_width=True)

        # Quick Disaster Trigger Buttons to play with
        st.markdown("###### 💥 SIMULATE SUDDEN CRISIS TRIGGER:")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            if st.button("🌊 TRIGGER FLASH FLOOD", use_container_width=True):
                new_id = f"CRISIS-DELTA-{len(st.session_state.incidents) + 1}"
                st.session_state.incidents.insert(0, {
                    "id": new_id,
                    "title": "Severe Coastal Inundation: Sea Dike Breach",
                    "type": "Flash Flood",
                    "lat": 12.8120,
                    "lng": 74.8450,
                    "sector": "Someshwar Coastal Colony",
                    "priority": "CRITICAL P1",
                    "status": "IMMEDIATE DISPATCH REQUIRED",
                    "trapped": 12,
                    "threat_water_rise": "+0.60 m/hr",
                    "time_to_crest": "15 Mins",
                    "damage_pct": 96,
                    "ai_action": "Deploy NDRF Gemini Boat Alpha + Airborne Supply Drops.",
                    "units_needed": ["NDRF Gemini Boat Alpha"]
                })
                trigger_sfx("siren")
                st.rerun()

        with sc2:
            if st.button("🔥 TRIGGER WILDFIRE FLARE", use_container_width=True):
                st.session_state.incidents.insert(0, {
                    "id": f"CRISIS-FIRE-{len(st.session_state.incidents) + 1}",
                    "title": "LPG Bottling Plant Thermal Flare",
                    "type": "Fire",
                    "lat": 12.9300,
                    "lng": 74.8200,
                    "sector": "Baikampady Sector 3",
                    "priority": "CRITICAL P1",
                    "status": "IMMEDIATE DISPATCH REQUIRED",
                    "trapped": 8,
                    "threat_water_rise": "Blast Perimeter 250m",
                    "time_to_crest": "12 Mins",
                    "damage_pct": 91,
                    "ai_action": "Foam Cannon perimeter containment + Hazmat Squad.",
                    "units_needed": ["Heavy Foam Tender FT-07"]
                })
                trigger_sfx("siren")
                st.rerun()

        with sc3:
            if st.button("⚡ AUTO-OPTIMIZE ENTIRE FLEET", use_container_width=True):
                for inc in st.session_state.incidents:
                    if inc["status"] != "RESOLVED":
                        inc["status"] = "UNITS EN ROUTE"
                for f in st.session_state.fleet:
                    f["status"] = "EN ROUTE"
                trigger_sfx("dispatch")
                st.rerun()

    with col_actions:
        st.markdown("##### 🚨 Active Crisis Queue & One-Click Execution")

        for inc in open_incidents:
            is_dispatched = "EN ROUTE" in inc["status"]
            st.markdown(f"""
            <div class="crisis-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#00f0ff; font-weight:bold; font-size:12px;">{inc['id']}</span>
                    <span class="{'status-pill-dispatched' if is_dispatched else 'status-pill-p1'}">
                        {inc['status']}
                    </span>
                </div>
                <div style="font-size:14px; font-weight:800; color:#fff; margin-bottom:4px;">{inc['title']}</div>
                <div style="font-size:11px; color:#94a3b8; margin-bottom:6px;">
                    📍 {inc['sector']} • Trapped: <strong style="color:#ef4444;">{inc['trapped']} lives</strong> • Window: <strong style="color:#f59e0b;">{inc['time_to_crest']}</strong>
                </div>
                <div style="background:rgba(6,10,20,0.7); border:1px solid rgba(0,240,255,0.2); padding:8px 12px; border-radius:6px; font-size:11px; margin-bottom:10px;">
                    <strong style="color:#00f0ff;">AI RECOMMENDED MOVE:</strong><br>
                    {inc['ai_action']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2 = st.columns([1, 1])
            with b1:
                if not is_dispatched:
                    if st.button(f"⚡ AUTHORIZE DISPATCH", key=f"disp_{inc['id']}", use_container_width=True):
                        inc["status"] = "UNITS EN ROUTE"
                        for u in inc["units_needed"]:
                            match = next((f for f in st.session_state.fleet if f["name"] == u), None)
                            if match:
                                match["status"] = "EN ROUTE"
                        trigger_sfx("dispatch")
                        st.rerun()
            with b2:
                if st.button(f"✅ CONFIRM RESCUE", key=f"res_{inc['id']}", use_container_width=True):
                    inc["status"] = "RESOLVED"
                    st.session_state.survivors_extracted += inc["trapped"]
                    for f in st.session_state.fleet:
                        f["status"] = "AVAILABLE"
                    trigger_sfx("dispatch")
                    st.rerun()


# ==============================================================================
# TAB 2: FLIR THERMAL DRONE RECON COCKPIT
# ==============================================================================
with tab_drone:
    st.markdown("##### 🛸 FLIR Thermal Reconnaissance Drone Video Cockpit")
    st.caption("Live simulated UAV Recon stream scanning sector coordinates for human thermal signatures and structural cracks.")

    col_flir, col_telemetry = st.columns([7, 5])

    with col_flir:
        sensor_mode = st.radio("Thermal Sensor Mode:", ["FLIR Ironbow (False Color)", "Night Vision (Phosphor Green)", "Optical 4K (Standard)"], horizontal=True)

        # Generate FLIR Drone Camera Simulation
        if "Ironbow" in sensor_mode:
            bg_color = (25, 10, 60)
            target_color = (255, 120, 0)
            ambient_color = (80, 20, 110)
        elif "Phosphor" in sensor_mode:
            bg_color = (5, 30, 10)
            target_color = (120, 255, 100)
            ambient_color = (20, 80, 30)
        else:
            bg_color = (20, 30, 50)
            target_color = (220, 60, 60)
            ambient_color = (40, 60, 90)

        flir_img = Image.new("RGB", (640, 340), color=bg_color)
        d = ImageDraw.Draw(flir_img)

        # Floodwater or terrain
        d.rectangle([0, 160, 640, 340], fill=ambient_color)

        # Submerged Structures
        d.rectangle([120, 100, 220, 200], fill=(50, 40, 80))
        d.polygon([(110, 100), (170, 50), (230, 100)], fill=(90, 50, 90))

        d.rectangle([340, 120, 460, 220], fill=(60, 50, 90))
        d.polygon([(330, 120), (400, 70), (470, 120)], fill=(110, 60, 100))

        # Human Thermal Signatures (Heat blooms)
        d.ellipse([145, 65, 165, 85], fill=target_color)
        d.ellipse([170, 70, 190, 90], fill=target_color)
        d.ellipse([185, 75, 205, 95], fill=target_color)

        # Crosshair HUD
        cx, cy = 320, 170
        d.line([cx - 40, cy, cx + 40, cy], fill=(0, 240, 255), width=2)
        d.line([cx, cy - 40, cx, cy + 40], fill=(0, 240, 255), width=2)
        d.rectangle([cx - 20, cy - 20, cx + 20, cy + 20], outline=(0, 240, 255), width=1)

        # Thermal Lock-on Bounding Box
        d.rectangle([135, 55, 215, 105], outline=(0, 255, 150), width=3)

        st.image(flir_img, caption="UAV Recon Eagle-X // Direct Drone Gimbal Telemetry", use_container_width=True)

    with col_telemetry:
        st.markdown("###### 📊 Real-Time Drone Avionics Telemetry")
        st.markdown("""
        <div style="background:rgba(8,16,36,0.8); border:1px solid rgba(0,240,255,0.3); border-radius:10px; padding:16px; font-size:12px; line-height:1.8;">
            • UAV Unit: <strong style="color:#00f0ff;">Eagle-X Hexacopter Recon</strong><br>
            • Altitude: <strong>124m AGL (Above Ground Level)</strong><br>
            • Airspeed: <strong>48.2 km/h (Wind Resistance: Grade 8)</strong><br>
            • Battery Pack: <strong style="color:#10b981;">88% (Remaining Flight: 34 Mins)</strong><br>
            • Thermal Sensor: <strong>FLIR Boson 640 @ 60Hz</strong><br>
            • Target Recognition: <strong style="color:#ef4444;">3 Human Heat Blooms Detected</strong><br>
            • Payload Status: <strong style="color:#00f0ff;">Acoustic Beacon + 2 Flotation Vests Ready</strong>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 RELEASE LIFE VEST DROP PAYLOAD", use_container_width=True):
            trigger_sfx("ping")
            st.success("Flotation payload winched down safely to rooftop survivors!")


# ==============================================================================
# TAB 3: ENVIRONMENTAL SURGE SIMULATOR
# ==============================================================================
with tab_sim:
    st.markdown("##### 🌊 Dynamic Water Level & Hazard Escalation Simulator")
    st.caption("Adjust environmental conditions to preview how floodwaters overwhelm road infrastructure and trigger automatic priority escalation.")

    surge_depth = st.slider("Flood Inundation Depth (Meters):", min_value=0.0, max_value=3.5, value=1.8, step=0.1)

    c_sim1, c_sim2 = st.columns(2)
    with c_sim1:
        if surge_depth < 0.6:
            st.success("🟢 Road Condition: ALL MAIN ARTERIAL ROADS PASSABLE\n- Wheeled Ambulances & Fire Trucks Operational.")
        elif surge_depth < 1.4:
            st.warning("🟡 Road Condition: PARTIAL SUBMERGENCE\n- High-clearance 4x4 trucks only. Normal vehicles blocked.")
        else:
            st.error("🔴 Road Condition: FULL ROAD INUNDATION (> 1.4m)\n- All wheeled vehicles will stall. INFLATABLE RESCUE BOATS MANDATORY.")

    with c_sim2:
        calc_urgency = round(min(100.0, 45.0 + surge_depth * 16.0), 1)
        st.metric("Dynamic Urgency Score", f"{calc_urgency} / 100", delta=f"+{surge_depth}m Water Surge", delta_color="inverse")


# ==============================================================================
# TAB 4: FLEET READINESS
# ==============================================================================
with tab_fleet:
    st.markdown("##### 🚒 Rescue Fleet Readiness Inventory")

    f_data = []
    for f in st.session_state.fleet:
        f_data.append({
            "Unit Code": f["id"],
            "Asset Name": f["name"],
            "Category": f["type"],
            "Status": f["status"],
            "Crew": f"{f['crew']} Pers",
            "Extraction Capacity": f"{f['capacity']} Victims",
            "Battery / Fuel": f"{f['battery']}%"
        })
    st.dataframe(pd.DataFrame(f_data), use_container_width=True, hide_index=True)
