import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import datetime
import time

# ==============================================================================
# 1. PAGE SETUP & OFFICIAL EMERGENCY MANAGEMENT SYSTEM THEME
# ==============================================================================
st.set_page_config(
    page_title="RESQGRID — Emergency Operations Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Authentic, Professional, Non-AI Institutional Theme (FEMA / NOAA / NASA Disaster Response)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Roboto+Mono:wght@400;500;700&display=swap');
    
    /* Clean, Matte Institutional Background */
    .stApp {
        background-color: #0b1120;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Agency Command Header Bar */
    .agency-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 20px;
        background: #111c35;
        border: 1px solid #1e2e4f;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    .agency-title {
        font-size: 19px;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .agency-badge {
        background: #ea580c;
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        font-family: 'Roboto Mono', monospace;
    }

    /* Authentic EOC Metrics */
    div[data-testid="stMetric"] {
        background: #111c35;
        border: 1px solid #1e2e4f;
        border-top: 3px solid #ea580c;
        padding: 14px 18px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    }
    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 700;
        font-size: 26px !important;
        font-family: 'Roboto Mono', monospace;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        font-weight: 600;
    }

    /* Real Incident Triage Cards (ICS-201 Compliant) */
    .incident-card {
        background: #111c35;
        border: 1px solid #1e2e4f;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    }
    .incident-critical {
        border-left: 4px solid #dc2626;
    }
    .incident-elevated {
        border-left: 4px solid #f59e0b;
    }

    /* Professional Status Badges */
    .status-badge-red {
        background: #450a0a;
        color: #f87171;
        border: 1px solid #dc2626;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 4px;
        font-family: 'Roboto Mono', monospace;
    }
    .status-badge-amber {
        background: #451a03;
        color: #fbbf24;
        border: 1px solid #d97706;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 4px;
        font-family: 'Roboto Mono', monospace;
    }
    .status-badge-green {
        background: #052e16;
        color: #4ade80;
        border: 1px solid #16a34a;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 4px;
        font-family: 'Roboto Mono', monospace;
    }

    /* Clean, Authentic ICS Module Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #0b1120;
        border-bottom: 2px solid #1e293b;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        background-color: #111c35;
        border: 1px solid #1e2e4f;
        border-radius: 6px 6px 0 0;
        color: #94a3b8;
        font-weight: 600;
        font-size: 12.5px;
        padding: 0 14px;
        transition: all 0.15s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        border-color: #ea580c !important;
        border-bottom: 2px solid #ea580c !important;
        color: #f8fafc !important;
    }

    /* Solid Action Buttons */
    .stButton>button {
        background: #ea580c;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border: 1px solid #c2410c;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 12px;
        letter-spacing: 0.3px;
        transition: all 0.15s ease;
    }
    .stButton>button:hover {
        background: #f97316;
        color: #ffffff;
        border-color: #ea580c;
        box-shadow: 0 2px 8px rgba(234, 88, 12, 0.3);
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. CINEMATIC INTRO: "RESQ" + "GRID" COLLISION & STORM CLOUD CRASH ANIMATION
# ==============================================================================
def render_cloud_crash_intro():
    """
    Dramatic cinematic collision animation:
    'RESQ' flies from the far left, 'GRID' flies from the far right,
    colliding in the center with a storm cloud clash, lightning flash,
    shockwave ripple, screen shake, and synthesized thunder impact audio.
    """
    intro_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Roboto+Mono:wght@700&display=swap');
            
            * { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                background: transparent;
                overflow: hidden;
                user-select: none;
            }

            #intro-stage {
                position: relative;
                width: 100%;
                height: 240px;
                background: radial-gradient(circle at center, #0f1a30 0%, #070c17 100%);
                border: 1px solid #1e2e4f;
                border-radius: 12px;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: inset 0 0 50px rgba(0,0,0,0.85), 0 8px 24px rgba(0,0,0,0.4);
            }

            /* Tactical Grid Lines in Background */
            .grid-bg {
                position: absolute;
                inset: 0;
                background-image: 
                    linear-gradient(rgba(30, 46, 79, 0.25) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(30, 46, 79, 0.25) 1px, transparent 1px);
                background-size: 28px 28px;
                pointer-events: none;
            }

            /* Volumetric Storm Clouds */
            .storm-cloud {
                position: absolute;
                border-radius: 50%;
                filter: blur(32px);
                pointer-events: none;
                mix-blend-mode: screen;
            }
            .cloud-l1 {
                width: 380px; height: 180px;
                background: radial-gradient(circle, #475569 0%, #1e293b 70%, transparent 100%);
                top: 25px; left: -140px;
                opacity: 0.5;
                animation: cloudClashLeft 2.4s ease-out forwards;
            }
            .cloud-l2 {
                width: 260px; height: 140px;
                background: radial-gradient(circle, #334155 0%, #0f172a 80%, transparent 100%);
                bottom: 10px; left: -80px;
                opacity: 0.6;
                animation: cloudClashLeft 2.4s ease-out 0.1s forwards;
            }
            .cloud-r1 {
                width: 400px; height: 190px;
                background: radial-gradient(circle, #64748b 0%, #334155 70%, transparent 100%);
                top: 15px; right: -160px;
                opacity: 0.5;
                animation: cloudClashRight 2.4s ease-out forwards;
            }
            .cloud-r2 {
                width: 280px; height: 150px;
                background: radial-gradient(circle, #475569 0%, #1e293b 80%, transparent 100%);
                bottom: 15px; right: -90px;
                opacity: 0.6;
                animation: cloudClashRight 2.4s ease-out 0.1s forwards;
            }

            @keyframes cloudClashLeft {
                0% { transform: translateX(-220px) scale(0.7); opacity: 0.1; }
                45% { transform: translateX(200px) scale(1.35); opacity: 0.8; }
                65% { transform: translateX(160px) scale(1.15); opacity: 0.45; }
                100% { transform: translateX(140px) scale(1.05); opacity: 0.3; }
            }
            @keyframes cloudClashRight {
                0% { transform: translateX(220px) scale(0.7); opacity: 0.1; }
                45% { transform: translateX(-200px) scale(1.4); opacity: 0.85; }
                65% { transform: translateX(-160px) scale(1.2); opacity: 0.45; }
                100% { transform: translateX(-140px) scale(1.05); opacity: 0.3; }
            }

            /* Lightning Bolt Flash Across Clouds */
            .lightning-flash {
                position: absolute;
                inset: 0;
                background: radial-gradient(circle at center, #ffffff 10%, #bae6fd 60%, transparent 100%);
                opacity: 0;
                pointer-events: none;
                animation: stormFlash 2.4s ease-out forwards;
            }
            @keyframes stormFlash {
                0%, 41% { opacity: 0; }
                42% { opacity: 0.95; }
                44% { opacity: 0.15; }
                46% { opacity: 0.85; }
                50% { opacity: 0.2; }
                54% { opacity: 0.6; }
                62% { opacity: 0; }
                100% { opacity: 0; }
            }

            /* Expanding Shockwave Ring */
            .shockwave {
                position: absolute;
                width: 16px; height: 16px;
                border-radius: 50%;
                border: 3px solid #f97316;
                opacity: 0;
                pointer-events: none;
                animation: blastWave 2.4s cubic-bezier(0.1, 0.8, 0.2, 1) forwards;
            }
            @keyframes blastWave {
                0%, 41% { width: 16px; height: 16px; opacity: 0; }
                42% { opacity: 1; border-color: #f97316; box-shadow: 0 0 30px #ea580c; }
                100% { width: 850px; height: 850px; opacity: 0; border-width: 1px; border-color: #38bdf8; }
            }

            /* Screen Shake on Collision Impact */
            .shake-wrapper {
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                animation: screenTremor 2.4s ease-out forwards;
            }
            @keyframes screenTremor {
                0%, 41% { transform: translate(0, 0); }
                42% { transform: translate(-8px, 5px) rotate(-0.5deg); }
                44% { transform: translate(7px, -6px) rotate(0.6deg); }
                46% { transform: translate(-6px, 4px) rotate(-0.4deg); }
                49% { transform: translate(4px, -3px) rotate(0.2deg); }
                53% { transform: translate(-2px, 2px); }
                58% { transform: translate(0, 0); }
                100% { transform: translate(0, 0); }
            }

            /* Colliding Letters Container */
            .logo-row {
                position: relative;
                z-index: 20;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 58px;
                font-weight: 900;
                letter-spacing: -1.5px;
                text-transform: uppercase;
            }

            /* Left Word: RESQ (Flies In from Far Left) */
            .resq-left {
                color: #f8fafc;
                display: inline-block;
                text-shadow: 0 4px 18px rgba(0, 0, 0, 0.7);
                animation: resqRushIn 1.0s cubic-bezier(0.18, 0.9, 0.28, 1) forwards;
            }
            @keyframes resqRushIn {
                0% {
                    transform: translateX(-480px) scale(0.65);
                    opacity: 0;
                    filter: blur(10px);
                }
                85% {
                    transform: translateX(12px) scale(1.08);
                    opacity: 1;
                    filter: blur(0);
                }
                100% {
                    transform: translateX(0) scale(1);
                    opacity: 1;
                }
            }

            /* Right Word: GRID (Flies In from Far Right) */
            .grid-right {
                color: #ea580c;
                display: inline-block;
                margin-left: 4px;
                text-shadow: 0 4px 20px rgba(234, 88, 12, 0.45);
                animation: gridRushIn 1.0s cubic-bezier(0.18, 0.9, 0.28, 1) forwards;
            }
            @keyframes gridRushIn {
                0% {
                    transform: translateX(480px) scale(0.65);
                    opacity: 0;
                    filter: blur(10px);
                }
                85% {
                    transform: translateX(-12px) scale(1.08);
                    opacity: 1;
                    filter: blur(0);
                }
                100% {
                    transform: translateX(0) scale(1);
                    opacity: 1;
                }
            }

            /* Institutional Subtitle Fade-In */
            .tagline {
                position: relative;
                z-index: 20;
                margin-top: 10px;
                font-family: 'Roboto Mono', monospace;
                font-size: 11.5px;
                color: #94a3b8;
                letter-spacing: 2.2px;
                font-weight: 600;
                text-transform: uppercase;
                opacity: 0;
                animation: tagReveal 2.4s ease-out 1.05s forwards;
            }
            @keyframes tagReveal {
                0% { opacity: 0; transform: translateY(12px); }
                100% { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body>
        <div id="intro-stage">
            <div class="grid-bg"></div>

            <!-- Clashing Storm Clouds -->
            <div class="storm-cloud cloud-l1"></div>
            <div class="storm-cloud cloud-l2"></div>
            <div class="storm-cloud cloud-r1"></div>
            <div class="storm-cloud cloud-r2"></div>

            <!-- Lightning Flash & Blast Shockwave -->
            <div class="lightning-flash"></div>
            <div class="shockwave"></div>

            <div class="shake-wrapper">
                <div class="logo-row">
                    <span class="resq-left">RESQ</span>
                    <span class="grid-right">GRID</span>
                </div>
                <div class="tagline">INCIDENT COMMAND SYSTEM • DISASTER RESPONSE INTELLIGENCE & RESOURCE MESH</div>
            </div>
        </div>

        <script>
            // Synchronized Collision Sound Impact (at 1000ms exact collision time)
            setTimeout(function() {
                try {
                    var AudioContext = window.AudioContext || window.webkitAudioContext;
                    if (!AudioContext) return;
                    var ctx = new AudioContext();
                    var now = ctx.currentTime;

                    // Deep Thunder Sub-Bass Boom
                    var osc = ctx.createOscillator();
                    var gain = ctx.createGain();
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(140, now);
                    osc.frequency.exponentialRampToValueAtTime(32, now + 0.65);
                    gain.gain.setValueAtTime(0.3, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.7);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now);
                    osc.stop(now + 0.7);

                    // High Impact Metal Clang
                    var clang = ctx.createOscillator();
                    var cGain = ctx.createGain();
                    clang.type = 'triangle';
                    clang.frequency.setValueAtTime(780, now);
                    clang.frequency.exponentialRampToValueAtTime(190, now + 0.35);
                    cGain.gain.setValueAtTime(0.22, now);
                    cGain.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
                    clang.connect(cGain);
                    cGain.connect(ctx.destination);
                    clang.start(now);
                    clang.stop(now + 0.38);
                } catch(e) {}
            }, 1000);
        </script>
    </body>
    </html>
    """
    components.html(intro_html, height=255, scrolling=False)


# ==============================================================================
# 3. SESSION STATE INITIALIZATION (DEFENSIVE VERSION 5.0)
# ==============================================================================
SESSION_VERSION = "5.0"
if st.session_state.get("session_version") != SESSION_VERSION:
    st.session_state.clear()
    st.session_state["session_version"] = SESSION_VERSION

if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

if "incidents" not in st.session_state:
    st.session_state.incidents = [
        {
            "id": "INC-2026-081",
            "title": "Netravati River Basin Flash Inundation",
            "type": "Flash Flood",
            "lat": 12.8465,
            "lng": 74.8624,
            "location_name": "Jeppinamogaru Residential Sector",
            "severity_level": "Level 1 Extreme",
            "status": "DISPATCH PENDING",
            "trapped": 16,
            "total_impacted": 42,
            "damage_score": 92,
            "water_crest_rate": "+0.45 m/hr",
            "action_directive": "Deploy NDRF Inflatable Gemini Alpha + Recon Drone Eagle-X.",
            "assigned_units": ["NDRF Gemini Boat Alpha", "UAV Recon Drone Eagle-X"],
            "eta_mins": 9.4
        },
        {
            "id": "INC-2026-082",
            "title": "Baikampady Petrochemical Flare & Vapor Cloud",
            "type": "Hazardous Material",
            "lat": 12.9512,
            "lng": 74.8021,
            "location_name": "Industrial Complex Gate 4",
            "severity_level": "Level 1 Extreme",
            "status": "DISPATCH PENDING",
            "trapped": 6,
            "total_impacted": 28,
            "damage_score": 88,
            "water_crest_rate": "Wind NNE 34 km/h",
            "action_directive": "Deploy Foam Tender FT-07 (AFFF Foam) + Hazmat Ambulance Squad.",
            "assigned_units": ["Heavy Foam Tender FT-07", "Advanced Life Support Unit 01"],
            "eta_mins": 12.1
        },
        {
            "id": "INC-2026-083",
            "title": "Gurupura Mountain Pass Rockfall & Highway Block",
            "type": "Landslide",
            "lat": 12.9056,
            "lng": 74.9124,
            "location_name": "NH-169 Ghat Corridor Km 34",
            "severity_level": "Level 2 Elevated",
            "status": "UNITS EN ROUTE",
            "trapped": 4,
            "total_impacted": 14,
            "damage_score": 72,
            "water_crest_rate": "Secondary Slump 68%",
            "action_directive": "Deploy SDRF Heavy Extrication Squad with hydraulic cutters.",
            "assigned_units": ["SDRF Rescue Squad 3"],
            "eta_mins": 14.5
        }
    ]

if "fleet" not in st.session_state:
    st.session_state.fleet = [
        {"id": "NDRF-BOAT-01", "name": "NDRF Gemini Boat Alpha", "category": "Watercraft", "status": "AVAILABLE", "crew": 6, "capacity": 12, "battery": 96, "station": "Panambur Marine Base"},
        {"id": "UAV-EAGLE-01", "name": "UAV Recon Drone Eagle-X", "category": "Aerial Recon", "status": "AVAILABLE", "crew": 2, "capacity": 2, "battery": 90, "station": "EOC Headquarters"},
        {"id": "FIRE-TENDER-07", "name": "Heavy Foam Tender FT-07", "category": "Fire & Hazmat", "status": "AVAILABLE", "crew": 6, "capacity": 4, "battery": 92, "station": "Kadri Fire Station"},
        {"id": "AMB-ALS-01", "name": "Advanced Life Support Unit 01", "category": "Medical Transport", "status": "AVAILABLE", "crew": 4, "capacity": 3, "battery": 86, "station": "District Trauma Center"},
        {"id": "SDRF-SQUAD-03", "name": "SDRF Rescue Squad 3", "category": "Heavy Extrication", "status": "EN ROUTE", "crew": 8, "capacity": 8, "battery": 78, "station": "Bantwal Taluk Center"}
    ]

if "rescued_count" not in st.session_state:
    st.session_state.rescued_count = 34


# ==============================================================================
# 4. INTRO ANIMATION SECTION
# ==============================================================================
if st.session_state.show_intro:
    render_cloud_crash_intro()
    # Action buttons below intro
    col_hide, col_replay, _ = st.columns([2.5, 2.5, 7])
    with col_hide:
        if st.button("✕ HIDE INTRO BANNER", use_container_width=True):
            st.session_state.show_intro = False
            st.rerun()
    with col_replay:
        if st.button("↻ REPLAY COLLISION", use_container_width=True):
            st.rerun()
else:
    # Small replay link if dismissed
    col_show, _ = st.columns([3, 9])
    with col_show:
        if st.button("▶ PLAY RESQ+GRID COLLISION INTRO", use_container_width=True):
            st.session_state.show_intro = True
            st.rerun()


# ==============================================================================
# 5. PROFESSIONAL EOC HEADER BAR
# ==============================================================================
st.markdown("""
<div class="agency-header">
    <div class="agency-title">
        <span style="color:#ea580c; font-size:22px;">🛡️</span>
        <div>
            <div style="font-size:18px; font-weight:800; letter-spacing:0.3px; color:#f8fafc;">
                RESQGRID <span style="font-weight:400; color:#94a3b8; font-size:14px;">| Incident Command System (ICS)</span>
            </div>
            <div style="font-size:11px; color:#64748b; font-weight:500;">Disaster Response Intelligence, Resource Optimization & Field Navigation</div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
        <span class="agency-badge">STATUS: LEVEL 1 ACTIVE EMERGENCY</span>
        <span style="font-size:12px; color:#94a3b8; font-family:'Roboto Mono', monospace;">EOC SECTOR: COASTAL DISTRICT</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 6. CORE OPERATIONAL METRICS (CLEAN & NON-AI)
# ==============================================================================
active_inc = [i for i in st.session_state.incidents if i.get("status") != "RESOLVED"]
trapped_sum = sum(i.get("trapped", 2) for i in active_inc)
deployed_units = len([f for f in st.session_state.fleet if f.get("status") in ["EN ROUTE", "ON SCENE"]])

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Active Incident Sectors", f"{len(active_inc)} Sectors")
m2.metric("Reported Trapped Persons", f"{trapped_sum} Lives", delta="High Urgency", delta_color="inverse")
m3.metric("Assigned Fleet Assets", f"{deployed_units} / {len(st.session_state.fleet)} Units", delta="Fielded")
m4.metric("Confirmed Extractions", f"{st.session_state.rescued_count} Persons", delta="+4 Completed")
m5.metric("System Operational Status", "NORMAL (0.78s)", delta="Online")

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# 7. INSTITUTIONAL MODULE TABS
# ==============================================================================
tab_map, tab_dispatch, tab_flir, tab_sim, tab_fleet = st.tabs([
    "🗺️ Operational GIS Map & Triage",
    "📋 Incident Action Plan (IAP)",
    "🛸 Aerial Reconnaissance Feed",
    "🌊 Hydrological Inundation Model",
    "🚒 Emergency Resource Inventory"
])


# ==============================================================================
# TAB 1: OPERATIONAL GIS MAP & LIVE TRIAGE
# ==============================================================================
with tab_map:
    col_map_view, col_triage_list = st.columns([7, 5])

    with col_map_view:
        st.markdown("##### 🗺️ Tactical Geographic Information System")
        
        # Dual-Layer High-Res Satellite GIS Map
        m = folium.Map(location=[12.8950, 74.8500], zoom_start=12, tiles=None)
        
        # Clean Professional Base Layers
        folium.TileLayer('CartoDB dark_matter', name='Tactical Dark Basemap').add_to(m)
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri World Imagery',
            name='Satellite Aerial Photography',
            overlay=False
        ).add_to(m)

        # Plot Incidents
        for inc in active_inc:
            lat = inc.get("lat", 12.85)
            lng = inc.get("lng", 74.85)
            title = inc.get("title", "Emergency Incident")
            trapped = inc.get("trapped", 2)
            is_crit = "Extreme" in inc.get("severity_level", "") or "P1" in inc.get("severity_level", "")
            color = "#dc2626" if is_crit else "#ea580c"

            # Hazard impact radius
            folium.Circle(
                location=[lat, lng],
                radius=450,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.25,
                weight=1.5
            ).add_to(m)

            # Center Incident Pin
            folium.CircleMarker(
                location=[lat, lng],
                radius=8,
                color=color,
                fill=True,
                fill_color="#ffffff",
                fill_opacity=0.95,
                weight=3,
                tooltip=f"{inc.get('id')}: {title} ({trapped} trapped)"
            ).add_to(m)

        # Inundated Road Blockade & Alternate Safe Corridor
        folium.PolyLine(
            [[12.8480, 74.8580], [12.8465, 74.8624], [12.8450, 74.8670]],
            color="#dc2626",
            weight=5,
            tooltip="ROAD CLOSED: NH-66 Submerged Under 1.8m Water"
        ).add_to(m)

        folium.PolyLine(
            [[12.8715, 74.8450], [12.8600, 74.8550], [12.8465, 74.8624]],
            color="#16a34a",
            weight=4,
            dash_array="6, 6",
            tooltip="SAFE ACCESS CORRIDOR: Peripheral Elevated Link"
        ).add_to(m)

        folium.LayerControl(position='topright').add_to(m)
        st_folium(m, height=460, use_container_width=True, returned_objects=[])

    with col_triage_list:
        st.markdown("##### 🚨 Active Incident Queue (ICS-201)")

        for inc in active_inc:
            is_dispatched = "EN ROUTE" in inc.get("status", "")
            is_crit = "Extreme" in inc.get("severity_level", "")
            card_class = "incident-critical" if is_crit else "incident-elevated"
            status_pill = '<span class="status-badge-green">UNITS EN ROUTE</span>' if is_dispatched else '<span class="status-badge-red">ACTION REQUIRED</span>'

            st.markdown(f"""
            <div class="incident-card {card_class}">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="color:#ea580c; font-weight:700; font-family:'Roboto Mono', monospace; font-size:12px;">{inc.get('id')}</span>
                    <div>{status_pill}</div>
                </div>
                <div style="font-size:14px; font-weight:700; color:#f8fafc; margin-bottom:4px;">{inc.get('title')}</div>
                <div style="font-size:11px; color:#94a3b8; margin-bottom:8px;">
                    Location: <strong>{inc.get('location_name')}</strong> • Trapped: <strong style="color:#f87171;">{inc.get('trapped')} Persons</strong> • Condition: {inc.get('water_crest_rate')}
                </div>
                <div style="background:#0b1120; border:1px solid #1e2e4f; padding:10px 12px; border-radius:6px; font-size:12px; margin-bottom:12px;">
                    <strong style="color:#f8fafc;">Operational Directive:</strong><br>
                    {inc.get('action_directive')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2 = st.columns([1, 1])
            with b1:
                if not is_dispatched:
                    if st.button(f"AUTHORIZE DISPATCH", key=f"disp_{inc.get('id')}", use_container_width=True):
                        inc["status"] = "UNITS EN ROUTE"
                        for u in inc.get("assigned_units", []):
                            match = next((f for f in st.session_state.fleet if f.get("name") == u), None)
                            if match:
                                match["status"] = "EN ROUTE"
                        st.rerun()
            with b2:
                if st.button(f"MARK RESOLVED", key=f"res_{inc.get('id')}", use_container_width=True):
                    inc["status"] = "RESOLVED"
                    st.session_state.rescued_count += inc.get("trapped", 2)
                    for f in st.session_state.fleet:
                        f["status"] = "AVAILABLE"
                    st.rerun()


# ==============================================================================
# TAB 2: INCIDENT ACTION PLAN (IAP / DISPATCH)
# ==============================================================================
with tab_dispatch:
    st.markdown("##### 📋 Incident Action Plan (ICS-204 Deployment Matrix)")
    st.caption("Standard operational assignment matrix pairing response teams with priority disaster zones.")

    col_sim_trig, col_opt = st.columns([6, 6])
    with col_sim_trig:
        st.markdown("###### Incident Ingestion Simulators:")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("+ LOG FLASH FLOOD SOS", use_container_width=True):
                new_id = f"INC-2026-08{len(st.session_state.incidents) + 1}"
                st.session_state.incidents.insert(0, {
                    "id": new_id,
                    "title": "Ullal Coastal Embankment Seawall Breach",
                    "type": "Coastal Flood",
                    "lat": 12.8120,
                    "lng": 74.8450,
                    "location_name": "Someshwar Ward 4",
                    "severity_level": "Level 1 Extreme",
                    "status": "DISPATCH PENDING",
                    "trapped": 10,
                    "total_impacted": 30,
                    "damage_score": 90,
                    "water_crest_rate": "+0.50 m/hr surge",
                    "action_directive": "Deploy NDRF Inflatable Watercraft and airborne flotation drops.",
                    "assigned_units": ["NDRF Gemini Boat Alpha"],
                    "eta_mins": 10.2
                })
                st.rerun()
        with c2:
            if st.button("+ LOG STRUCTURAL COLLAPSE", use_container_width=True):
                new_id = f"INC-2026-08{len(st.session_state.incidents) + 1}"
                st.session_state.incidents.insert(0, {
                    "id": new_id,
                    "title": "Old Port Commercial Warehouse Collapse",
                    "type": "Collapse",
                    "lat": 12.8682,
                    "lng": 74.8385,
                    "location_name": "Bunder Wharf Area",
                    "severity_level": "Level 2 Elevated",
                    "status": "DISPATCH PENDING",
                    "trapped": 5,
                    "total_impacted": 12,
                    "damage_score": 76,
                    "water_crest_rate": "Structural Unstable",
                    "action_directive": "Deploy acoustic search listening probes and heavy shoring team.",
                    "assigned_units": ["SDRF Rescue Squad 3"],
                    "eta_mins": 11.5
                })
                st.rerun()

    with col_opt:
        st.markdown("###### Resource Optimization Engine:")
        if st.button("OPTIMIZE & DISPATCH ALL AVAILABLE TEAMS", use_container_width=True):
            for inc in st.session_state.incidents:
                if inc.get("status") != "RESOLVED":
                    inc["status"] = "UNITS EN ROUTE"
            for f in st.session_state.fleet:
                f["status"] = "EN ROUTE"
            st.rerun()


# ==============================================================================
# TAB 3: AERIAL RECONNAISSANCE FEED (FLIR CANVAS)
# ==============================================================================
with tab_flir:
    st.markdown("##### 🛸 Aerial Reconnaissance & Thermal Imaging Feed")
    st.caption("Real-time optical and radiometric infrared aerial telemetry from Eagle-X UAV over target coordinates.")

    col_flir_view, col_flir_info = st.columns([7, 5])

    with col_flir_view:
        components.html("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { margin:0; padding:0; background:#070d18; overflow:hidden; font-family:'Roboto Mono', monospace; }
                #hud-canvas { width:100%; height:320px; display:block; border:1px solid #1e2e4f; border-radius:6px; }
            </style>
        </head>
        <body>
            <canvas id="hud-canvas" width="640" height="320"></canvas>
            <script>
                const canvas = document.getElementById('hud-canvas');
                const ctx = canvas.getContext('2d');
                let t = 0;

                function renderRecon() {
                    t += 0.03;
                    ctx.clearRect(0, 0, 640, 320);

                    // Thermal Ground Gradient (Realistic Ironbow palette)
                    let g = ctx.createLinearGradient(0, 0, 0, 320);
                    g.addColorStop(0, '#131c31');
                    g.addColorStop(0.5, '#281a44');
                    g.addColorStop(1, '#0c1a33');
                    ctx.fillStyle = g;
                    ctx.fillRect(0, 0, 640, 320);

                    // Flooded river corridor
                    ctx.fillStyle = '#061328';
                    ctx.fillRect(0, 140, 640, 180);

                    // Building structures
                    ctx.fillStyle = '#3f1f4d';
                    ctx.fillRect(110, 90, 140, 130);
                    ctx.beginPath();
                    ctx.moveTo(100, 90); ctx.lineTo(180, 40); ctx.lineTo(260, 90);
                    ctx.fillStyle = '#5c1b52'; ctx.fill();

                    ctx.fillStyle = '#2d1b46';
                    ctx.fillRect(360, 100, 130, 120);

                    // Human Thermal Signatures (White-Hot / Amber cores)
                    for(let i = 0; i < 4; i++) {
                        let hx = 145 + i * 20 + Math.sin(t + i) * 1.5;
                        let hy = 68 + Math.cos(t * 1.2 + i) * 1.5;
                        
                        let rad = ctx.createRadialGradient(hx, hy, 2, hx, hy, 14);
                        rad.addColorStop(0, '#ffffff');
                        rad.addColorStop(0.4, '#fb923c');
                        rad.addColorStop(0.8, '#ea580c');
                        rad.addColorStop(1, 'transparent');
                        ctx.fillStyle = rad;
                        ctx.beginPath();
                        ctx.arc(hx, hy, 14, 0, Math.PI * 2);
                        ctx.fill();
                    }

                    // Tactical HUD Crosshair
                    ctx.strokeStyle = '#38bdf8';
                    ctx.lineWidth = 1.2;
                    ctx.beginPath();
                    ctx.arc(320, 160, 22, 0, Math.PI * 2);
                    ctx.moveTo(320, 125); ctx.lineTo(320, 150);
                    ctx.moveTo(320, 170); ctx.lineTo(320, 195);
                    ctx.moveTo(285, 160); ctx.lineTo(310, 160);
                    ctx.moveTo(330, 160); ctx.lineTo(355, 160);
                    ctx.stroke();

                    // Artificial Horizon Reticle
                    ctx.strokeStyle = 'rgba(148, 163, 184, 0.4)';
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(270, 160); ctx.lineTo(300, 160);
                    ctx.moveTo(340, 160); ctx.lineTo(370, 160);
                    ctx.stroke();

                    // Lock-on Target Box
                    ctx.strokeStyle = '#22c55e';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(130, 48, 90, 44);
                    ctx.fillStyle = '#22c55e';
                    ctx.font = '10px monospace';
                    ctx.fillText('[THERMAL CONTACT: 4 PERS]', 130, 40);

                    // Real OSD Metrics
                    ctx.fillStyle = '#f8fafc';
                    ctx.font = '11px monospace';
                    ctx.fillText('ALT: 124m AGL', 20, 28);
                    ctx.fillText('AIRSPEED: 46.5 km/h', 20, 46);
                    ctx.fillText('COORD: 12.8465°N, 74.8624°E', 20, 305);

                    ctx.fillStyle = '#ef4444';
                    ctx.fillText('RECORDING ●', 530, 28);
                    ctx.fillStyle = '#22c55e';
                    ctx.fillText('BATTERY: 89%', 530, 46);

                    requestAnimationFrame(renderRecon);
                }
                renderRecon();
            </script>
        </body>
        </html>
        """, height=335)

    with col_flir_info:
        st.markdown("###### 📊 Sensor & Telemetry Specifications")
        st.markdown("""
        <div style="background:#111c35; border:1px solid #1e2e4f; border-radius:8px; padding:16px; font-size:12px; line-height:1.9;">
            • Platform: <strong>Eagle-X Hexacopter SAR Drone</strong><br>
            • Sensor Core: <strong>FLIR Boson 640 @ 60Hz Radiometric</strong><br>
            • Operating Altitude: <strong>124m AGL</strong><br>
            • Thermal Detection: <strong style="color:#4ade80;">4 Human Body Heat Blooms Verified</strong><br>
            • Slant Laser Range: <strong>480m to rooftop terrace</strong><br>
            • Mission Payload: <strong>2x Acoustic Flotation Kits Ready</strong>
        </div>
        """, unsafe_allow_html=True)

        if st.button("DEPLOY FLOTATION PAYLOAD WINCH", use_container_width=True):
            st.success("Winch line released: 2 flotation vests dropped directly to stranded individuals.")


# ==============================================================================
# TAB 4: HYDROLOGICAL INUNDATION MODEL (PLOTLY)
# ==============================================================================
with tab_sim:
    st.markdown("##### 🌊 Hydrological Floodwater Level & Cutoff Projections")
    st.caption("Forecast model calculating river crest elevations and identifying road submersions across operational sectors.")

    surge_depth = st.slider("River Gauge Water Level (Meters above datum):", min_value=0.0, max_value=3.5, value=1.8, step=0.1)

    hours = np.linspace(0, 6, 25)
    projected = surge_depth + 0.35 * np.sin(hours * 0.7) + (hours * 0.12)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours,
        y=projected,
        mode='lines+markers',
        name='Projected River Stage',
        line=dict(color='#0284c7', width=3),
        fill='tozeroy',
        fillcolor='rgba(2, 132, 199, 0.18)'
    ))

    fig.add_hline(
        y=1.4,
        line_dash="dash",
        line_color="#dc2626",
        annotation_text="Critical Highway Submergence Point (1.4m)",
        annotation_position="top left"
    )

    fig.update_layout(
        title="6-Hour Flood Stage Forecast (NOAA / Central Water Commission Model)",
        xaxis_title="Forecast Window (Hours Ahead)",
        yaxis_title="Stage Depth (Meters)",
        template="plotly_dark",
        paper_bgcolor='#111c35',
        plot_bgcolor='#0b1120',
        font=dict(family="Inter, sans-serif", color="#cbd5e1"),
        height=320,
        margin=dict(l=40, r=40, t=50, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

    if surge_depth < 0.8:
        st.success("STATUS: ROAD NETWORK CLEAR • Standard ambulances and fire tenders operating normally.")
    elif surge_depth < 1.4:
        st.warning("STATUS: MODERATE WATER ACCUMULATION • Heavy 4x4 rescue vehicles only.")
    else:
        st.error("STATUS: HIGHWAY IMPASSABLE (> 1.4m) • Motorized rescue boats and helicopter hoists required.")


# ==============================================================================
# TAB 5: EMERGENCY RESOURCE INVENTORY
# ==============================================================================
with tab_fleet:
    st.markdown("##### 🚒 Emergency Resource Inventory (ICS-204 Resource List)")
    st.caption("Active tracking of personnel, rescue apparatus, fuel levels, and current mission assignments.")

    f_col1, f_col2 = st.columns(2)

    for idx, f in enumerate(st.session_state.fleet):
        col = f_col1 if idx % 2 == 0 else f_col2
        is_avail = f.get("status") == "AVAILABLE"
        badge = '<span class="status-badge-green">AVAILABLE</span>' if is_avail else '<span class="status-badge-amber">DISPATCHED</span>'

        with col:
            st.markdown(f"""
            <div style="background:#111c35; border:1px solid #1e2e4f; border-radius:8px; padding:16px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <strong style="color:#f8fafc; font-size:14px;">{f.get('name')}</strong>
                    <div>{badge}</div>
                </div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.8;">
                    • Asset ID: <strong style="color:#f8fafc;">{f.get('id')}</strong> • Category: {f.get('category')}<br>
                    • Operating Station: {f.get('station')}<br>
                    • Crew Size: <strong>{f.get('crew', 4)} Specialists</strong> • Extraction Capacity: <strong style="color:#4ade80;">{f.get('capacity', 4)} Persons</strong><br>
                    • Equipment Readiness / Fuel: <strong>{f.get('battery', 90)}%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if is_avail:
                if st.button(f"DISPATCH {f.get('id')}", key=f"f_dep_{f.get('id')}", use_container_width=True):
                    f["status"] = "EN ROUTE"
                    st.rerun()
            else:
                if st.button(f"RECALL {f.get('id')} TO BASE", key=f"f_rec_{f.get('id')}", use_container_width=True):
                    f["status"] = "AVAILABLE"
                    st.rerun()
