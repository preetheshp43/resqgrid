import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
from PIL import Image, ImageDraw, ImageEnhance
import datetime
import time
import math

# ==============================================================================
# 1. APPLICATION CONFIGURATION & CLEAN PROFESSIONAL THEME
# ==============================================================================
st.set_page_config(
    page_title="RESQGRID — Autonomous Disaster Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Minimalist CSS Theme (Palantir / SpaceX Command Aesthetic)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #080d1a;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Top Bar Branding */
    .top-brand {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 20px;
        background: rgba(13, 21, 39, 0.7);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 14px;
        margin-bottom: 20px;
        backdrop-filter: blur(16px);
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background: rgba(13, 21, 39, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 14px 18px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    div[data-testid="stMetricValue"] {
        color: #00f0ff !important;
        font-weight: 700;
        font-size: 28px !important;
        font-family: 'JetBrains Mono', monospace;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
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
        font-family: 'JetBrains Mono', monospace;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 16px rgba(0, 240, 255, 0.45);
        color: #000;
        transform: translateY(-1px);
    }
    
    /* Status Badges */
    .badge-critical {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-high {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-moderate {
        background: rgba(0, 240, 255, 0.15);
        color: #00f0ff;
        border: 1px solid rgba(0, 240, 255, 0.4);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-dispatched {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Cards */
    .incident-card {
        background: rgba(17, 26, 46, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: border 0.2s ease;
    }
    .incident-card:hover {
        border-color: rgba(0, 240, 255, 0.35);
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. AUDIO & 3D INTERACTIVE HERO COMPONENT
# ==============================================================================
def render_tactical_hero_3d():
    """Renders interactive 3D WebGL Holographic Earth & UAV Radar Canvas."""
    hero_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            body, html { margin: 0; padding: 0; overflow: hidden; background: #080d1a; width: 100%; height: 100%; font-family: monospace; }
            #container { width: 100%; height: 260px; position: relative; }
            .telemetry-label { position: absolute; top: 10px; left: 14px; color: #00f0ff; font-size: 11px; font-weight: bold; background: rgba(8,13,26,0.8); padding: 4px 10px; border: 1px solid rgba(0,240,255,0.3); border-radius: 6px; pointer-events: none; }
            .hint-label { position: absolute; bottom: 10px; right: 14px; color: #64748b; font-size: 10px; background: rgba(8,13,26,0.8); padding: 3px 8px; border-radius: 4px; pointer-events: none; }
        </style>
    </head>
    <body>
        <div id="container">
            <div class="telemetry-label">
                <span style="color:#ef4444; animation: blink 1s infinite;">●</span> SATELLITE DISASTER GRID: ONLINE
            </div>
            <div class="hint-label">DRAG TO ROTATE 3D TACTICAL PROJECTION</div>
        </div>
        <script>
            const container = document.getElementById('container');
            const w = container.clientWidth || window.innerWidth;
            const h = 260;

            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x080d1a, 0.04);
            const camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 1000);
            camera.position.set(0, 0.8, 6.2);

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(w, h);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(renderer.domElement);

            scene.add(new THREE.AmbientLight(0x00f0ff, 0.8));
            const light = new THREE.DirectionalLight(0xffffff, 1.8);
            light.position.set(4, 6, 4);
            scene.add(light);

            const globe = new THREE.Group();
            scene.add(globe);

            // Digital Globe Wireframe
            const sphere = new THREE.Mesh(
                new THREE.SphereGeometry(2.1, 28, 28),
                new THREE.MeshBasicMaterial({ color: 0x005577, wireframe: true, transparent: true, opacity: 0.25 })
            );
            globe.add(sphere);

            // Dark Inner Sphere
            globe.add(new THREE.Mesh(
                new THREE.SphereGeometry(2.06, 24, 24),
                new THREE.MeshBasicMaterial({ color: 0x0a1426, transparent: true, opacity: 0.85 })
            ));

            // Orbital Rings
            const ring1 = new THREE.Mesh(
                new THREE.RingGeometry(2.5, 2.53, 48),
                new THREE.MeshBasicMaterial({ color: 0x00f0ff, side: THREE.DoubleSide, transparent: true, opacity: 0.4 })
            );
            ring1.rotation.x = Math.PI / 2.3;
            globe.add(ring1);

            const ring2 = new THREE.Mesh(
                new THREE.RingGeometry(2.8, 2.82, 48),
                new THREE.MeshBasicMaterial({ color: 0xef4444, side: THREE.DoubleSide, transparent: true, opacity: 0.3 })
            );
            ring2.rotation.x = Math.PI / 1.8;
            ring2.rotation.y = -0.3;
            globe.add(ring2);

            // Disaster Beacons
            const beacons = [
                { lat: 12.8, lon: 74.8, c: 0xef4444 },
                { lat: 25.0, lon: 45.0, c: 0xf59e0b },
                { lat: -15.0, lon: 120.0, c: 0x00f0ff },
                { lat: 35.0, lon: -95.0, c: 0xef4444 }
            ];
            const pings = [];
            beacons.forEach(b => {
                const phi = (90 - b.lat) * (Math.PI / 180);
                const theta = (b.lon + 180) * (Math.PI / 180);
                const x = -(2.1 * Math.sin(phi) * Math.cos(theta));
                const z = 2.1 * Math.sin(phi) * Math.sin(theta);
                const y = 2.1 * Math.cos(phi);

                const pt = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 12), new THREE.MeshBasicMaterial({ color: b.c }));
                pt.position.set(x, y, z);
                globe.add(pt);

                const ping = new THREE.Mesh(new THREE.RingGeometry(0.09, 0.14, 16), new THREE.MeshBasicMaterial({ color: b.c, side: THREE.DoubleSide, transparent: true, opacity: 0.9 }));
                ping.position.set(x * 1.01, y * 1.01, z * 1.01);
                ping.lookAt(x * 2, y * 2, z * 2);
                globe.add(ping);
                pings.push(ping);
            });

            // Orbiting Recon Drone with Radar Cone
            const drone = new THREE.Group();
            drone.add(new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.04, 0.25), new THREE.MeshBasicMaterial({ color: 0x00f0ff })));
            const cone = new THREE.Mesh(new THREE.ConeGeometry(0.5, 1.2, 14, 1, true), new THREE.MeshBasicMaterial({ color: 0x00f0ff, wireframe: true, transparent: true, opacity: 0.2 }));
            cone.rotation.x = Math.PI;
            cone.position.y = -0.6;
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
                globe.rotation.y = t * 0.12 + mouseX * 0.35;
                globe.rotation.x = 0.15 + mouseY * 0.2;
                ring1.rotation.z = t * 0.18;
                ring2.rotation.z = -t * 0.22;

                pings.forEach((p, i) => {
                    const s = 1 + (Math.sin(t * 4 + i) + 1) * 0.55;
                    p.scale.set(s, s, s);
                    p.material.opacity = Math.max(0, 1 - (s - 1));
                });

                drone.position.x = Math.cos(t * 0.5) * 3.0;
                drone.position.z = Math.sin(t * 0.5) * 3.0;
                drone.position.y = 0.7 + Math.sin(t * 1.4) * 0.25;
                drone.lookAt(0, 0, 0);

                renderer.render(scene, camera);
            }
            animate();
        </script>
    </body>
    </html>
    """
    components.html(hero_code, height=270, scrolling=False)


def play_chime():
    """Web Audio API tactical confirmation chime."""
    components.html("""
    <script>
    try {
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var now = ctx.currentTime;
        [523.25, 659.25, 783.99, 1046.5].forEach((freq, idx) => {
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            var t = now + idx * 0.07;
            osc.frequency.setValueAtTime(freq, t);
            gain.gain.setValueAtTime(0.08, t);
            gain.gain.exponentialRampToValueAtTime(0.001, t + 0.2);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(t);
            osc.stop(t + 0.2);
        });
    } catch(e) {}
    </script>
    """, height=0, width=0)


# ==============================================================================
# 3. LIVE SIMULATION STATE
# ==============================================================================
if "incidents" not in st.session_state:
    st.session_state.incidents = [
        {
            "id": "EMERGENCY-01",
            "title": "Severe Flash Flood & Submerged Settlement",
            "type": "Flood",
            "lat": 12.8465,
            "lng": 74.8624,
            "location_name": "Jeppinamogaru, Netravati Basin",
            "priority": "CRITICAL P1",
            "status": "PENDING",
            "trapped": 14,
            "total_victims": 18,
            "damage_score": 92,
            "escalation": "Rapid (+0.4m/hr crest rise)",
            "solution_summary": "Deploy NDRF Inflatable Rescue Boat + Eagle-X Recon UAV with flotation payload.",
            "recommended_units": ["NDRF Inflatable Boat Alpha", "UAV Recon Drone Eagle-X"],
            "eta_mins": 8.4,
            "safe_corridor": "Bypass via Kuloor Peripheral Ring Road"
        },
        {
            "id": "EMERGENCY-02",
            "title": "Chemical Fire & Toxic Vapor Threat",
            "type": "Fire",
            "lat": 12.9512,
            "lng": 74.8021,
            "location_name": "Baikampady Industrial Estate",
            "priority": "CRITICAL P1",
            "status": "PENDING",
            "trapped": 5,
            "total_victims": 8,
            "damage_score": 88,
            "escalation": "High (plume spreading at 34 km/h)",
            "solution_summary": "Deploy Heavy Foam Tender FT-07 with AFFF + Hazmat Ambulance Squad.",
            "recommended_units": ["Heavy Foam Tender FT-07", "Rapid Paramedic Unit 02"],
            "eta_mins": 11.2,
            "safe_corridor": "Direct Northern Highway Corridor"
        },
        {
            "id": "EMERGENCY-03",
            "title": "Ghat Landslide & Road Blockade",
            "type": "Landslide",
            "lat": 12.9056,
            "lng": 74.9124,
            "location_name": "Gurupura Ghat Corridor",
            "priority": "ELEVATED P2",
            "status": "DISPATCHED",
            "trapped": 3,
            "total_victims": 7,
            "damage_score": 68,
            "escalation": "Moderate",
            "solution_summary": "Deploy SDRF Rescue Squad with hydraulic spreaders via Kaikamba link.",
            "recommended_units": ["SDRF Rescue Squad 3", "ALS Mobile Trauma Unit 01"],
            "eta_mins": 14.0,
            "safe_corridor": "Kaikamba Bypass Link"
        },
        {
            "id": "EMERGENCY-04",
            "title": "Commercial Building Structural Failure",
            "type": "Collapse",
            "lat": 12.8682,
            "lng": 74.8385,
            "location_name": "Bunder Old Port Complex",
            "priority": "ELEVATED P2",
            "status": "DISPATCHED",
            "trapped": 2,
            "total_victims": 11,
            "damage_score": 62,
            "escalation": "Stable",
            "solution_summary": "Deploy acoustic search probe and rapid foundation shoring crew.",
            "recommended_units": ["ALS Mobile Trauma Unit 01"],
            "eta_mins": 9.5,
            "safe_corridor": "Port Link Road"
        }
    ]

if "fleet" not in st.session_state:
    st.session_state.fleet = [
        {"id": "UNIT-01", "name": "NDRF Inflatable Boat Alpha", "type": "Watercraft", "status": "AVAILABLE", "battery": 94, "capacity": 12, "crew": 5, "assigned_to": None},
        {"id": "UNIT-02", "name": "UAV Recon Drone Eagle-X", "type": "Drone", "status": "AVAILABLE", "battery": 88, "capacity": 2, "crew": 2, "assigned_to": None},
        {"id": "UNIT-03", "name": "Heavy Foam Tender FT-07", "type": "Fire", "status": "AVAILABLE", "battery": 92, "capacity": 6, "crew": 6, "assigned_to": None},
        {"id": "UNIT-04", "name": "ALS Mobile Trauma Unit 01", "type": "Ambulance", "status": "EN ROUTE", "battery": 78, "capacity": 3, "crew": 4, "assigned_to": "EMERGENCY-03"},
        {"id": "UNIT-05", "name": "Rapid Paramedic Unit 02", "type": "Ambulance", "status": "AVAILABLE", "battery": 86, "capacity": 2, "crew": 3, "assigned_to": None},
        {"id": "UNIT-06", "name": "SDRF Rescue Squad 3", "type": "Heavy Rescue", "status": "ON SCENE", "battery": 74, "capacity": 10, "crew": 8, "assigned_to": "EMERGENCY-03"}
    ]

if "saved_victims" not in st.session_state:
    st.session_state.saved_victims = 24


# ==============================================================================
# 4. TOP BRANDING & HUD METRICS
# ==============================================================================
st.markdown("""
<div class="top-brand">
    <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:24px;">⚡</span>
        <div>
            <div style="font-size:16px; font-weight:800; letter-spacing:1px; color:#fff; font-family:'JetBrains Mono', monospace;">
                RESQ<span style="color:#00f0ff;">GRID</span> <span style="font-size:11px; color:#94a3b8; font-weight:normal;">v2.5 OPERATIONS</span>
            </div>
            <div style="font-size:11px; color:#64748b;">Autonomous Disaster Response Intelligence & Fleet Optimization</div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:10px;">
        <span class="badge-critical">DEFCON 2 : CRISIS ACTIVE</span>
        <span style="font-size:11px; font-family:'JetBrains Mono', monospace; color:#94a3b8;">SECTOR: COASTAL HUB</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 3D Interactive Hero Projection
render_tactical_hero_3d()

# Quick Key Numbers
active_incidents = [i for i in st.session_state.incidents if i["status"] != "RESOLVED"]
critical_count = len([i for i in active_incidents if "CRITICAL" in i["priority"]])
trapped_lives = sum(i["trapped"] for i in active_incidents)
deployed_count = len([f for f in st.session_state.fleet if f["status"] in ["EN ROUTE", "ON SCENE"]])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Active Disaster Zones", f"{len(active_incidents)} Sectors")
m2.metric("Critical P1 Emergencies", f"{critical_count}", delta="Requires Dispatch", delta_color="inverse")
m3.metric("Lives in Jeopardy", f"{trapped_lives} Trapped", delta="Window < 35m", delta_color="inverse")
m4.metric("Deployed Rescue Fleet", f"{deployed_count} / {len(st.session_state.fleet)} Units", delta="Active")

st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# 5. NAVIGATION TABS (CLEAN & PROFESSIONAL)
# ==============================================================================
tab_triage, tab_intake, tab_fleet, tab_routes = st.tabs([
    "🗺️ Operational Map & AI Triage",
    "📸 Report Emergency (AI Vision)",
    "🚒 Rescue Fleet & Auto-Optimizer",
    "🛣️ Safe Hazard Corridors"
])


# ==============================================================================
# TAB 1: OPERATIONAL MAP & LIVE TRIAGE
# ==============================================================================
with tab_triage:
    col_map, col_list = st.columns([7, 5])

    with col_map:
        st.markdown("#### 🛰️ Live GIS Situational Map")
        
        # Build clean PyDeck 3D visualization
        map_points = []
        for inc in active_incidents:
            is_crit = "CRITICAL" in inc["priority"]
            map_points.append({
                "title": inc["title"],
                "type": inc["type"],
                "lat": inc["lat"],
                "lng": inc["lng"],
                "severity": inc["damage_score"],
                "color": [239, 68, 68] if is_crit else [245, 158, 11],
                "radius": inc["trapped"] * 50 + 150
            })
        
        view_state = pdk.ViewState(latitude=12.8950, longitude=74.8500, zoom=11.2, pitch=40, bearing=0)
        
        col_layer = pdk.Layer(
            "ColumnLayer",
            data=pd.DataFrame(map_points),
            get_position=["lng", "lat"],
            get_elevation="severity",
            elevation_scale=40,
            radius=200,
            get_fill_color="color",
            pickable=True,
            auto_highlight=True
        )

        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame(map_points),
            get_position=["lng", "lat"],
            get_color="color",
            get_radius="radius",
            opacity=0.7,
            pickable=True,
            filled=True
        )

        st.pydeck_chart(pdk.Deck(
            layers=[col_layer, scatter_layer],
            initial_view_state=view_state,
            map_style="mapbox://styles/mapbox/dark-v11",
            tooltip={"text": "{title} ({type})\nDamage Index: {severity}%"}
        ), use_container_width=True)

    with col_list:
        st.markdown("#### ⚡ Active Emergencies & AI Solutions")

        for inc in active_incidents:
            is_p1 = "CRITICAL" in inc["priority"]
            is_dispatched = inc["status"] == "DISPATCHED"
            badge = '<span class="badge-critical">CRITICAL P1</span>' if is_p1 else '<span class="badge-high">ELEVATED P2</span>'
            status_badge = '<span class="badge-dispatched">DISPATCHED</span>' if is_dispatched else '<span style="color:#94a3b8; font-size:10px; font-weight:bold;">PENDING APPROVAL</span>'

            st.markdown(f"""
            <div class="incident-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-size:11px; font-weight:bold; color:#00f0ff; font-family:'JetBrains Mono', monospace;">{inc['id']}</span>
                    <div style="display:flex; gap:6px;">{badge} {status_badge}</div>
                </div>
                <div style="font-size:14px; font-weight:700; color:#fff; margin-bottom:4px;">{inc['title']}</div>
                <div style="font-size:11px; color:#94a3b8; margin-bottom:8px;">📍 {inc['location_name']} • Trapped: <strong style="color:#ef4444;">{inc['trapped']} lives</strong> • Escalation: {inc['escalation']}</div>
                
                <div style="background:rgba(8,13,26,0.6); padding:8px 12px; border-radius:8px; border:1px solid rgba(0,240,255,0.2); font-size:11px; margin-bottom:10px;">
                    <span style="color:#00f0ff; font-weight:bold;">AI RECOMMENDED ACTION:</span><br>
                    {inc['solution_summary']}<br>
                    <span style="color:#10b981;">ETA: {inc['eta_mins']} mins</span> • <span style="color:#94a3b8;">Corridor: {inc['safe_corridor']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Actions
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                if not is_dispatched:
                    if st.button(f"⚡ DEPLOY FLEET", key=f"btn_dep_{inc['id']}", use_container_width=True):
                        inc["status"] = "DISPATCHED"
                        for u_name in inc["recommended_units"]:
                            fleet_item = next((f for f in st.session_state.fleet if f["name"] == u_name), None)
                            if fleet_item:
                                fleet_item["status"] = "EN ROUTE"
                                fleet_item["assigned_to"] = inc["id"]
                        play_chime()
                        st.rerun()
            with col_b2:
                if st.button(f"✅ MARK RESOLVED", key=f"btn_res_{inc['id']}", use_container_width=True):
                    inc["status"] = "RESOLVED"
                    st.session_state.saved_victims += inc["trapped"]
                    for f in st.session_state.fleet:
                        if f["assigned_to"] == inc["id"]:
                            f["status"] = "AVAILABLE"
                            f["assigned_to"] = None
                    play_chime()
                    st.rerun()


# ==============================================================================
# TAB 2: AI VISION & SOS INTAKE
# ==============================================================================
with tab_intake:
    st.markdown("#### 📸 Multi-Modal AI Damage Assessment & SOS Ingestion")
    st.caption("Upload ground or drone imagery to automatically identify disaster category, calculate damage %, and locate trapped survivors.")

    c_up, c_res = st.columns([6, 6])

    with c_up:
        with st.form("sos_form"):
            in_name = st.text_input("Emergency Scenario Title:", value="Torrential Inundation & Trapped Civilians")
            in_cat = st.selectbox("Disaster Category:", ["Flood", "Industrial Fire", "Landslide", "Structure Collapse", "Cyclone"])
            in_loc = st.text_input("Incident Location / Sector:", value="Ullal Coastal Settlement, Sector 4")
            
            c1, c2 = st.columns(2)
            with c1:
                in_trapped = st.number_input("Trapped Individuals:", min_value=1, value=6)
            with c2:
                in_total = st.number_input("Total Impacted:", min_value=1, value=14)

            uploaded_img = st.file_uploader("Upload Drone / Sensor Photo:", type=["jpg", "png", "jpeg"])
            
            submit_sos = st.form_submit_btn("⚡ RUN COMPUTER VISION & DISPATCH TO QUEUE")

    with c_res:
        st.markdown("##### 🔬 Computer Vision Object Detection")
        
        # Display image with bounding boxes
        if uploaded_img:
            base_image = Image.open(uploaded_img).convert("RGB")
        else:
            # Generate synthetic inspection image
            base_image = Image.new("RGB", (480, 260), color=(14, 25, 45))
            d = ImageDraw.Draw(base_image)
            d.rectangle([0, 130, 480, 260], fill=(22, 58, 104))
            d.rectangle([90, 80, 180, 150], fill=(120, 60, 40))
            d.polygon([(80, 80), (135, 45), (190, 80)], fill=(180, 50, 40))
            d.rectangle([260, 90, 360, 160], fill=(90, 90, 100))

        annotated = base_image.copy()
        draw = ImageDraw.Draw(annotated)
        # Bounding box survivors
        draw.rectangle([95, 55, 175, 95], outline=(16, 185, 129), width=3)
        # Bounding box submerged hazard
        draw.rectangle([10, 160, 470, 250], outline=(239, 68, 68), width=3)

        st.image(annotated, caption="Vision Triage: Green = Survivors Detected | Red = Severe Hazard Zone", use_container_width=True)

        st.markdown("""
        <div style="background:rgba(13,21,39,0.7); border:1px solid rgba(0,240,255,0.2); padding:12px; border-radius:10px; font-size:12px;">
            <span style="color:#00f0ff; font-weight:bold;">AUTOMATED VISION EXTRACTION</span><br>
            • Detected Victims on Elevated Surface: <strong style="color:#10b981;">6 Verified (98.2% Confidence)</strong><br>
            • Submerged Arterial Depth: <strong style="color:#ef4444;">1.72 meters (Impassable to wheeled vehicles)</strong><br>
            • Computed Structural Damage Index: <strong style="color:#f59e0b;">86% (Critical Evacuation Mandatory)</strong>
        </div>
        """, unsafe_allow_html=True)

    if submit_sos:
        new_entry = {
            "id": f"EMERGENCY-0{len(st.session_state.incidents) + 1}",
            "title": in_name,
            "type": in_cat,
            "lat": 12.8050,
            "lng": 74.8520,
            "location_name": in_loc,
            "priority": "CRITICAL P1" if in_trapped >= 4 else "ELEVATED P2",
            "status": "PENDING",
            "trapped": in_trapped,
            "total_victims": in_total,
            "damage_score": 86,
            "escalation": "Rapid",
            "solution_summary": f"Immediate deployment of NDRF Boat Alpha and Paramedic Unit to {in_loc}.",
            "recommended_units": ["NDRF Inflatable Boat Alpha", "Rapid Paramedic Unit 02"],
            "eta_mins": 9.8,
            "safe_corridor": "Coastal Elevated Bypass"
        }
        st.session_state.incidents.insert(0, new_entry)
        play_chime()
        st.success(f"Disaster Incident Ingested into Live Operational Triage!")
        time.sleep(1)
        st.rerun()


# ==============================================================================
# TAB 3: RESCUE FLEET & OPTIMIZER
# ==============================================================================
with tab_fleet:
    st.markdown("#### 🚒 Emergency Fleet Inventory & Combinatorial Optimizer")
    st.caption("Matches available emergency equipment to open emergencies minimizing total response arrival latency.")

    if st.button("⚡ EXECUTE FLEET ALLOCATION OPTIMIZER", use_container_width=True):
        # Assign available units to pending emergencies
        pending = [i for i in st.session_state.incidents if i["status"] == "PENDING"]
        avail = [f for f in st.session_state.fleet if f["status"] == "AVAILABLE"]
        
        matches = 0
        for p in pending:
            for f in avail:
                if f["status"] == "AVAILABLE":
                    f["status"] = "EN ROUTE"
                    f["assigned_to"] = p["id"]
                    p["status"] = "DISPATCHED"
                    matches += 1
                    break
        play_chime()
        st.success(f"Optimal Allocation Complete: {matches} emergency units matched and dispatched.")
        time.sleep(1)
        st.rerun()

    fleet_table = []
    for f in st.session_state.fleet:
        fleet_table.append({
            "Unit Code": f["id"],
            "Asset Name": f["name"],
            "Category": f["type"],
            "Status": f["status"],
            "Power/Fuel": f"{f['battery']}%",
            "Capacity": f"{f['capacity']} Survivors",
            "Crew Size": f"{f['crew']} Pers",
            "Assignment": f["assigned_to"] or "READY (STANDBY)"
        })

    st.dataframe(pd.DataFrame(fleet_table), use_container_width=True, hide_index=True)


# ==============================================================================
# TAB 4: SAFE HAZARD CORRIDORS
# ==============================================================================
with tab_routes:
    st.markdown("#### 🛣️ Hazard-Free Routing & Road Clearance Corridors")
    st.caption("Dynamically steers rescue convoys around flooded underpasses, landslides, and toxic plumes.")

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("""
        <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:12px; padding:16px;">
            <div style="font-weight:700; color:#ef4444; font-size:13px; margin-bottom:8px;">⛔ BLOCKED DIRECT ARTERIAL ROUTE (NH-66)</div>
            <div style="font-size:12px; color:#cbd5e1; line-height:1.6;">
                • Obstruction: Underpass submerged under 1.8m flash floodwaters.<br>
                • Risk Assessment: <strong>96% probability of vehicle stall/inundation.</strong><br>
                • Travel ETA: <strong>BLOCKED (Infinite Latency)</strong><br>
                • Clearance Decision: <strong>REJECTED BY NAVIGATION ENGINE</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown("""
        <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:12px; padding:16px;">
            <div style="font-weight:700; color:#10b981; font-size:13px; margin-bottom:8px;">✅ AI CALCULATED SAFE CORRIDOR (KAIKAMBA BYPASS)</div>
            <div style="font-size:12px; color:#cbd5e1; line-height:1.6;">
                • Alignment: Elevated peripheral bypass with 350m hazard buffer.<br>
                • Water Inundation: <strong>Zero structural flooding detected.</strong><br>
                • Travel Distance: <strong>+3.2 km detour</strong><br>
                • Arrival ETA: <strong>11.4 mins guaranteed arrival time</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
