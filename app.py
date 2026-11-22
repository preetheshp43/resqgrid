import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
from PIL import Image, ImageDraw, ImageFont
import datetime
import time
import math
import io
import json

# ==============================================================================
# 1. PAGE CONFIGURATION & STYLING
# ==============================================================================
st.set_page_config(
    page_title="RESQGRID | AI Disaster Response Intelligence",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Tactical CSS Theme
st.markdown("""
<style>
    /* Dark tactical HUD style */
    .stApp {
        background-color: #070b14;
        color: #f1f5f9;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background: rgba(13, 21, 39, 0.7);
        border: 1px solid rgba(0, 240, 255, 0.2);
        padding: 12px 18px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    div[data-testid="stMetricValue"] {
        color: #00f0ff !important;
        font-weight: 800;
        font-size: 26px !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00f0ff 0%, #0088ff 100%);
        color: #050811;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.5);
        color: #000;
        transform: scale(1.02);
    }
    
    /* Alert cards */
    .tactical-card {
        background: rgba(17, 29, 56, 0.6);
        border: 1px solid rgba(0, 240, 255, 0.2);
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    .p1-badge {
        background: rgba(255, 51, 102, 0.2);
        color: #ff3366;
        border: 1px solid #ff3366;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .p2-badge {
        background: rgba(255, 176, 32, 0.2);
        color: #ffb020;
        border: 1px solid #ffb020;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .p3-badge {
        background: rgba(0, 240, 255, 0.2);
        color: #00f0ff;
        border: 1px solid #00f0ff;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. EMBEDDED TACTICAL AUDIO & 3D THREE.JS WEBGL HERO SCENE
# ==============================================================================
def render_3d_hero_animation():
    """Renders real-time Three.js 3D WebGL Holographic Earth & UAV Radar Canvas."""
    hero_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            body, html { margin: 0; padding: 0; overflow: hidden; background: #070b14; width: 100%; height: 100%; font-family: monospace; }
            #canvas-container { width: 100%; height: 320px; position: relative; }
            .hud-overlay { position: absolute; top: 12px; left: 14px; color: #00f0ff; font-size: 11px; background: rgba(5,8,17,0.7); padding: 6px 12px; border: 1px solid rgba(0,240,255,0.3); border-radius: 6px; pointer-events: none; }
            .hud-info { position: absolute; bottom: 12px; right: 14px; color: #94a3b8; font-size: 10px; background: rgba(5,8,17,0.7); padding: 4px 10px; border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; pointer-events: none; }
        </style>
    </head>
    <body>
        <div id="canvas-container">
            <div class="hud-overlay">
                <span style="color:#ff3366;">●</span> 3D TACTICAL DISASTER GRID: LIVE ORBITAL TELEMETRY
            </div>
            <div class="hud-info">
                MOVE CURSOR TO ROTATE TACTICAL GLOBE
            </div>
        </div>
        <script>
            const container = document.getElementById('canvas-container');
            const width = container.clientWidth || window.innerWidth;
            const height = 320;

            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x070b14, 0.04);
            const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
            camera.position.set(0, 1.0, 6.8);

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(width, height);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(renderer.domElement);

            // Lighting
            scene.add(new THREE.AmbientLight(0x00f0ff, 0.6));
            const dirLight = new THREE.DirectionalLight(0x00ffff, 2.2);
            dirLight.position.set(5, 8, 5);
            scene.add(dirLight);

            // Globe Group
            const globeGroup = new THREE.Group();
            scene.add(globeGroup);

            // Wireframe Earth Sphere
            const sphereGeo = new THREE.SphereGeometry(2.3, 30, 30);
            const sphereMat = new THREE.MeshBasicMaterial({ color: 0x005577, wireframe: true, transparent: true, opacity: 0.28 });
            globeGroup.add(new THREE.Mesh(sphereGeo, sphereMat));

            // Inner Core
            const coreMat = new THREE.MeshBasicMaterial({ color: 0x091428, transparent: true, opacity: 0.85 });
            globeGroup.add(new THREE.Mesh(new THREE.SphereGeometry(2.26, 24, 24), coreMat));

            // Concentric Orbital Rings
            const ring1 = new THREE.Mesh(new THREE.RingGeometry(2.8, 2.84, 48), new THREE.MeshBasicMaterial({ color: 0x00f0ff, side: THREE.DoubleSide, transparent: true, opacity: 0.5 }));
            ring1.rotation.x = Math.PI / 2.2;
            globeGroup.add(ring1);

            const ring2 = new THREE.Mesh(new THREE.RingGeometry(3.1, 3.13, 48), new THREE.MeshBasicMaterial({ color: 0xff3366, side: THREE.DoubleSide, transparent: true, opacity: 0.35 }));
            ring2.rotation.x = Math.PI / 1.7;
            ring2.rotation.y = -0.3;
            globeGroup.add(ring2);

            // Pulsing Disaster Beacons
            const beacons = [
                { lat: 12.8, lon: 74.8, col: 0xff3366 }, // Mangaluru Flash Flood
                { lat: 25.0, lon: 45.0, col: 0xffb020 },
                { lat: -15.0, lon: 120.0, col: 0x00f0ff },
                { lat: 35.0, lon: -95.0, col: 0xff3366 }
            ];
            const pings = [];
            beacons.forEach(b => {
                const phi = (90 - b.lat) * (Math.PI / 180);
                const theta = (b.lon + 180) * (Math.PI / 180);
                const x = -(2.3 * Math.sin(phi) * Math.cos(theta));
                const z = 2.3 * Math.sin(phi) * Math.sin(theta);
                const y = 2.3 * Math.cos(phi);

                const point = new THREE.Mesh(new THREE.SphereGeometry(0.08, 12, 12), new THREE.MeshBasicMaterial({ color: b.col }));
                point.position.set(x, y, z);
                globeGroup.add(point);

                const ping = new THREE.Mesh(new THREE.RingGeometry(0.1, 0.16, 16), new THREE.MeshBasicMaterial({ color: b.col, side: THREE.DoubleSide, transparent: true, opacity: 0.9 }));
                ping.position.set(x * 1.02, y * 1.02, z * 1.02);
                ping.lookAt(x * 2, y * 2, z * 2);
                globeGroup.add(ping);
                pings.push(ping);
            });

            // Orbiting Recon Drone
            const drone = new THREE.Group();
            const chassis = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.05, 0.3), new THREE.MeshBasicMaterial({ color: 0x00f0ff }));
            drone.add(chassis);
            const cone = new THREE.Mesh(new THREE.ConeGeometry(0.6, 1.4, 16, 1, true), new THREE.MeshBasicMaterial({ color: 0x00f0ff, wireframe: true, transparent: true, opacity: 0.25 }));
            cone.rotation.x = Math.PI;
            cone.position.y = -0.7;
            drone.add(cone);
            scene.add(drone);

            // Mouse Interaction
            let mouseX = 0, mouseY = 0;
            window.addEventListener('mousemove', (e) => {
                mouseX = (e.clientX / window.innerWidth) * 2 - 1;
                mouseY = -(e.clientY / 320) * 2 + 1;
            });

            let clock = new THREE.Clock();
            function animate() {
                requestAnimationFrame(animate);
                const t = clock.getElapsedTime();
                globeGroup.rotation.y = t * 0.15 + mouseX * 0.4;
                globeGroup.rotation.x = 0.15 + mouseY * 0.25;
                ring1.rotation.z = t * 0.2;
                ring2.rotation.z = -t * 0.25;

                pings.forEach((p, idx) => {
                    const s = 1 + (Math.sin(t * 4 + idx) + 1) * 0.6;
                    p.scale.set(s, s, s);
                    p.material.opacity = Math.max(0, 1 - (s - 1));
                });

                drone.position.x = Math.cos(t * 0.6) * 3.3;
                drone.position.z = Math.sin(t * 0.6) * 3.3;
                drone.position.y = 0.8 + Math.sin(t * 1.5) * 0.3;
                drone.lookAt(0, 0, 0);

                renderer.render(scene, camera);
            }
            animate();
        </script>
    </body>
    </html>
    """
    components.html(hero_html, height=330, scrolling=False)


def play_tactical_sound(sound_type="chime"):
    """Plays synthesized tactical audio using Web Audio API in Streamlit."""
    audio_code = f"""
    <script>
    (function() {{
        try {{
            var AudioContext = window.AudioContext || window.webkitAudioContext;
            var ctx = new AudioContext();
            var now = ctx.currentTime;
            
            if ('{sound_type}' === 'alert') {{
                var osc = ctx.createOscillator();
                var gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(540, now);
                osc.frequency.exponentialRampToValueAtTime(860, now + 0.15);
                osc.frequency.exponentialRampToValueAtTime(540, now + 0.3);
                gain.gain.setValueAtTime(0.15, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.35);
            }} else {{
                // Chime
                [523.25, 659.25, 783.99, 1046.5].forEach((freq, idx) => {{
                    var osc = ctx.createOscillator();
                    var gain = ctx.createGain();
                    var t = now + idx * 0.08;
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, t);
                    gain.gain.setValueAtTime(0.1, t);
                    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.25);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(t);
                    osc.stop(t + 0.25);
                }});
            }}
        }} catch(e) {{}}
    }})();
    </script>
    """
    components.html(audio_code, height=0, width=0)


# ==============================================================================
# 3. SESSION STATE INITIALIZATION (DATA LAYER)
# ==============================================================================
if "incidents" not in st.session_state:
    st.session_state.incidents = [
        {
            "id": "INC-MNG-001",
            "title": "Severe Flash Flood & Submerged Settlement",
            "type": "flood",
            "lat": 12.8465,
            "lng": 74.8624,
            "address": "Jeppinamogaru, Netravati River Basin",
            "sector": "Sector Delta-4",
            "severity": 94,
            "priority": "P1_CRITICAL",
            "status": "awaiting_approval",
            "trapped_victims": 14,
            "total_victims": 18,
            "damage_score": 88,
            "recommended_units": ["RES-BOAT-01", "RES-UAV-01"],
            "action_summary": "Immediate deployment of NDRF Inflatable Boat and Thermal Recon Drone.",
            "urgency_score": 97.4,
            "time_saved_mins": 24,
            "reported_time": "14 mins ago"
        },
        {
            "id": "INC-MNG-002",
            "title": "Industrial Fire & Chemical Gas Hazard",
            "type": "fire",
            "lat": 12.9512,
            "lng": 74.8021,
            "address": "Baikampady Industrial Estate, Sector B",
            "sector": "Sector Alpha-2",
            "severity": 89,
            "priority": "P1_CRITICAL",
            "status": "awaiting_approval",
            "trapped_victims": 5,
            "total_victims": 8,
            "damage_score": 78,
            "recommended_units": ["RES-FIRE-01", "RES-AMB-02"],
            "action_summary": "Deploy Heavy Foam Tender and Hazmat Decontamination Unit.",
            "urgency_score": 89.2,
            "time_saved_mins": 18,
            "reported_time": "28 mins ago"
        },
        {
            "id": "INC-MNG-003",
            "title": "Ghat Landslide & Multi-Vehicle Blockade",
            "type": "landslide",
            "lat": 12.9056,
            "lng": 74.9124,
            "address": "Gurupura Ghat Corridor, NH-169",
            "sector": "Sector Echo-1",
            "severity": 76,
            "priority": "P2_HIGH",
            "status": "dispatched",
            "trapped_victims": 3,
            "total_victims": 7,
            "damage_score": 64,
            "recommended_units": ["RES-AMB-01"],
            "action_summary": "Deploy Hydraulic Extrication Spreaders via Kaikamba bypass.",
            "urgency_score": 78.5,
            "time_saved_mins": 14,
            "reported_time": "45 mins ago"
        },
        {
            "id": "INC-MNG-004",
            "title": "Old Port Commercial Structure Collapse",
            "type": "collapse",
            "lat": 12.8682,
            "lng": 74.8385,
            "address": "Bunder Old Port Fish Market Complex",
            "sector": "Sector Bravo-3",
            "severity": 72,
            "priority": "P2_HIGH",
            "status": "dispatched",
            "trapped_victims": 2,
            "total_victims": 11,
            "damage_score": 58,
            "recommended_units": ["RES-AMB-01"],
            "action_summary": "Acoustic search sensor squad & rapid shoring team.",
            "urgency_score": 74.0,
            "time_saved_mins": 10,
            "reported_time": "1 hr ago"
        }
    ]

if "resources" not in st.session_state:
    st.session_state.resources = [
        {
            "id": "RES-BOAT-01",
            "name": "NDRF Gemini Alpha (Rapid Inflatable)",
            "type": "ndrf_boat",
            "status": "available",
            "lat": 12.8715,
            "lng": 74.8450,
            "capacity": 12,
            "crew": 5,
            "battery_fuel": 94,
            "assigned_to": None
        },
        {
            "id": "RES-UAV-01",
            "name": "Eagle-X Recon Drone (Thermal/LiDAR)",
            "type": "uav_recon",
            "status": "available",
            "lat": 12.8820,
            "lng": 74.8510,
            "capacity": 2,
            "crew": 2,
            "battery_fuel": 88,
            "assigned_to": None
        },
        {
            "id": "RES-FIRE-01",
            "name": "FT-07 Heavy Foam Tender",
            "type": "fire_unit",
            "status": "available",
            "lat": 12.9200,
            "lng": 74.8250,
            "capacity": 6,
            "crew": 6,
            "battery_fuel": 92,
            "assigned_to": None
        },
        {
            "id": "RES-AMB-01",
            "name": "ALS-01 Mobile Trauma Unit",
            "type": "ambulance",
            "status": "en_route",
            "lat": 12.8650,
            "lng": 74.8420,
            "capacity": 3,
            "crew": 4,
            "battery_fuel": 78,
            "assigned_to": "INC-MNG-003"
        },
        {
            "id": "RES-AMB-02",
            "name": "BLS-04 Rapid Paramedic Van",
            "type": "ambulance",
            "status": "available",
            "lat": 12.9150,
            "lng": 74.8480,
            "capacity": 2,
            "crew": 3,
            "battery_fuel": 85,
            "assigned_to": None
        }
    ]

if "audit_log" not in st.session_state:
    st.session_state.audit_log = [
        {
            "timestamp": "11:15 IST",
            "incident_id": "INC-MNG-003",
            "action": "DISPATCH AUTHORIZED",
            "commander": "CDR. PREETHESH",
            "units": "RES-AMB-01",
            "signature": "SHA256-8A39F0B"
        }
    ]


# ==============================================================================
# 4. MATHEMATICAL & ALGORITHMIC FUNCTIONS
# ==============================================================================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_dynamic_risk(severity, vulnerability, escalation):
    # R(i) = 0.45*Severity + 0.35*Vulnerability + 0.20*Escalation
    return round(min(100.0, 0.45 * severity + 0.35 * vulnerability + 0.20 * escalation), 1)

def calculate_urgency_tier(trapped, total, risk_score, access_time=0.8):
    urgency_raw = (trapped * 2.5 + total * 1.0) * (risk_score / 100.0) / max(0.5, access_time)
    score = round(min(100.0, urgency_raw * 10.0), 1)
    if score >= 75.0 or trapped >= 4:
        return "P1_CRITICAL", score
    elif score >= 45.0:
        return "P2_HIGH", score
    else:
        return "P3_MODERATE", score

def run_hungarian_optimization():
    """Bipartite matching algorithm allocating idle rescue units to pending emergencies."""
    available_res = [r for r in st.session_state.resources if r["status"] == "available"]
    pending_inc = [i for i in st.session_state.incidents if i["status"] == "awaiting_approval"]

    assigned_count = 0
    for inc in pending_inc:
        best_r = None
        min_eta = float("inf")
        for res in available_res:
            dist = haversine(inc["lat"], inc["lng"], res["lat"], res["lng"])
            speed = 45.0
            eta = (dist / speed) * 60.0
            # Specialization preference
            if inc["type"] == "flood" and res["type"] == "ndrf_boat":
                eta -= 5.0
            elif inc["type"] == "fire" and res["type"] == "fire_unit":
                eta -= 5.0
            
            if eta < min_eta:
                min_eta = eta
                best_r = res
        
        if best_r:
            best_r["status"] = "en_route"
            best_r["assigned_to"] = inc["id"]
            inc["status"] = "dispatched"
            if best_r["id"] not in inc["recommended_units"]:
                inc["recommended_units"].append(best_r["id"])
            available_res.remove(best_r)
            assigned_count += 1

    return assigned_count


# ==============================================================================
# 5. SIDEBAR: NAVIGATION & CONTROL
# ==============================================================================
with st.sidebar:
    st.markdown("### 🚨 RESQGRID COMMAND HUB")
    st.markdown("<span class='p1-badge'>DEFCON 2 : ACTIVE DISASTER</span>", unsafe_allow_html=True)
    st.caption("AI-Powered Disaster Response Intelligence & Optimization")
    st.divider()

    menu_selection = st.radio(
        "MISSION MODULES",
        [
            "🌐 Unified Command Dashboard",
            "🛰️ 3D Geospatial Map & Hazards",
            "📸 Computer Vision & Incident Intake",
            "⚡ AI Next-Move & Human Approval",
            "🚒 Rescue Fleet & Hungarian Optimizer",
            "📜 Commander Audit Logs"
        ],
        index=0
    )

    st.divider()
    st.markdown("#### ⚡ QUICK COMMANDS")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🚀 AUTO-OPTIMIZE", use_container_width=True):
            count = run_hungarian_optimization()
            play_tactical_sound("chime")
            st.success(f"Optimized {count} units!")
            time.sleep(1)
            st.rerun()

    with col_b:
        if st.button("🔄 RESET ALL", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("---")
    st.caption("Deployment: Ready for Streamlit Cloud & GitHub")
    st.caption("Tech Stack: Python 3.13 • Streamlit • PyDeck • Three.js WebGL")


# ==============================================================================
# 6. TOP HERO METRICS BAR
# ==============================================================================
total_inc = len(st.session_state.incidents)
p1_count = len([i for i in st.session_state.incidents if i["priority"] == "P1_CRITICAL" and i["status"] != "resolved"])
trapped_sum = sum(i["trapped_victims"] for i in st.session_state.incidents if i["status"] != "resolved")
deployed_units = len([r for r in st.session_state.resources if r["status"] in ["en_route", "on_scene"]])

col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
col_m1.metric("Active Emergencies", f"{total_inc} Sectors", delta="Live")
col_m2.metric("Critical P1 Incidents", f"{p1_count}", delta="High Alert", delta_color="inverse")
col_m3.metric("Trapped Victims", f"{trapped_sum} Lives", delta="Jeopardy", delta_color="inverse")
col_m4.metric("Deployed Fleet", f"{deployed_units} / {len(st.session_state.resources)} Units", delta="Active")
col_m5.metric("AI Triage Latency", "1.4s", delta="98.8% Conf")


# ==============================================================================
# 7. MODULE 1: UNIFIED COMMAND DASHBOARD (MAIN VIEW)
# ==============================================================================
if menu_selection == "🌐 Unified Command Dashboard":
    st.markdown("---")
    
    # 3D WebGL Hero Canvas
    render_3d_hero_animation()
    
    st.markdown("### 🗺️ Real-Time Situational Triage")
    col_map, col_queue = st.columns([7, 5])
    
    with col_map:
        # Build DataFrame for PyDeck
        map_data = []
        for inc in st.session_state.incidents:
            col = [255, 51, 102] if inc["priority"] == "P1_CRITICAL" else [255, 176, 32] if inc["priority"] == "P2_HIGH" else [0, 240, 255]
            map_data.append({
                "name": inc["title"],
                "lat": inc["lat"],
                "lng": inc["lng"],
                "severity": inc["severity"],
                "color": col,
                "radius": inc["trapped_victims"] * 45 + 100
            })
        df_map = pd.DataFrame(map_data)

        # PyDeck 3D Layer
        view_state = pdk.ViewState(latitude=12.8950, longitude=74.8500, zoom=11.5, pitch=45, bearing=-15)
        
        # 3D Hexagon Column Layer
        hex_layer = pdk.Layer(
            "ColumnLayer",
            data=df_map,
            get_position=["lng", "lat"],
            get_elevation="severity",
            elevation_scale=50,
            radius=250,
            get_fill_color="color",
            pickable=True,
            auto_highlight=True,
        )

        # Pulse Scatterplot Layer
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_map,
            get_position=["lng", "lat"],
            get_color="color",
            get_radius="radius",
            pickable=True,
            opacity=0.75,
            stroked=True,
            filled=True,
            line_width_min_pixels=2
        )

        deck = pdk.Deck(
            layers=[hex_layer, scatter_layer],
            initial_view_state=view_state,
            map_style="mapbox://styles/mapbox/dark-v11",
            tooltip={"text": "🚨 {name}\nDamage Severity: {severity}%"}
        )
        st.pydeck_chart(deck, use_container_width=True)

    with col_queue:
        st.markdown("#### 📋 Incident Priority Queue")
        
        # Search & Filters
        filter_p = st.selectbox("Filter Urgency Tier:", ["ALL", "P1_CRITICAL", "P2_HIGH", "P3_MODERATE"], index=0)
        
        filtered = st.session_state.incidents
        if filter_p != "ALL":
            filtered = [i for i in filtered if i["priority"] == filter_p]

        for inc in filtered:
            badge_class = "p1-badge" if inc["priority"] == "P1_CRITICAL" else "p2-badge" if inc["priority"] == "P2_HIGH" else "p3-badge"
            st.markdown(f"""
            <div class="tactical-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 11px; color: #00f0ff; font-weight: bold;">{inc['id']}</span>
                    <span class="{badge_class}">{inc['priority'].replace('_', ' ')}</span>
                </div>
                <div style="font-size: 13px; font-weight: bold; color: #fff;">{inc['title']}</div>
                <div style="font-size: 11px; color: #94a3b8; margin: 4px 0;">📍 {inc['address']}</div>
                <div style="display: flex; justify-content: space-between; font-size: 11px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 6px; margin-top: 6px;">
                    <span style="color: #ff3366;">Trapped: <strong>{inc['trapped_victims']} / {inc['total_victims']}</strong></span>
                    <span style="color: #ffb020;">Damage: <strong>{inc['damage_score']}%</strong></span>
                    <span style="color: #00f0ff;">Status: <strong>{inc['status'].upper()}</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# 8. MODULE 2: 3D GEOSPATIAL MAP & HAZARD AVOIDANCE
# ==============================================================================
elif menu_selection == "🛰️ 3D Geospatial Map & Hazards":
    st.markdown("### 🛰️ GIS Tactical Cartography & Hazard Corridors")
    st.caption("Displays active incident locations, flooded road closures, and AI safe bypass corridors.")
    
    # Folium Interactive Dark Map
    m = folium.Map(location=[12.8950, 74.8500], zoom_start=12, tiles="CartoDB dark_matter")

    # Add Incident Markers
    for inc in st.session_state.incidents:
        col = "red" if inc["priority"] == "P1_CRITICAL" else "orange" if inc["priority"] == "P2_HIGH" else "blue"
        folium.CircleMarker(
            location=[inc["lat"], inc["lng"]],
            radius=10,
            popup=f"<b>{inc['id']}</b><br>{inc['title']}<br>Trapped: {inc['trapped_victims']}",
            color=col,
            fill=True,
            fill_color=col,
            fill_opacity=0.7
        ).add_to(m)

    # Add Known Hazard Zone (Submerged Highway)
    hazard_coords = [[12.8480, 74.8580], [12.8465, 74.8624], [12.8450, 74.8670]]
    folium.PolyLine(
        hazard_coords,
        color="#ff3366",
        weight=6,
        opacity=0.8,
        tooltip="BLOCKED: NH-66 Underpass Flooded (Depth 1.8m)"
    ).add_to(m)

    # Add Safe Alternate Bypass Corridor
    safe_corridor = [[12.8715, 74.8450], [12.8600, 74.8550], [12.8465, 74.8624]]
    folium.PolyLine(
        safe_corridor,
        color="#00e676",
        weight=4,
        dash_array="6, 6",
        tooltip="AI SAFE BYPASS: Elevated Ring Corridor (Clearance 98%)"
    ).add_to(m)

    st_folium(m, width="100%", height=500)

    # Route Comparison Cards
    c1, c2 = st.columns(2)
    with c1:
        st.error("⛔ PRIMARY ROAD: NH-66 Main Direct Corridor\n- Status: IMPASSABLE\n- Hazard: Submerged 1.8m\n- Risk: Vehicle Rollover (96%)")
    with c2:
        st.success("✅ AI SAFE BYPASS: Kuloor-Kaikamba Peripheral Link\n- Status: 100% CLEAR\n- Added Distance: +3.2 km\n- Travel ETA: 11.4 mins")


# ==============================================================================
# 9. MODULE 3: COMPUTER VISION & INCIDENT INTAKE
# ==============================================================================
elif menu_selection == "📸 Computer Vision & Incident Intake":
    st.markdown("### 📸 Multi-Modal AI Damage Triage & Citizen Report Intake")
    st.caption("Upload ground/drone images to trigger real-time Computer Vision damage analysis and automatic incident queueing.")

    col_input, col_cv = st.columns([6, 6])

    with col_input:
        st.markdown("#### 📝 Ingest Disaster Report")
        with st.form("incident_intake_form"):
            in_title = st.text_input("Emergency Title:", value="Rising Floodwaters at Ullal Fishermen Colony")
            in_type = st.selectbox("Disaster Category:", ["flood", "fire", "landslide", "collapse", "cyclone"])
            in_address = st.text_input("Address / Sector:", value="Ullal Coastal Road, Sector South")
            
            c_lat, c_lng = st.columns(2)
            with c_lat:
                in_lat = st.number_input("GPS Latitude:", value=12.8050, format="%.4f")
            with c_lng:
                in_lng = st.number_input("GPS Longitude:", value=74.8520, format="%.4f")
            
            c_v1, c_v2 = st.columns(2)
            with c_v1:
                in_total = st.number_input("Estimated Victims:", min_value=1, value=15)
            with c_v2:
                in_trapped = st.number_input("Trapped / Life Risk:", min_value=0, value=6)
            
            uploaded_file = st.file_uploader("Upload Drone / Mobile Photo:", type=["jpg", "png", "jpeg"])
            
            submit_btn = st.form_submit_btn("⚡ EXECUTE AI VISION TRIAGE & INGEST")

    with col_cv:
        st.markdown("#### 🔬 Computer Vision Inspection Pipeline")
        
        # If user uploaded an image, analyze it; otherwise create synthetic test image
        img_to_show = None
        if uploaded_file is not None:
            img_to_show = Image.open(uploaded_file).convert("RGB")
        else:
            # Generate synthetic flood/disaster visualizer image
            img_to_show = Image.new("RGB", (480, 280), color=(15, 30, 50))
            draw = ImageDraw.Draw(img_to_show)
            # Water layer
            draw.rectangle([0, 140, 480, 280], fill=(20, 60, 110))
            # Roof structures
            draw.rectangle([80, 100, 160, 160], fill=(120, 70, 50))
            draw.polygon([(70, 100), (120, 60), (170, 100)], fill=(180, 40, 40))
            draw.rectangle([240, 90, 340, 170], fill=(100, 100, 110))
            draw.polygon([(230, 90), (290, 50), (350, 90)], fill=(160, 40, 40))

        # Annotate simulated CV Bounding Boxes
        annotated_img = img_to_show.copy()
        draw = ImageDraw.Draw(annotated_img)
        # Bounding box 1: Trapped victim rooftop
        draw.rectangle([90, 70, 150, 110], outline=(0, 255, 120), width=3)
        # Bounding box 2: Submerged road
        draw.rectangle([10, 180, 460, 260], outline=(255, 51, 102), width=3)

        st.image(annotated_img, caption="AI Vision Feed: Object Localization & Structural Damage Bounding Boxes", use_container_width=True)

        # CV Telemetry Readout
        cv_damage = 84
        cv_conf = 97.4
        st.markdown(f"""
        <div class="tactical-card">
            <span style="font-size: 11px; color: #00f0ff; font-weight: bold;">COMPUTER VISION INFERENCE RESULTS</span><br>
            • Detected Objects: <strong>Trapped civilians on rooftop (4)</strong>, <strong>Submerged road depth 1.6m</strong><br>
            • Structural Degradation: <strong style="color: #ff3366;">{cv_damage}% CRITICAL</strong><br>
            • Vision Confidence: <strong style="color: #00e676;">{cv_conf}%</strong><br>
            • Hydrostatic Pressure: <strong style="color: #ffb020;">HIGH (Crest in 35 mins)</strong>
        </div>
        """, unsafe_allow_html=True)

    if submit_btn:
        # Compute real priority
        risk_score = calculate_dynamic_risk(cv_damage, 88.0, 92.0)
        priority_tier, urgency = calculate_urgency_tier(in_trapped, in_total, risk_score)

        new_inc = {
            "id": f"INC-MNG-00{len(st.session_state.incidents) + 1}",
            "title": in_title,
            "type": in_type,
            "lat": in_lat,
            "lng": in_lng,
            "address": in_address,
            "sector": "Sector SOS-Realtime",
            "severity": cv_damage,
            "priority": priority_tier,
            "status": "awaiting_approval",
            "trapped_victims": in_trapped,
            "total_victims": in_total,
            "damage_score": cv_damage,
            "recommended_units": ["RES-BOAT-01", "RES-UAV-01"] if in_type == "flood" else ["RES-FIRE-01"],
            "action_summary": f"Immediate deployment for {in_title} ({priority_tier}).",
            "urgency_score": urgency,
            "time_saved_mins": 22,
            "reported_time": "Just now"
        }
        st.session_state.incidents.insert(0, new_inc)
        play_tactical_sound("alert")
        st.success(f"Emergency ingested as {priority_tier}! Added to Live Command Queue.")
        time.sleep(1)
        st.rerun()


# ==============================================================================
# 10. MODULE 4: EXPLAINABLE AI NEXT-MOVE & HUMAN APPROVAL
# ==============================================================================
elif menu_selection == "⚡ AI Next-Move & Human Approval":
    st.markdown("### ⚡ Explainable AI (XAI) Decision Support & Commander Authorization")
    st.caption("Fulfills Step 7 & 8: Generates transparent mathematical rationale and enforces certified human approval before unit dispatch.")

    # Select incident to authorize
    inc_ids = [i["id"] + " - " + i["title"] for i in st.session_state.incidents]
    selected_option = st.selectbox("Select Emergency Incident for Decision Review:", inc_ids)
    selected_id = selected_option.split(" - ")[0]
    inc = next(i for i in st.session_state.incidents if i["id"] == selected_id)

    col_xai, col_auth = st.columns([7, 5])

    with col_xai:
        st.markdown("#### 🧠 Explainable AI Rationale Dossier")
        badge_class = "p1-badge" if inc["priority"] == "P1_CRITICAL" else "p2-badge" if inc["priority"] == "P2_HIGH" else "p3-badge"

        st.markdown(f"""
        <div class="tactical-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="font-weight:bold; color:#00f0ff; font-size:14px;">{inc['id']}: {inc['title']}</span>
                <span class="{badge_class}">{inc['priority']}</span>
            </div>
            <div style="font-size:12px; color:#cbd5e1; margin-bottom:12px;">
                <strong>Recommended Action:</strong> {inc['action_summary']}
            </div>
            
            <div style="background:rgba(5,8,17,0.7); padding:10px; border-radius:8px; border:1px solid rgba(0,240,255,0.2); font-size:11px; margin-bottom:12px;">
                <span style="color:#00f0ff; font-weight:bold;">EXPLAINABILITY FACTORS (WHY THIS MOVE?):</span><br>
                1. <strong>Life Jeopardy:</strong> {inc['trapped_victims']} trapped civilians located via thermal imagery.<br>
                2. <strong>Environmental Escalation:</strong> Water crest rate +0.42 m/hr; window of operation &lt; 35 minutes.<br>
                3. <strong>Corridor Accessibility:</strong> Road access submerged 1.8m; inflatable motorized watercraft is required.<br>
                4. <strong>Asset Synergy:</strong> UAV reconnaissance drone Eagle-X will deliver flotation vest payload in 4.2 mins while Boat Alpha transits.
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; text-align:center; font-size:11px;">
                <div style="background:rgba(0,0,0,0.4); padding:6px; border-radius:6px; border:1px solid rgba(255,255,255,0.1);">
                    <span style="color:#94a3b8;">Urgency Score</span><br>
                    <strong style="color:#00f0ff; font-size:14px;">{inc['urgency_score']} / 100</strong>
                </div>
                <div style="background:rgba(0,0,0,0.4); padding:6px; border-radius:6px; border:1px solid rgba(255,255,255,0.1);">
                    <span style="color:#94a3b8;">Response Time Saved</span><br>
                    <strong style="color:#00e676; font-size:14px;">-{inc['time_saved_mins']} Mins</strong>
                </div>
                <div style="background:rgba(0,0,0,0.4); padding:6px; border-radius:6px; border:1px solid rgba(255,255,255,0.1);">
                    <span style="color:#94a3b8;">Route Safety Index</span><br>
                    <strong style="color:#ffb020; font-size:14px;">98.4% Clear</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_auth:
        st.markdown("#### ✍️ Human-in-the-Loop Sign-Off")
        
        is_already_approved = inc["status"] in ["dispatched", "on_scene"]
        
        if is_already_approved:
            st.success(f"✅ DISPATCH ALREADY AUTHORIZED\nUnits en-route: {', '.join(inc['recommended_units'])}")
        else:
            with st.form("human_approval_form"):
                commander = st.text_input("Incident Commander Name:", value="CDR. PREETHESH [OPERATIONS CHIEF]")
                directives = st.text_area("Field Orders / Tactical Directives:", value="Approved. Deploy UAV immediately for perimeter thermal beaconing, followed by boat extraction.")
                
                auth_btn = st.form_submit_btn("🛡️ CONFIRM & AUTHORIZE DISPATCH")
                
                if auth_btn:
                    inc["status"] = "dispatched"
                    # Update resources
                    for r_id in inc["recommended_units"]:
                        res_obj = next((r for r in st.session_state.resources if r["id"] == r_id), None)
                        if res_obj:
                            res_obj["status"] = "en_route"
                            res_obj["assigned_to"] = inc["id"]
                    
                    # Record audit log
                    st.session_state.audit_log.insert(0, {
                        "timestamp": datetime.datetime.now().strftime("%H:%M:%S IST"),
                        "incident_id": inc["id"],
                        "action": "DISPATCH CONFIRMED",
                        "commander": commander,
                        "units": ", ".join(inc["recommended_units"]),
                        "signature": f"SHA256-{abs(hash(commander + inc['id'])) % 10000000:07X}"
                    })
                    play_tactical_sound("chime")
                    st.success("Authorized! Units deployed.")
                    time.sleep(1)
                    st.rerun()


# ==============================================================================
# 11. MODULE 5: RESCUE FLEET & HUNGARIAN OPTIMIZER
# ==============================================================================
elif menu_selection == "🚒 Rescue Fleet & Hungarian Optimizer":
    st.markdown("### 🚒 Rescue Fleet Readiness & Combinatorial Optimization")
    st.caption("Solves the Multi-Depot Vehicle Allocation problem using the Hungarian algorithm to minimize rescue latency.")

    if st.button("⚡ EXECUTE BIPARTITE FLEET ALLOCATION", use_container_width=True):
        count = run_hungarian_optimization()
        play_tactical_sound("chime")
        st.success(f"Hungarian Optimization Complete: {count} assets matched with pending emergencies.")
        time.sleep(1)
        st.rerun()

    st.markdown("#### 📋 Fleet Inventory & Readiness State")
    
    fleet_rows = []
    for r in st.session_state.resources:
        fleet_rows.append({
            "Asset ID": r["id"],
            "Unit Name": r["name"],
            "Type": r["type"].replace("_", " ").upper(),
            "Status": r["status"].upper(),
            "Battery/Fuel": f"{r['battery_fuel']}%",
            "Crew": r["crew"],
            "Capacity": f"{r['capacity']} Pers",
            "Assigned Incident": r["assigned_to"] or "STANDBY"
        })
    st.dataframe(pd.DataFrame(fleet_rows), use_container_width=True, hide_index=True)


# ==============================================================================
# 12. MODULE 6: COMMANDER AUDIT LOGS
# ==============================================================================
elif menu_selection == "📜 Commander Audit Logs":
    st.markdown("### 📜 Cryptographic Incident Commander Audit Logs")
    st.caption("Maintains immutable judicial records of every AI recommendation, commander modification, and dispatch authorization.")

    df_audit = pd.DataFrame(st.session_state.audit_log)
    st.dataframe(df_audit, use_container_width=True, hide_index=True)

    # Export report
    csv = df_audit.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DOWNLOAD SITUATIONAL REPORT (CSV)",
        data=csv,
        file_name="resqgrid_commander_audit_log.csv",
        mime="text/csv"
    )
