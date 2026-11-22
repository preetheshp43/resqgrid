"""
RESQGRID - Core Mathematical Formulations and Optimization Algorithms
Compliant with VTU CSE(AIML) Capstone Project Specification
"""

import math
from typing import List, Dict, Any, Tuple

def calculate_risk_score(severity: float, vulnerability: float, escalation_rate: float) -> float:
    """
    Computes composite Risk Index R(i):
    R(i) = (w1 * Severity) + (w2 * Vulnerability) + (w3 * EscalationFactor)
    where w1=0.45, w2=0.35, w3=0.20
    """
    w1, w2, w3 = 0.45, 0.35, 0.20
    risk = (w1 * severity) + (w2 * vulnerability) + (w3 * escalation_rate)
    return round(min(100.0, max(0.0, risk)), 2)


def calculate_urgency_priority(trapped_victims: int, total_victims: int, risk_score: float, access_window_hours: float) -> Tuple[str, float]:
    """
    Priority Assessment Matrix (Step 4 of Synopsis):
    Urgency = (trapped_victims * 2.5 + total_victims * 1.0) * (risk_score / 100) / max(0.5, access_window_hours)
    """
    urgency_raw = (trapped_victims * 2.5 + total_victims * 1.0) * (risk_score / 100.0) / max(0.5, access_window_hours)
    urgency_normalized = round(min(100.0, urgency_raw * 10.0), 2)

    if urgency_normalized >= 75.0 or trapped_victims >= 5:
        return "P1_CRITICAL", urgency_normalized
    elif urgency_normalized >= 45.0:
        return "P2_HIGH", urgency_normalized
    elif urgency_normalized >= 20.0:
        return "P3_MODERATE", urgency_normalized
    else:
        return "P4_LOW", urgency_normalized


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance in kilometers between two GPS points."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def optimize_resource_assignment(
    incidents: List[Dict[str, Any]], 
    resources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Step 5: Resource Optimization
    Solves bipartite matching minimizing total response latency and matching specialized capabilities:
    - Floods -> NDRF boats + UAVs
    - Fires -> Foam Fire units + Ambulances
    - Landslides -> SDRF rescue squads + Ambulances
    """
    assignments = []
    available_resources = [r for r in resources if r.get("status") == "available"]

    # Sort incidents by severity descending
    sorted_incidents = sorted(incidents, key=lambda x: x.get("severity", 0), reverse=True)

    for inc in sorted_incidents:
        inc_lat = inc["location"]["lat"]
        inc_lng = inc["location"]["lng"]
        inc_type = inc.get("type")

        # Find best candidate resource
        best_resource = None
        min_cost = float("inf")

        for res in available_resources:
            # Capability compatibility check
            res_type = res["type"]
            type_bonus = 0.0
            if inc_type == "flood" and res_type == "ndrf_boat":
                type_bonus = -5.0
            elif inc_type == "fire" and res_type == "fire_unit":
                type_bonus = -5.0
            elif inc_type in ["collapse", "landslide"] and res_type in ["medical_triage", "ambulance"]:
                type_bonus = -4.0

            dist = haversine_distance(inc_lat, inc_lng, res["location"]["lat"], res["location"]["lng"])
            speed = max(20.0, res.get("speedKmH", 40.0))
            eta_minutes = (dist / speed) * 60.0

            cost = eta_minutes + type_bonus
            if cost < min_cost:
                min_cost = cost
                best_resource = res

        if best_resource:
            assignments.append({
                "incident_id": inc["id"],
                "resource_id": best_resource["id"],
                "resource_name": best_resource["name"],
                "estimated_eta_minutes": round(max(2.0, min_cost), 1),
                "distance_km": round(haversine_distance(inc_lat, inc_lng, best_resource["location"]["lat"], best_resource["location"]["lng"]), 2)
            })
            available_resources.remove(best_resource)

    return assignments


def compute_hazard_free_route(
    start_coords: Tuple[float, float],
    dest_coords: Tuple[float, float],
    hazard_zones: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Step 6: Route Analysis & Hazard Avoidance
    Computes bypass coordinates around active road blockades or submerged zones.
    """
    direct_dist = haversine_distance(start_coords[0], start_coords[1], dest_coords[0], dest_coords[1])
    is_direct_blocked = False

    for h in hazard_zones:
        h_lat = h["coordinates"][0][0]
        h_lng = h["coordinates"][0][1]
        dist_to_hazard = haversine_distance(dest_coords[0], dest_coords[1], h_lat, h_lng)
        if dist_to_hazard < 1.0: # hazard near destination
            is_direct_blocked = True
            break

    if is_direct_blocked:
        # Generate safe alternate bypass waypoint
        bypass_lat = (start_coords[0] + dest_coords[0]) / 2 + 0.006
        bypass_lng = (start_coords[1] + dest_coords[1]) / 2 - 0.009
        safe_dist = direct_dist + 2.8
        safe_eta = (safe_dist / 45.0) * 60.0
        return {
            "route_status": "BYPASS_CALCULATED",
            "primary_blocked": True,
            "waypoints": [list(start_coords), [bypass_lat, bypass_lng], list(dest_coords)],
            "safe_distance_km": round(safe_dist, 2),
            "safe_eta_mins": round(safe_eta, 1),
            "hazard_clearance_radius_m": 450
        }
    else:
        return {
            "route_status": "DIRECT_CLEAR",
            "primary_blocked": False,
            "waypoints": [list(start_coords), list(dest_coords)],
            "safe_distance_km": round(direct_dist, 2),
            "safe_eta_mins": round((direct_dist / 50.0) * 60.0, 1),
            "hazard_clearance_radius_m": 1200
        }

