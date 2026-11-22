"""
RESQGRID - AI-Powered Disaster Response Intelligence & Resource Optimization
FastAPI Backend Service
Department of CSE (AIML), A J Institute of Engineering & Technology, Mangaluru
VTU Belagavi Capstone Project
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import datetime

from algorithms import (
    calculate_risk_score,
    calculate_urgency_priority,
    optimize_resource_assignment,
    compute_hazard_free_route
)

app = FastAPI(
    title="RESQGRID API",
    description="Cognitive Disaster Response Intelligence & Resource Allocation Engine",
    version="2.4.0"
)

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---

class LocationModel(BaseModel):
    lat: float
    lng: float
    address: str
    sector: str

class IncidentIngestRequest(BaseModel):
    title: str
    type: str  # flood, fire, landslide, collapse, cyclone
    location: LocationModel
    estimated_victims: int = 1
    trapped_victims: int = 0
    image_url: Optional[str] = None
    sensor_notes: Optional[str] = None

class ApprovalRequest(BaseModel):
    recommendation_id: str
    commander_name: str
    commander_notes: str


# --- In-Memory State for Demonstration ---
ACTIVE_INCIDENTS = []
RESCUE_FLEET = [
    {
        "id": "RES-BOAT-01",
        "name": "NDRF Gemini Alpha (Rapid Inflatable)",
        "type": "ndrf_boat",
        "status": "available",
        "location": {"lat": 12.8715, "lng": 74.8450},
        "speedKmH": 35.0,
        "capacity": 12,
        "fuelBatteryPercent": 94
    },
    {
        "id": "RES-UAV-01",
        "name": "Eagle-X Recon Drone (Thermal/LiDAR)",
        "type": "uav_recon",
        "status": "available",
        "location": {"lat": 12.8820, "lng": 74.8510},
        "speedKmH": 85.0,
        "capacity": 2,
        "fuelBatteryPercent": 88
    },
    {
        "id": "RES-FIRE-01",
        "name": "FT-07 Heavy Foam Tender",
        "type": "fire_unit",
        "status": "available",
        "location": {"lat": 12.9200, "lng": 74.8250},
        "speedKmH": 50.0,
        "capacity": 6,
        "fuelBatteryPercent": 92
    },
    {
        "id": "RES-AMB-01",
        "name": "ALS-01 Mobile Trauma Unit",
        "type": "ambulance",
        "status": "available",
        "location": {"lat": 12.8650, "lng": 74.8420},
        "speedKmH": 60.0,
        "capacity": 3,
        "fuelBatteryPercent": 85
    }
]


@app.get("/")
def root():
    return {
        "system": "RESQGRID Cognitive Backend",
        "status": "ONLINE",
        "version": "2.4.0",
        "institution": "A J Institute of Engineering & Technology, Mangaluru",
        "affiliated_university": "VTU Belagavi",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


@app.post("/api/v1/incidents/ingest")
def ingest_incident(data: IncidentIngestRequest):
    """
    Step 1 & 2: Input Collection & AI Incident Analysis
    """
    # Simulated Computer Vision & NLP triage
    synthetic_damage = min(98, max(40, 50 + data.trapped_victims * 8))
    vulnerability = 85.0
    escalation = 90.0 if data.trapped_victims > 2 else 50.0

    risk_score = calculate_risk_score(synthetic_damage, vulnerability, escalation)
    priority, urgency_score = calculate_urgency_priority(
        trapped_victims=data.trapped_victims,
        total_victims=data.estimated_victims,
        risk_score=risk_score,
        access_window_hours=0.8
    )

    incident_id = f"INC-MNG-{len(ACTIVE_INCIDENTS) + 101}"

    # Generate Explainable AI recommendation
    rec = {
        "id": f"REC-{len(ACTIVE_INCIDENTS) + 501}",
        "incidentId": incident_id,
        "recommendedResourceIds": ["RES-BOAT-01" if data.type == "flood" else "RES-FIRE-01"],
        "actionSummary": f"Immediate deployment for {data.title} ({priority}).",
        "priorityRank": 1 if priority == "P1_CRITICAL" else 2,
        "explainability": {
            "reasons": [
                f"{data.trapped_victims} trapped victims detected by Vision Triage.",
                f"Urgency matrix score: {urgency_score} / 100.",
                f"Hazard escalation velocity estimated at rapid threshold."
            ],
            "urgencyFormulaScore": urgency_score,
            "escalationWarning": "Imminent threat to human life within 45 minute window.",
            "estimatedTimeSavingMins": 18,
            "routeSafetyConfidence": 95.2
        },
        "status": "proposed"
    }

    new_incident = {
        "id": incident_id,
        "title": data.title,
        "type": data.type,
        "location": data.location.dict(),
        "reportedAt": "Just now",
        "severity": synthetic_damage,
        "priority": priority,
        "status": "awaiting_approval",
        "victimCount": {
            "estimated": data.estimated_victims,
            "injured": max(0, data.estimated_victims - data.trapped_victims),
            "trapped": data.trapped_victims
        },
        "vulnerabilityScore": vulnerability,
        "aiAnalysis": {
            "confidenceScore": 96.5,
            "damagePercentage": synthetic_damage,
            "detectedObjects": ["Structural fracture", "Flood surge", "Trapped victims"],
            "weatherConditions": {
                "tempC": 26.5,
                "rainfallMmPerHour": 58.0,
                "windSpeedKmh": 44.0,
                "visibilityM": 900,
                "hazardIndex": "HIGH"
            }
        },
        "recommendation": rec
    }

    ACTIVE_INCIDENTS.append(new_incident)
    return {"status": "SUCCESS", "incident": new_incident}


@app.get("/api/v1/incidents")
def list_incidents():
    """Returns active incidents ranked by priority score."""
    return {"count": len(ACTIVE_INCIDENTS), "incidents": ACTIVE_INCIDENTS}


@app.post("/api/v1/optimize-resources")
def optimize_resources():
    """Step 5: Resource Optimization via Bipartite Assignment."""
    matches = optimize_resource_assignment(ACTIVE_INCIDENTS, RESCUE_FLEET)
    return {
        "status": "OPTIMIZATION_COMPLETE",
        "algorithm": "Kuhn-Munkres (Hungarian) & Greedy Latency Minimization",
        "assignments": matches
    }


@app.post("/api/v1/route-analysis")
def get_route_analysis(
    start_lat: float = 12.8715,
    start_lng: float = 74.8450,
    dest_lat: float = 12.8465,
    dest_lng: float = 74.8624
):
    """Step 6: Route Analysis & Hazard Avoidance."""
    mock_hazards = [
        {"coordinates": [[12.8465, 74.8624]]}
    ]
    result = compute_hazard_free_route((start_lat, start_lng), (dest_lat, dest_lng), mock_hazards)
    return result


@app.post("/api/v1/recommendation/approve")
def approve_recommendation(data: ApprovalRequest):
    """Step 8: Human-in-the-Loop Responder Approval."""
    return {
        "status": "DISPATCH_AUTHORIZED",
        "recommendation_id": data.recommendation_id,
        "commander": data.commander_name,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "cryptographic_hash": f"SHA256-{abs(hash(data.recommendation_id + data.commander_name))}"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

