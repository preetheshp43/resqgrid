export type DisasterType = 'flood' | 'fire' | 'landslide' | 'earthquake' | 'cyclone' | 'collapse';

export type PriorityLevel = 'P1_CRITICAL' | 'P2_HIGH' | 'P3_MODERATE' | 'P4_LOW';

export type IncidentStatus = 
  | 'pending_analysis'
  | 'awaiting_approval'
  | 'dispatched'
  | 'on_scene'
  | 'resolved';

export interface LocationCoords {
  lat: number;
  lng: number;
  address: string;
  sector: string;
}

export interface AIAnalysisResult {
  confidenceScore: number; // 0 - 100
  damagePercentage: number; // 0 - 100
  detectedObjects: string[];
  weatherConditions: {
    tempC: number;
    rainfallMmPerHour: number;
    windSpeedKmh: number;
    visibilityM: number;
    hazardIndex: 'EXTREME' | 'HIGH' | 'MODERATE' | 'LOW';
  };
  structuralRisk: string;
  victimConfidence: number;
}

export interface NextMoveRecommendation {
  id: string;
  incidentId: string;
  recommendedResourceIds: string[];
  actionSummary: string;
  priorityRank: number;
  explainability: {
    reasons: string[];
    urgencyFormulaScore: number; // calculated score
    escalationWarning: string;
    estimatedTimeSavingMins: number;
    routeSafetyConfidence: number;
  };
  status: 'proposed' | 'approved' | 'rejected' | 'modified';
  approvedBy?: string;
  approvedAt?: string;
  notes?: string;
}

export interface Incident {
  id: string;
  title: string;
  type: DisasterType;
  location: LocationCoords;
  reportedAt: string;
  severity: number; // 1-100
  priority: PriorityLevel;
  status: IncidentStatus;
  victimCount: {
    estimated: number;
    injured: number;
    trapped: number;
  };
  vulnerabilityScore: number; // 1-100 (population density, age index, water proximity)
  escalationRisk: 'rapid' | 'moderate' | 'stable';
  aiAnalysis: AIAnalysisResult;
  imageUrl: string;
  assignedResourceIds: string[];
  recommendation?: NextMoveRecommendation;
}

export type ResourceType = 
  | 'ndrf_boat' 
  | 'ambulance' 
  | 'fire_unit' 
  | 'uav_recon' 
  | 'medical_triage' 
  | 'air_rescue';

export interface RescueResource {
  id: string;
  name: string;
  type: ResourceType;
  status: 'available' | 'assigned' | 'en_route' | 'on_scene' | 'maintenance';
  location: {
    lat: number;
    lng: number;
    baseStation: string;
  };
  speedKmH: number;
  capacity: number;
  crewCount: number;
  equipment: string[];
  fuelBatteryPercent: number;
  assignedIncidentId?: string;
}

export interface RouteHazard {
  id: string;
  type: 'flooded_road' | 'bridge_collapse' | 'debris_blockage' | 'fire_perimeter';
  name: string;
  coordinates: [number, number][];
  riskLevel: 'impassable' | 'caution';
  severity: number;
}

