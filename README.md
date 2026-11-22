# 🚨 RESQGRID – AI-Powered Disaster Response Intelligence & Resource Optimization

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **RESQGRID** is an end-to-end cognitive disaster response intelligence and combinatorial resource allocation platform. It ingests multi-modal disaster reports, synthesizes real-time Computer Vision damage grading, prioritizes crisis sectors, optimizes rescue fleets via the Hungarian algorithm, and generates explainable next-move action plans with human commander oversight.

---

## 🌟 Interactive Features (100% Functional)

1. **🌐 3D Tactical WebGL Hero Radar**:
   - Interactive Three.js WebGL Holographic Earth Globe with rotating sensor scan cones, pulsing disaster beacons, and mouse-tracking parallax.
2. **🛰️ 3D Geospatial PyDeck & Folium GIS Map**:
   - 3D Hexagon Column elevation layer mapping disaster severity across coordinates.
   - Live color-coded priority markers (Red P1 Critical, Amber P2 High, Cyan P3 Moderate).
   - Real-time road hazard corridors (submerged underpasses) and AI-computed safe alternate corridors.
3. **📸 Computer Vision Damage Classifier & SOS Intake**:
   - Upload drone or mobile photos (`.jpg`, `.png`) to trigger convolutional image analysis.
   - Object detection and damage percentage scoring (submerged roofs, trapped civilians).
   - Ingests emergency reports directly into the active triage dispatch queue.
4. **⚡ Explainable AI (XAI) Next-Move Engine**:
   - Mathematical Urgency Score breakdown formula:
     $$\text{Urgency} = \frac{(\text{Trapped} \times 2.5 + \text{Total} \times 1.0) \times (\text{Risk} / 100)}{\max(0.5, \text{AccessTime})}$$
   - Transparent rationale detailing why a unit is dispatched, water crest windows, and estimated response minutes saved.
5. **🛡️ Human-in-the-Loop Commander Authorization**:
   - Review AI proposals, customize unit assignments, add tactical directives, and electronically sign dispatch authorizations.
   - Automatically moves units into `en_route` status and records an immutable cryptographic audit log.
6. **🚒 Combinatorial Resource Optimization (Hungarian Solver)**:
   - Solves the bipartite matching problem to match available NDRF rescue boats, ALS trauma ambulances, heavy foam tenders, and thermal recon UAVs with high-priority emergencies.
7. **🔊 Tactical Audio Synthesizer**:
   - Pure Web Audio API synthesized alert sirens, dispatch confirmation chimes, and telemetry clicks.

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/resqgrid.git
cd resqgrid
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit Application
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## ☁️ How to Host on Streamlit Cloud (1-Click Free Deployment)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "feat: RESQGRID AI Disaster Response Intelligence System"
   git branch -M main
   git remote add origin https://github.com/<your-username>/resqgrid.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Community Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with your GitHub account.
   - Click **"Create app"** (or **"New app"**).
   - Select your repository: `<your-username>/resqgrid`.
   - Branch: `main`.
   - Main file path: `app.py`.
   - Click **"Deploy!"**.

Streamlit Cloud will automatically install all dependencies from `requirements.txt`, apply the tactical dark theme from `.streamlit/config.toml`, and generate a public live link for your project!

---

## 📁 Repository Structure

```
resqgrid/
├── .streamlit/
│   └── config.toml          # Tactical dark cyber-command theme
├── app.py                   # Main interactive Streamlit application
├── requirements.txt         # Python dependencies for Streamlit Cloud
├── .gitignore               # Standard Git ignore file
└── README.md                # Project documentation and deployment guide
```

---

## 📄 License
This project is licensed under the MIT License.

