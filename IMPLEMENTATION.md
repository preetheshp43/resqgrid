# RESQGRID – AI-Powered Disaster Response Intelligence & Resource Optimization
### Visvesvaraya Technological University (VTU) Belagavi
**Department of Computer Science & Engineering (Artificial Intelligence & Machine Learning)**  
**A J Institute of Engineering and Technology (AJIET), Mangaluru – 575006**  
**Academic Year:** 2026–2027

---

## 1. Executive Summary & Project Synopsis

**RESQGRID** is an end-to-end cognitive emergency response intelligence and combinatorial resource optimization platform engineered to support disaster management authorities, municipal emergency operation centers (EOCs), and search-and-rescue teams (NDRF/SDRF/Fire/Medical) during catastrophic events (floods, landslides, structural fires, cyclones, and building collapses).

During mass-casualty disaster events, ground information streams from heterogeneous, noisy channels: citizen SOS dispatches, geo-tagged mobile imagery, municipal flood sensors, and drone surveillance feeds. Simultaneously, emergency resources (NDRF inflatable rescue boats, Advanced Life Support ambulances, foam fire tenders, reconnaissance UAVs) are scarce, while physical transportation corridors are obstructed by rising waters, debris, or toxic plumes.

RESQGRID resolves this challenge by synthesizing **Multi-Modal AI (Computer Vision + NLP)**, **Mathematical Risk & Urgency Scoring**, **Combinatorial Resource Matching (Hungarian Algorithm / MILP)**, **Hazard-Avoidance Path Routing**, and **Explainable AI (XAI) Next-Move Recommendations**, while strictly enforcing **Human-in-the-Loop Commander Authorization**.

---

## 2. Investigators & Academic Leadership

- **Preethesh** `[USN: 4JK24CI082]` – *System Architecture & AI Resource Optimization*
- **Pavan Kumar** `[USN: 4JK24CI080]` – *Full-Stack Command HUD & GIS Navigation*
- **Yashash** `[USN: 4JK24CI121]` – *Computer Vision & Damage Triage Pipelines*
- **Mugil Kumar** `[USN: 4JK24CI074]` – *Explainable AI & Natural Language Ingestion*

### Faculty Guidance
- **Project Guide:** Dr. Pradeep Udupa, *Associate Professor, Dept. of CSE (AI&ML)*
- **Mini Project Coordinator:** Mrs. Deeptha Hegde, *Assistant Professor, Dept. of CSE (AI&ML)*
- **Head of Department (HOD):** Mr. Chanchal Antony, *Department of CSE (AI&ML)*
- **Institution:** A J Institute of Engineering and Technology, Kottara Chowki, Mangaluru, Karnataka

---

## 3. End-to-End 9-Stage Architecture (Fig. 1 Compliance)

```
[ START ]
   │
   ▼
1. Input Collection (Citizen reports, GPS coordinates, Drone feeds, Weather)
   │
   ▼
2. Incident Analysis (Computer Vision damage grading, victim estimation, NLP)
   │
   ▼
3. Risk Assessment (Vulnerability indexing, severity, escalation prediction)
   │
   ▼
4. Priority Assessment (Urgency triage matrix: P1 Critical, P2 High, P3 Moderate)
   │
   ▼
5. Resource Optimization (Bipartite matching: Boats, UAVs, Ambulances, Fire units)
   │
   ▼
6. Route Analysis (Safe corridor routing, avoidance of submerged/blocked roads)
   │
   ▼
7. Next-Move Recommendation (Explainable AI decision plan with explicit rationale)
   │
   ▼
8. Human Approval ◄────────┐ (Commander reviews, modifies, or confirms)
   │                       │ (Revise/Modify loop)
   ▼                       │
9. Command Dashboard ──────┘ (Real-time GIS map, fleet status, audio-visual HUD)
   │
   ▼
[ END ]
```

### The 5 AI Cognitive Stages
1. **Understand:** Ingests raw unstructured text, multi-spectral drone imagery, GPS data, and dynamic meteorological variables.
2. **Correlate:** Integrates geospatial topology with sensor feeds to verify and de-duplicate disaster reports.
3. **Assess:** Computes composite Risk \(R_i\) and Urgency Priority scores based on trapped lives and vulnerability.
4. **Predict:** Projects floodwater crest velocity, fire smoke plumes, and calculates hazard-free shortest paths.
5. **Recommend:** Generates human-auditable action proposals with quantified time-savings and transparent logic.

---

## 4. Key Mathematical & Algorithmic Formulations

### 4.1 Composite Risk Index Formula
The dynamic risk score \(R_i \in [0, 100]\) for incident \(i\) is evaluated using a weighted multi-factor regression:

$$\text{Risk}_i = w_1 \cdot \text{Severity}_i + w_2 \cdot \text{Vulnerability}_i + w_3 \cdot \text{EscalationFactor}_i$$

*Standard parameter weights:* \(w_1 = 0.45\), \(w_2 = 0.35\), \(w_3 = 0.20\).

### 4.2 Dynamic Urgency Triage Formula
$$\text{Urgency}_i = \frac{(\text{Victims}_{\text{trapped}} \times 2.5 + \text{Victims}_{\text{total}} \times 1.0) \times (\text{Risk}_i / 100)}{\max(0.5, \Delta t_{\text{access}})}$$

- **P1 Critical:** \(\text{Urgency} \ge 75\) or \(\text{Victims}_{\text{trapped}} \ge 5\)
- **P2 High:** \(45 \le \text{Urgency} < 75\)
- **P3 Moderate:** \(20 \le \text{Urgency} < 45\)

### 4.3 Resource Allocation Problem (Bipartite Matching)
Given a set of active incidents \(I\) and available rescue assets \(R\), the system minimizes the total response latency while satisfying equipment and capacity constraints:

$$\min \sum_{i \in I} \sum_{j \in R} C_{ij} \cdot X_{ij}$$

$$\text{Subject to:} \quad \sum_{j \in R} X_{ij} \le 1, \quad \sum_{i \in I} X_{ij} \le 1, \quad X_{ij} \in \{0, 1\}$$

where \(C_{ij}\) is the travel time penalized by vehicle-hazard compatibility (e.g. infinite penalty for deploying standard ambulances across flooded corridors).

### 4.4 Hazard-Free Routing Heuristic (Penalized A*)
$$\text{Cost}(u, v) = \text{EuclideanDist}(u, v) + \sum_{k \in \text{Hazards}} \frac{\text{Severity}_k}{\text{Distance}(v, \text{Hazard}_k)^2}$$

---

## 5. Technology Stack & Implementation Directory

| Tier | Technologies |
|---|---|
| **Frontend Framework** | React 18, TypeScript, Vite, Tailwind CSS |
| **3D Graphics & Animations** | Three.js (WebGL interactive tactical globe & drone radar), GSAP 3 + ScrollTrigger |
| **GIS Mapping** | Leaflet, OpenStreetMap Dark Matter Tiles |
| **Tactical Audio** | Native Web Audio API Synthesizer (Zero asset dependencies) |
| **Backend API** | Python 3.11, FastAPI, Pydantic, Uvicorn |
| **Optimization Algorithms** | SciPy, NumPy, Kuhn-Munkres / Greedy Heuristics |
| **Database** | PostgreSQL / Supabase Schema (documented below) |

### Workspace Directory Structure
```
resqrid/
├── backend/
│   ├── algorithms.py         # Risk, Urgency, Hungarian matching, and Routing formulas
│   ├── main.py               # FastAPI endpoints (/ingest, /optimize, /route, /approve)
│   └── requirements.txt      # Python dependencies
├── src/
│   ├── components/
│   │   ├── 3d/
│   │   │   ├── Hero3DScene.tsx      # Interactive 3D WebGL Holographic Earth & UAV Mesh
│   │   │   └── TacticalRadar3D.tsx  # 3D concentric radar scan widget
│   │   ├── dashboard/
│   │   │   ├── CommandDashboard.tsx     # Centralized mission control hub
│   │   │   ├── HumanApprovalModal.tsx   # Step 8: Commander authorization interface
│   │   │   ├── IncidentFeed.tsx         # Step 4: Urgency priority queue
│   │   │   ├── IncidentIntakeModal.tsx  # Step 1 & 2: Citizen SOS with simulated CV
│   │   │   ├── NextMoveCard.tsx         # Step 7: Explainable AI recommendation card
│   │   │   ├── ResourceFleet.tsx        # Step 5: Rescue fleet readiness view
│   │   │   ├── RouteAnalysisModal.tsx   # Step 6: Hazard-free corridor inspection
│   │   │   ├── TacticalMap.tsx          # Step 9: Interactive GIS Leaflet dark map
│   │   │   └── TacticalNavbar.tsx       # Live status clock, Defcon level, quick triggers
│   │   └── landing/
│   │       ├── ArchitectureSection.tsx  # 3-Tier specification & hardware matrix
│   │       ├── GSAPWorkflowSection.tsx  # GSAP + ScrollTrigger 9-stage sequence
│   │       ├── HeroSection.tsx          # Hero presentation overlay
│   │       ├── Navbar.tsx               # Top navigation bar
│   │       └── ProjectCredits.tsx       # VTU AJIET faculty & student credits
│   ├── data/
│   │   └── mockData.ts       # Realistic Mangaluru regional disaster dataset
│   ├── types/
│   │   └── index.ts          # Complete TypeScript domain interfaces
│   ├── utils/
│   │   └── audio.ts          # Synthesized Web Audio API tactical sounds
│   ├── App.tsx               # Main application root
│   ├── index.css             # Tailwind layers & dark HUD theme
│   └── main.tsx              # React DOM entrypoint
├── IMPLEMENTATION.md         # Comprehensive project documentation
├── index.html                # HTML entrypoint with Leaflet and Google Fonts
├── package.json              # NPM manifest
├── tailwind.config.js        # Tactical neon palette configuration
├── tsconfig.json             # TypeScript compiler settings
└── vite.config.ts            # Vite bundler configuration
```

---

## 6. How to Run & Verify the System

### 6.1 Frontend Application
The frontend is pre-configured and production-built. To start the live development server:
```bash
npm run dev
```
Open your browser at `http://localhost:5173`.

**Interactive Features to Explore:**
1. **Interactive 3D Hero Scene:** Move your mouse over the holographic digital globe; observe the 3D drone mesh orbiting with rotating radar scan cones and pulsing disaster beacons.
2. **GSAP 9-Stage AI Workflow:** Scroll down or click the stage tabs (1 through 9) to view the mathematical formulations, technical capabilities, and cognitive stages.
3. **Launch Command Dashboard:** Click the glowing **"Launch Command HUD"** button in the header or the floating pill at the bottom right.
4. **Interactive GIS Map:** Click on any incident marker (Red P1, Amber P2, Cyan P3) in Mangaluru (Jeppinamogaru, Baikampady, Gurupura, Panambur). Watch the map smoothly fly to the incident coordinate.
5. **Explainable AI Next-Move:** In the bottom-left card, review the AI recommendation, mathematical score breakdown, and time-saving metrics.
6. **Step 8 Human Approval:** Click **"Review & Authorize Dispatch"**, input operational notes, and electronically sign the order to dispatch units.
7. **Hazard Route Inspection:** Click **"View Safe Corridor Route"** to compare the blocked primary highway with the AI-calculated safe bypass corridor.
8. **Simulate Citizen SOS Report:** Click **"Report SOS Incident"**, click **"Run CV Pipeline"** to simulate convolutional damage detection, and ingest the incident into the live priority queue.

### 6.2 Python FastAPI Backend (Optional Local Microservice)
```bash
cd backend
pip install -r requirements.txt
python main.py
```
FastAPI interactive Swagger documentation will be available at `http://localhost:8000/docs`.

---

## 7. Database Schema (PostgreSQL / Supabase DDL)

```sql
-- 1. Incidents Table
CREATE TABLE incidents (
    id VARCHAR(32) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    disaster_type VARCHAR(32) NOT NULL CHECK (disaster_type IN ('flood', 'fire', 'landslide', 'earthquake', 'cyclone', 'collapse')),
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    address TEXT NOT NULL,
    sector VARCHAR(64) NOT NULL,
    severity INTEGER CHECK (severity BETWEEN 1 AND 100),
    priority VARCHAR(16) NOT NULL CHECK (priority IN ('P1_CRITICAL', 'P2_HIGH', 'P3_MODERATE', 'P4_LOW')),
    status VARCHAR(32) NOT NULL DEFAULT 'awaiting_approval',
    trapped_victims INTEGER DEFAULT 0,
    estimated_victims INTEGER DEFAULT 0,
    vulnerability_score INTEGER DEFAULT 50,
    image_url TEXT,
    reported_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Rescue Fleet Table
CREATE TABLE rescue_resources (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    resource_type VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'available',
    current_lat DECIMAL(10, 7) NOT NULL,
    current_lng DECIMAL(10, 7) NOT NULL,
    base_station VARCHAR(128) NOT NULL,
    speed_kmh DECIMAL(5, 2) NOT NULL,
    crew_capacity INTEGER NOT NULL,
    battery_fuel_percent INTEGER CHECK (battery_fuel_percent BETWEEN 0 AND 100),
    assigned_incident_id VARCHAR(32) REFERENCES incidents(id)
);

-- 3. Next-Move Audit Logs Table (Human Approval)
CREATE TABLE recommendations_audit (
    id VARCHAR(32) PRIMARY KEY,
    incident_id VARCHAR(32) REFERENCES incidents(id),
    action_summary TEXT NOT NULL,
    urgency_score DECIMAL(5, 2) NOT NULL,
    status VARCHAR(32) NOT NULL,
    commander_name VARCHAR(128),
    commander_notes TEXT,
    approved_at TIMESTAMP WITH TIME ZONE
);
```

---

## 8. Academic References

1. **H. Zheng, X. Zhao, X. Yang, and B. Chen**, *"Predictive Resource Request for Disaster Response: A Deep Learning-Based Optimization Model,"* Information Systems Research, vol. 35, no. 2, pp. 528–550, 2024.
2. **W. Wang, K. Yang, L. Yang, and Z. Gao**, *"Distributionally Robust Chance-Constrained Programming for Multi-Period Emergency Resource Allocation and Vehicle Routing in Disaster Response Operations,"* Omega, vol. 120, Art. 102915, 2023.
3. **N. Al Theeb and C. Murray**, *"Vehicle Routing and Resource Distribution in Postdisaster Humanitarian Relief Operations,"* International Transactions in Operational Research, vol. 24, no. 6, pp. 1253–1284, 2017.
4. **T. I. Faiz, C. Vogiatzis, J. Liu, and M. Noor-E-Alam**, *"A Robust Optimization Framework for Two-Echelon Vehicle and UAV Routing for Post-Disaster Humanitarian Logistics Operations,"* Networks, vol. 84, no. 2, pp. 200–219, 2024.
5. **United Nations Office for Disaster Risk Reduction (UNDRR)**, *Special Report on the Use of Technology for Disaster Risk Reduction*, 2025.
6. **UNDRR, World Meteorological Organization (WMO), and ITU**, *Leveraging AI to Enhance Multi-Hazard Early Warning Systems*, 2026.

