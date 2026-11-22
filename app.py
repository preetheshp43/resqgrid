import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFilter
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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 5%, #0d1a36 0%, #060b17 65%, #020409 100%);
        color: #e2e8f0;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Top HUD Header */
    .hud-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 24px;
        background: rgba(10, 22, 48, 0.75);
        border: 1px solid rgba(0, 240, 255, 0.35);
        border-radius: 14px;
        box-shadow: 0 0 35px rgba(0, 240, 255, 0.15), inset 0 0 20px rgba(0, 240, 255, 0.05);
        backdrop-filter: blur(20px);
        margin-bottom: 20px;
    }
    
    .hud-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 22px;
        font-weight: 900;
        letter-spacing: 2.5px;
        color: #fff;
        text-shadow: 0 0 12px rgba(0, 240, 255, 0.8);
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background: rgba(12, 24, 52, 0.85);
        border: 1px solid rgba(0, 240, 255, 0.3);
        padding: 14px 20px;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), inset 0 0 12px rgba(0, 240, 255, 0.08);
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
        background: linear-gradient(135deg, rgba(16, 30, 64, 0.8) 0%, rgba(8, 16, 32, 0.95) 100%);
        border: 1px solid rgba(0, 240, 255, 0.25);
        border-left: 5px solid #ef4444;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.5);
        transition: all 0.2s ease;
    }
    .crisis-card:hover {
        border-color: rgba(0, 240, 255, 0.65);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.3);
        transform: translateY(-2px);
    }
    
    .status-pill-p1 {
        background: rgba(239, 68, 68, 0.25);
        color: #ef4444;
        border: 1px solid #ef4444;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    .status-pill-dispatched {
        background: rgba(16, 185, 129, 0.25);
        color: #10b981;
        border: 1px solid #10b981;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    /* Asset Card */
    .asset-card {
        background: rgba(13, 24, 50, 0.7);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
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
        font-size: 11px;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.85);
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
            #radar-view { width:100%; height:260px; position:relative; }
            .badge-hud { position:absolute; top:10px; left:16px; color:#00f0ff; font-size:11px; font-weight:bold; background:rgba(6,10,20,0.85); padding:5px 12px; border:1px solid rgba(0,240,255,0.4); border-radius:6px; box-shadow:0 0 10px rgba(0,240,255,0.3); pointer-events:none; }
            .grid-coords { position:absolute; bottom:10px; right:16px; color:#64748b; font-size:10px; background:rgba(6,10,20,0.85); padding:4px 10px; border-radius:4px; pointer-events:none; }
        </style>
    </head>
    <body>
        <div id="radar-view">
            <div class="badge-hud">
                <span style="color:#ef4444;">●</span> SATELLITE MESH: 32 NODES SYNCED // LIVE TELEMETRY
            </div>
            <div class="grid-coords">DRAG TO ORBIT TACTICAL PROJECTION</div>
        </div>
        <script>
            const container = document.getElementById('radar-view');
            const w = container.clientWidth || window.innerWidth;
            const h = 260;

            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x060a14, 0.035);
            const camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 1000);
            camera.position.set(0, 1.0, 6.2);

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
                new THREE.SphereGeometry(2.1, 32, 32),
                new THREE.MeshBasicMaterial({ color: 0x007799, wireframe: true, transparent: true, opacity: 0.28 })
            );
            globe.add(earthMesh);

            // Dark inner core
            globe.add(new THREE.Mesh(
                new THREE.SphereGeometry(2.05, 26, 26),
                new THREE.MeshBasicMaterial({ color: 0x091428, transparent: true, opacity: 0.85 })
            ));

            // Concentric Radar Scan Rings
            const ring1 = new THREE.Mesh(
                new THREE.RingGeometry(2.5, 2.53, 64),
                new THREE.MeshBasicMaterial({ color: 0x00f0ff, side: THREE.DoubleSide, transparent: true, opacity: 0.45 })
            );
            ring1.rotation.x = Math.PI / 2.3;
            globe.add(ring1);

            const ring2 = new THREE.Mesh(
                new THREE.RingGeometry(2.8, 2.83, 64),
                new THREE.MeshBasicMaterial({ color: 0xef4444, side: THREE.DoubleSide, transparent: true, opacity: 0.35 })
            );
            ring2.rotation.x = Math.PI / 1.7;
            ring2.rotation.y = -0.3;
            globe.add(ring2);

            // Disaster Beacons with Expanding Waves
            const coords = [
                { lat: 12.8, lon: 74.8, c: 0xef4444 },
                { lat: 25.0, lon: 45.0, c: 0xf59e0b },
                { lat: -15.0, lon: 120.0, c: 0x00f0ff },
                { lat: 35.0, lon: -95.0, c: 0xef4444 }
            ];
            const pings = [];
            coords.forEach(b => {
                const phi = (90 - b.lat) * (Math.PI / 180);
                const theta = (b.lon + 180) * (Math.PI / 180);
                const x = -(2.1 * Math.sin(phi) * Math.cos(theta));
                const z = 2.1 * Math.sin(phi) * Math.sin(theta);
                const y = 2.1 * Math.cos(phi);

                const pin = new THREE.Mesh(new THREE.SphereGeometry(0.08, 12, 12), new THREE.MeshBasicMaterial({ color: b.c }));
                pin.position.set(x, y, z);
                globe.add(pin);

                const ring = new THREE.Mesh(new THREE.RingGeometry(0.09, 0.15, 20), new THREE.MeshBasicMaterial({ color: b.c, side: THREE.DoubleSide, transparent: true, opacity: 0.9 }));
                ring.position.set(x * 1.01, y * 1.01, z * 1.01);
                ring.lookAt(x * 2, y * 2, z * 2);
                globe.add(ring);
                pings.push(ring);
            });

            // Reconnaissance Drone with Sensor Cone
            const drone = new THREE.Group();
            drone.add(new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.05, 0.32), new THREE.MeshBasicMaterial({ color: 0x00f0ff })));
            const cone = new THREE.Mesh(new THREE.ConeGeometry(0.55, 1.3, 16, 1, true), new THREE.MeshBasicMaterial({ color: 0x00f0ff, wireframe: true, transparent: true, opacity: 0.25 }));
            cone.rotation.x = Math.PI;
            cone.position.y = -0.65;
            drone.add(cone);
            scene.add(drone);

            let mouseX = 0, mouseY = 0;
            window.addEventListener('mousemove', e => {
                mouseX = (e.clientX / window.innerWidth) * 2 - 1;
                mouseY = -(e.clientY / 260) * 2 + 1;
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

                drone.position.x = Math.cos(t * 0.5) * 3.1;
                drone.position.z = Math.sin(t * 0.5) * 3.1;
                drone.position.y = 0.7 + Math.sin(t * 1.4) * 0.3;
                drone.lookAt(0, 0, 0);

                renderer.render(scene, camera);
            }
            animate();
        </script>
    </body>
    </html>
    """, height=270, scrolling=False)


# ==============================================================================
# 4. CRISIS DATA ENGINE & STATE
# ==============================================================================
SESSION_VERSION = "4.0"
if st.session_state.get("session_version") != SESSION_VERSION:
    st.session_state.clear()
    st.session_state["session_version"] = SESSION_VERSION

if "incidents" not in st.session_state:
    st.session_state.incidents = [
        {
            "id": "CRISIS-DELTA-1",
            "title": "Catastrophic Flash Flood: Submerged Urban Settlement",
            "type": "Flash Flood",
            "lat": 12.8465,
            "lng": 74.8624,
            "sector": "Jeppinamogaru River Basin",
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
        {"id": "RESCUE-01", "name": "NDRF Gemini Boat Alpha", "type": "Watercraft", "status": "AVAILABLE", "crew": 6, "capacity": 12, "battery": 96, "equipment": "Yamaha 40HP, Lifejackets (25)"},
        {"id": "RESCUE-02", "name": "Eagle-X Recon Drone", "type": "FLIR Thermal UAV", "status": "AVAILABLE", "crew": 2, "capacity": 2, "battery": 89, "equipment": "FLIR Boson 640, Winch (8kg)"},
        {"id": "RESCUE-03", "name": "Heavy Foam Tender FT-07", "type": "Fire Suppression", "status": "AVAILABLE", "crew": 6, "capacity": 4, "battery": 92, "equipment": "4500L AFFF Foam, Jaws of Life"},
        {"id": "RESCUE-04", "name": "Hazmat Trauma Unit", "type": "Advanced Life Support", "status": "AVAILABLE", "crew": 4, "capacity": 3, "battery": 85, "equipment": "Ventilator, Defibrillator, Decon"},
        {"id": "RESCUE-05", "name": "SDRF Rescue Squad 3", "type": "Heavy Shoring", "status": "EN ROUTE", "crew": 8, "capacity": 8, "battery": 78, "equipment": "Pneumatic Jackhammers, Fiberscope"}
    ]

if "survivors_extracted" not in st.session_state:
    st.session_state.survivors_extracted = 42


# ==============================================================================
# 5. HEADER HUD
# ==============================================================================
st.markdown("""
<div class="hud-header">
    <div style="display:flex; align-items:center; gap:16px;">
        <span style="font-size:30px; filter: drop-shadow(0 0 10px #00f0ff);">⚡</span>
        <div>
            <div class="hud-title">RESQGRID <span style="color:#00f0ff;">WAR ROOM</span></div>
            <div style="font-size:11px; color:#64748b; font-family:'JetBrains Mono', monospace;">AUTONOMOUS INCIDENT DISPATCH & COMBINATORIAL RESOURCE RESCUE MESH</div>
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
open_incidents = [i for i in st.session_state.incidents if i.get("status") != "RESOLVED"]
trapped_lives = sum(i.get("trapped", i.get("trapped_victims", 2)) for i in open_incidents)
units_deployed = len([f for f in st.session_state.fleet if f.get("status") in ["EN ROUTE", "ON SCENE"]])

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Critical Sectors", f"{len(open_incidents)} Active")
m2.metric("Lives in Direct Peril", f"{trapped_lives} Trapped", delta="Critical", delta_color="inverse")
m3.metric("Fleet Deployed", f"{units_deployed} / {len(st.session_state.fleet)} Units", delta="Active")
m4.metric("Survivors Rescued", f"{st.session_state.survivors_extracted} Saved", delta="+6 this turn")
m5.metric("Decision Latency", "0.82s", delta="Real-time")

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
        # Map view mode toggle: Folium Dark / Satellite vs PyDeck Carto
        map_mode = st.radio("Map Cartography Mode:", ["🛰️ Satellite Hybrid GIS (High-Res Aerial)", "🌐 3D Column Elevation (Carto Dark)"], horizontal=True)

        if "Satellite" in map_mode:
            # Folium with Satellite Hybrid imagery & Carto Dark
            m = folium.Map(location=[12.8950, 74.8500], zoom_start=12, tiles=None)
            
            # Base Layer 1: Dark Matter
            folium.TileLayer('CartoDB dark_matter', name='Tactical Dark GIS').add_to(m)
            # Base Layer 2: Real Satellite Imagery
            folium.TileLayer(
                tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr='Esri World Imagery',
                name='Satellite High-Res Aerial',
                overlay=False,
                control=True
            ).add_to(m)

            # Add Incidents with Danger Perimeters
            for inc in open_incidents:
                lat = inc.get("lat", 12.85)
                lng = inc.get("lng", 74.85)
                title = inc.get("title", "Emergency")
                tr = inc.get("trapped", 2)
                is_crit = "CRITICAL" in inc.get("priority", "CRITICAL P1")
                col = "#ef4444" if is_crit else "#f59e0b"

                # Danger radius circle
                folium.Circle(
                    location=[lat, lng],
                    radius=500,
                    color=col,
                    fill=True,
                    fill_color=col,
                    fill_opacity=0.25,
                    weight=1.5
                ).add_to(m)

                # Core Marker
                folium.CircleMarker(
                    location=[lat, lng],
                    radius=9,
                    color=col,
                    fill=True,
                    fill_color="#fff",
                    fill_opacity=0.9,
                    weight=3,
                    tooltip=f"🚨 {title} ({tr} trapped)"
                ).add_to(m)

            # Blocked Road & Safe Route Corridor
            folium.PolyLine(
                [[12.8480, 74.8580], [12.8465, 74.8624], [12.8450, 74.8670]],
                color="#ef4444",
                weight=5,
                tooltip="BLOCKED: NH-66 Submerged 1.8m"
            ).add_to(m)

            folium.PolyLine(
                [[12.8715, 74.8450], [12.8600, 74.8550], [12.8465, 74.8624]],
                color="#10b981",
                weight=4,
                dash_array="6, 6",
                tooltip="AI SAFE BYPASS: Elevated Ring Road Corridor"
            ).add_to(m)

            folium.LayerControl(position='topright').add_to(m)
            st_folium(m, width="100%", height=400)
        
        else:
            # PyDeck with 100% Free Carto Dark Style (Zero Mapbox Token Required!)
            pts = []
            for inc in open_incidents:
                dmg = inc.get("damage_pct", inc.get("damage_score", 85))
                tr = inc.get("trapped", inc.get("trapped_victims", 2))
                is_crit = "CRITICAL" in inc.get("priority", "CRITICAL P1")
                pts.append({
                    "title": inc.get("title", "Emergency Crisis"),
                    "lat": inc.get("lat", 12.85),
                    "lng": inc.get("lng", 74.85),
                    "elevation": dmg * 35,
                    "color": [239, 68, 68, 220] if is_crit else [245, 158, 11, 220],
                    "radius": tr * 50 + 150
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

            # Using free Carto Dark Matter style URL
            st.pydeck_chart(pdk.Deck(
                layers=[cols_3d, rings],
                initial_view_state=view,
                map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
                tooltip={"text": "🚨 {title}\nDamage: {elevation}"}
            ), use_container_width=True)

        # Quick Disaster Trigger Buttons
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
                    "sector": "Someshwar Coastal Settlement",
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
            if st.button("⚡ AUTO-OPTIMIZE ALL", use_container_width=True):
                for inc in st.session_state.incidents:
                    if inc.get("status") != "RESOLVED":
                        inc["status"] = "UNITS EN ROUTE"
                for f in st.session_state.fleet:
                    f["status"] = "EN ROUTE"
                trigger_sfx("dispatch")
                st.rerun()

    with col_actions:
        st.markdown("##### 🚨 Active Crisis Queue & One-Click Execution")

        for inc in open_incidents:
            is_dispatched = "EN ROUTE" in inc.get("status", "") or "DISPATCHED" in inc.get("status", "")
            inc_id = inc.get("id", "CRISIS")
            title = inc.get("title", "Active Crisis")
            sector = inc.get("sector", inc.get("location_name", inc.get("address", "Sector Hub")))
            trapped = inc.get("trapped", inc.get("trapped_victims", 2))
            time_to_crest = inc.get("time_to_crest", "25 Mins")
            ai_action = inc.get("ai_action", inc.get("solution_summary", "Deploy rescue unit"))
            status = inc.get("status", "IMMEDIATE DISPATCH REQUIRED")
            units_needed = inc.get("units_needed", inc.get("recommended_units", []))

            st.markdown(f"""
            <div class="crisis-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#00f0ff; font-weight:bold; font-size:12px;">{inc_id}</span>
                    <span class="{'status-pill-dispatched' if is_dispatched else 'status-pill-p1'}">
                        {status}
                    </span>
                </div>
                <div style="font-size:14px; font-weight:800; color:#fff; margin-bottom:4px;">{title}</div>
                <div style="font-size:11px; color:#94a3b8; margin-bottom:6px;">
                    📍 {sector} • Trapped: <strong style="color:#ef4444;">{trapped} lives</strong> • Window: <strong style="color:#f59e0b;">{time_to_crest}</strong>
                </div>
                <div style="background:rgba(6,10,20,0.7); border:1px solid rgba(0,240,255,0.2); padding:8px 12px; border-radius:6px; font-size:11px; margin-bottom:10px;">
                    <strong style="color:#00f0ff;">AI RECOMMENDED MOVE:</strong><br>
                    {ai_action}
                </div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2 = st.columns([1, 1])
            with b1:
                if not is_dispatched:
                    if st.button(f"⚡ AUTHORIZE DISPATCH", key=f"disp_{inc_id}", use_container_width=True):
                        inc["status"] = "UNITS EN ROUTE"
                        for u in units_needed:
                            match = next((f for f in st.session_state.fleet if f.get("name") == u), None)
                            if match:
                                match["status"] = "EN ROUTE"
                        trigger_sfx("dispatch")
                        st.rerun()
            with b2:
                if st.button(f"✅ CONFIRM RESCUE", key=f"res_{inc_id}", use_container_width=True):
                    inc["status"] = "RESOLVED"
                    st.session_state.survivors_extracted += trapped
                    for f in st.session_state.fleet:
                        f["status"] = "AVAILABLE"
                    trigger_sfx("dispatch")
                    st.rerun()


# ==============================================================================
# TAB 2: FLIR THERMAL DRONE RECON COCKPIT (HIGH-RES CANVAS)
# ==============================================================================
with tab_drone:
    st.markdown("##### 🛸 FLIR Thermal Reconnaissance Drone Video Cockpit")
    st.caption("Live high-altitude thermal UAV feed scanning target coordinates with real-time target recognition and avionics telemetry.")

    col_flir, col_telemetry = st.columns([7, 5])

    with col_flir:
        # Realistic Thermal Canvas in HTML5/JS
        components.html("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { margin:0; padding:0; background:#040711; overflow:hidden; font-family:'Courier New', monospace; }
                #hud-canvas { width:100%; height:340px; display:block; border:1px solid rgba(0,240,255,0.4); border-radius:10px; }
            </style>
        </head>
        <body>
            <canvas id="hud-canvas" width="640" height="340"></canvas>
            <script>
                const canvas = document.getElementById('hud-canvas');
                const ctx = canvas.getContext('2d');
                let t = 0;

                function drawFLIR() {
                    t += 0.03;
                    ctx.clearRect(0, 0, 640, 340);

                    // Background Thermal Palette (Ironbow gradient)
                    let grad = ctx.createLinearGradient(0, 0, 0, 340);
                    grad.addColorStop(0, '#10062a');
                    grad.addColorStop(0.5, '#2c0c4d');
                    grad.addColorStop(1, '#0c1a40');
                    ctx.fillStyle = grad;
                    ctx.fillRect(0, 0, 640, 340);

                    // River / Floodwater gradient
                    ctx.fillStyle = '#06132e';
                    ctx.fillRect(0, 150, 640, 190);

                    // Structural silhouettes
                    ctx.fillStyle = '#4a154b';
                    ctx.fillRect(100, 100, 130, 120);
                    ctx.beginPath();
                    ctx.moveTo(90, 100); ctx.lineTo(165, 45); ctx.lineTo(240, 100);
                    ctx.fillStyle = '#6b1b4d'; ctx.fill();

                    ctx.fillStyle = '#3c1852';
                    ctx.fillRect(360, 110, 140, 130);
                    ctx.beginPath();
                    ctx.moveTo(350, 110); ctx.lineTo(430, 60); ctx.lineTo(510, 110);
                    ctx.fillStyle = '#5c1b52'; ctx.fill();

                    // Thermal Heat Signatures (Survivors on rooftop) - Intense Orange/White blooms
                    const heatColors = ['#ffea00', '#ff5500', '#ffffff'];
                    for(let i = 0; i < 4; i++) {
                        let hx = 130 + i * 22 + Math.sin(t + i) * 1.5;
                        let hy = 75 + Math.cos(t * 1.2 + i) * 1.5;
                        
                        let rad = ctx.createRadialGradient(hx, hy, 2, hx, hy, 16);
                        rad.addColorStop(0, '#ffffff');
                        rad.addColorStop(0.3, '#ffaa00');
                        rad.addColorStop(0.8, '#ff2200');
                        rad.addColorStop(1, 'transparent');
                        ctx.fillStyle = rad;
                        ctx.beginPath();
                        ctx.arc(hx, hy, 16, 0, Math.PI * 2);
                        ctx.fill();
                    }

                    // Artificial Horizon Ladder
                    ctx.strokeStyle = 'rgba(0, 240, 255, 0.4)';
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(270, 170); ctx.lineTo(310, 170);
                    ctx.moveTo(330, 170); ctx.lineTo(370, 170);
                    ctx.moveTo(285, 140); ctx.lineTo(355, 140);
                    ctx.moveTo(285, 200); ctx.lineTo(355, 200);
                    ctx.stroke();

                    // Center Crosshair Reticle
                    ctx.strokeStyle = '#00f0ff';
                    ctx.lineWidth = 1.5;
                    ctx.beginPath();
                    ctx.arc(320, 170, 24, 0, Math.PI * 2);
                    ctx.moveTo(320, 130); ctx.lineTo(320, 160);
                    ctx.moveTo(320, 180); ctx.lineTo(320, 210);
                    ctx.moveTo(280, 170); ctx.lineTo(310, 170);
                    ctx.moveTo(330, 170); ctx.lineTo(360, 170);
                    ctx.stroke();

                    // Target Tracking Box
                    ctx.strokeStyle = '#10b981';
                    ctx.lineWidth = 2;
                    let pulse = Math.sin(t * 3) * 3;
                    ctx.strokeRect(115 - pulse/2, 50 - pulse/2, 95 + pulse, 50 + pulse);
                    ctx.fillStyle = '#10b981';
                    ctx.font = '10px monospace';
                    ctx.fillText('[TARGET LOCK: 4 SURVIVORS]', 115, 42);

                    // Top Compass Heading Tape
                    ctx.fillStyle = 'rgba(6,10,20,0.7)';
                    ctx.fillRect(200, 8, 240, 24);
                    ctx.strokeStyle = 'rgba(0,240,255,0.5)';
                    ctx.strokeRect(200, 8, 240, 24);
                    ctx.fillStyle = '#00f0ff';
                    ctx.font = '11px monospace';
                    ctx.fillText('030° • • • 045° NE • • • 060°', 215, 24);

                    // OSD Telemetry Overlays
                    ctx.fillStyle = '#00f0ff';
                    ctx.font = '11px monospace';
                    ctx.fillText('ALT: 124m AGL', 20, 30);
                    ctx.fillText('SPD: 48.2 km/h', 20, 48);
                    ctx.fillText('FLIR: 640x512 60Hz', 20, 66);
                    ctx.fillText('GPS: 12.8465°N, 74.8624°E', 20, 320);

                    ctx.fillStyle = '#ef4444';
                    ctx.fillText('REC ● 00:14:32', 530, 30);
                    ctx.fillStyle = '#10b981';
                    ctx.fillText('BATT: 89%', 545, 48);

                    requestAnimationFrame(drawFLIR);
                }
                drawFLIR();
            </script>
        </body>
        </html>
        """, height=355)

    with col_telemetry:
        st.markdown("###### 📊 UAV Recon Eagle-X Avionics Telemetry")
        st.markdown("""
        <div style="background:rgba(8,16,36,0.85); border:1px solid rgba(0,240,255,0.3); border-radius:12px; padding:18px; font-size:12px; line-height:2.0;">
            • Tactical Airframe: <strong style="color:#00f0ff;">Eagle-X Hexacopter Heavy Recon</strong><br>
            • Operating Ceiling: <strong>124m AGL (Above Ground Level)</strong><br>
            • Thermal Sensor: <strong style="color:#10b981;">FLIR Boson 640 @ 60Hz Radiometric</strong><br>
            • Live Target Identification: <strong style="color:#ef4444;">4 Heat Blooms Confirmed on Terrace</strong><br>
            • Slant Rangefinder: <strong>480 meters (Laser TOF Valid)</strong><br>
            • Winch Payload: <strong style="color:#00f0ff;">2x Flotation Lifejackets + Acoustic Beacon</strong>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 RELEASE LIFE VEST DROP WINCH", use_container_width=True):
            trigger_sfx("ping")
            st.success("Winch deployed: Life jackets and acoustic beacon dropped safely to survivors!")


# ==============================================================================
# TAB 3: ENVIRONMENTAL SURGE SIMULATOR (PLOTLY CHARTS)
# ==============================================================================
with tab_sim:
    st.markdown("##### 🌊 Dynamic Water Level & Infrastructure Vulnerability Simulator")
    st.caption("Simulate rising flood crests over the next 6 hours to preview road submergence and infrastructure breakdown in real-time.")

    c_slider, c_score = st.columns([8, 4])
    with c_slider:
        surge_depth = st.slider("Simulated Flood Inundation Depth (Meters):", min_value=0.0, max_value=3.5, value=1.8, step=0.1)

    with c_score:
        calc_urgency = round(min(100.0, 42.0 + surge_depth * 17.0), 1)
        st.metric("Dynamic Urgency Index", f"{calc_urgency} / 100", delta=f"+{surge_depth}m Water Surge", delta_color="inverse")

    # Interactive Plotly Hydrograph Curve
    hours = np.linspace(0, 6, 25)
    baseline_water = surge_depth + 0.4 * np.sin(hours * 0.8) + (hours * 0.15)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours,
        y=baseline_water,
        mode='lines+markers',
        name='Predicted Flood Crest (m)',
        line=dict(color='#00f0ff', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 240, 255, 0.15)'
    ))

    # Critical Road Submergence Line
    fig.add_hline(
        y=1.4,
        line_dash="dash",
        line_color="#ef4444",
        annotation_text="Critical Road Inundation Cutoff (1.4m)",
        annotation_position="top left"
    )

    fig.update_layout(
        title="6-Hour Hydrographic Floodwater Elevation Projection",
        xaxis_title="Hours From Now",
        yaxis_title="Water Depth Above Ground (Meters)",
        template="plotly_dark",
        paper_bgcolor='rgba(6,10,20,0.8)',
        plot_bgcolor='rgba(10,20,40,0.5)',
        font=dict(family="JetBrains Mono, monospace", color="#cbd5e1"),
        height=320,
        margin=dict(l=40, r=40, t=50, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Road Condition Alert
    if surge_depth < 0.6:
        st.success("🟢 Road Status: ALL ARTERIAL HIGHWAYS OPEN • Wheeled ALS Ambulances & Fire Trucks Operating.")
    elif surge_depth < 1.4:
        st.warning("🟡 Road Status: PARTIAL SUBMERGENCE (Caution) • 4x4 Heavy Rescue Trucks Required.")
    else:
        st.error("🔴 Road Status: FULL HIGHWAY SUBMERGENCE (> 1.4m) • All Wheeled Convoys Stalled. Inflatable Boats Mandatory.")


# ==============================================================================
# TAB 4: FLEET READINESS
# ==============================================================================
with tab_fleet:
    st.markdown("##### 🚒 Rescue Fleet Readiness & Asset Cards")
    st.caption("Monitor power/fuel meters, equipment inventories, and deploy individual units directly to open crisis sectors.")

    col_f1, col_f2 = st.columns(2)

    for idx, f in enumerate(st.session_state.fleet):
        target_col = col_f1 if idx % 2 == 0 else col_f2
        is_avail = f.get("status") == "AVAILABLE"
        badge_style = "status-pill-dispatched" if not is_avail else "status-pill-p1"
        
        with target_col:
            st.markdown(f"""
            <div class="asset-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="color:#00f0ff; font-weight:bold; font-size:13px;">{f.get('id')} — {f.get('name')}</span>
                    <span class="{badge_style}">{f.get('status')}</span>
                </div>
                <div style="font-size:12px; color:#cbd5e1; margin-bottom:8px;">
                    • Category: <strong>{f.get('type')}</strong><br>
                    • Equipment: <span style="color:#94a3b8;">{f.get('equipment', 'Standard SAR Gear')}</span><br>
                    • Crew Size: <strong>{f.get('crew', 4)} Specialists</strong> • Extraction Capacity: <strong style="color:#10b981;">{f.get('capacity', 4)} Survivors</strong>
                </div>
                <div style="margin-top:8px;">
                    <span style="font-size:10px; color:#94a3b8;">BATTERY / FUEL CHARGE ({f.get('battery', 90)}%)</span>
                    <div style="background:rgba(255,255,255,0.1); border-radius:6px; height:8px; width:100%; overflow:hidden;">
                        <div style="background:linear-gradient(90deg, #00f0ff, #10b981); height:100%; width:{f.get('battery', 90)}%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if is_avail:
                if st.button(f"⚡ DEPLOY {f.get('id')}", key=f"f_dep_{f.get('id')}", use_container_width=True):
                    f["status"] = "EN ROUTE"
                    trigger_sfx("dispatch")
                    st.rerun()
            else:
                if st.button(f"🔄 RECALL {f.get('id')} TO BASE", key=f"f_rec_{f.get('id')}", use_container_width=True):
                    f["status"] = "AVAILABLE"
                    trigger_sfx("ping")
                    st.rerun()
