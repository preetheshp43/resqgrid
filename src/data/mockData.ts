import { Incident, RescueResource, RouteHazard } from '../types';

// Mangaluru / Coastal Karnataka & Western Ghats Region Context
// (Aligns with AJIET Mangaluru / VTU Synopsis Project Scope)
export const INITIAL_INCIDENTS: Incident[] = [
  {
    id: 'INC-MNG-001',
    title: 'Severe Flash Flood & Submerged Settlement',
    type: 'flood',
    location: {
      lat: 12.8465,
      lng: 74.8624,
      address: 'Jeppinamogaru, Netravati River Basin',
      sector: 'Sector Delta-4'
    },
    reportedAt: '12 mins ago',
    severity: 94,
    priority: 'P1_CRITICAL',
    status: 'awaiting_approval',
    victimCount: {
      estimated: 18,
      injured: 4,
      trapped: 14
    },
    vulnerabilityScore: 89,
    escalationRisk: 'rapid',
    aiAnalysis: {
      confidenceScore: 98.2,
      damagePercentage: 86,
      detectedObjects: ['Submerged residential roofs (7)', 'Stranded family group (3 kids)', 'Floating debris'],
      weatherConditions: {
        tempC: 26.5,
        rainfallMmPerHour: 68.4,
        windSpeedKmh: 48,
        visibilityM: 800,
        hazardIndex: 'EXTREME'
      },
      structuralRisk: 'Masonry foundation saturation warning; imminent collapse within 45 mins if water exceeds 2.8m mark.',
      victimConfidence: 96.4
    },
    imageUrl: 'https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80',
    assignedResourceIds: [],
    recommendation: {
      id: 'REC-001',
      incidentId: 'INC-MNG-001',
      recommendedResourceIds: ['RES-BOAT-01', 'RES-UAV-01', 'RES-AMB-01'],
      actionSummary: 'Immediate air reconnaissance and dual inflatable rescue boat deployment with water paramedics.',
      priorityRank: 1,
      explainability: {
        reasons: [
          'Water level rising at critical delta rate of +0.42 m/hr.',
          'Road access via NH-66 sub-link is fully submerged (depth 1.8m). Inflatable boat mandatory.',
          'High vulnerability: 3 toddlers and 2 senior citizens identified by thermal camera.',
          'UAV Eagle-1 can drop flotation vests and acoustic beacons in 4.2 minutes.'
        ],
        urgencyFormulaScore: 97.4,
        escalationWarning: 'Flood crest predicted at 13:45 IST; rescue window is under 35 minutes.',
        estimatedTimeSavingMins: 24,
        routeSafetyConfidence: 94.8
      },
      status: 'proposed'
    }
  },
  {
    id: 'INC-MNG-002',
    title: 'Industrial Fire & Chemical Vapour Threat',
    type: 'fire',
    location: {
      lat: 12.9512,
      lng: 74.8021,
      address: 'Baikampady Industrial Estate, Sector B',
      sector: 'Sector Alpha-2'
    },
    reportedAt: '24 mins ago',
    severity: 88,
    priority: 'P1_CRITICAL',
    status: 'awaiting_approval',
    victimCount: {
      estimated: 8,
      injured: 3,
      trapped: 5
    },
    vulnerabilityScore: 82,
    escalationRisk: 'rapid',
    aiAnalysis: {
      confidenceScore: 94.8,
      damagePercentage: 74,
      detectedObjects: ['Class B hydrocarbon flames', 'LPG storage manifold nearby (60m)', 'Active toxic plume'],
      weatherConditions: {
        tempC: 29.1,
        rainfallMmPerHour: 2.1,
        windSpeedKmh: 34,
        visibilityM: 1400,
        hazardIndex: 'HIGH'
      },
      structuralRisk: 'Steel girder distortion detected. Thermal stress near flashpoint.',
      victimConfidence: 91.2
    },
    imageUrl: 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?auto=format&fit=crop&w=800&q=80',
    assignedResourceIds: [],
    recommendation: {
      id: 'REC-002',
      incidentId: 'INC-MNG-002',
      recommendedResourceIds: ['RES-FIRE-01', 'RES-AMB-02'],
      actionSummary: 'Deploy Foam Tender Unit FT-7 and Hazmat decontamination ambulance squad.',
      priorityRank: 2,
      explainability: {
        reasons: [
          'Class B chemical fire requires aqueous film-forming foam (AFFF), standard water jet ineffective.',
          'Wind blowing at 34 km/h towards adjacent residential colony (Kuloor). Perimeter foam containment critical.',
          'Industrial gas sensor indicates elevated volatile organic hydrocarbon ppm.'
        ],
        urgencyFormulaScore: 89.1,
        escalationWarning: 'Blast radius expansion possible if cylinder bank reaches 140°C.',
        estimatedTimeSavingMins: 18,
        routeSafetyConfidence: 91.0
      },
      status: 'proposed'
    }
  },
  {
    id: 'INC-MNG-003',
    title: 'Ghat Landslide & Multi-Vehicle Blockade',
    type: 'landslide',
    location: {
      lat: 12.9056,
      lng: 74.9124,
      address: 'Gurupura Ghat Corridor, NH-169',
      sector: 'Sector Echo-1'
    },
    reportedAt: '41 mins ago',
    severity: 76,
    priority: 'P2_HIGH',
    status: 'dispatched',
    victimCount: {
      estimated: 7,
      injured: 2,
      trapped: 3
    },
    vulnerabilityScore: 68,
    escalationRisk: 'moderate',
    aiAnalysis: {
      confidenceScore: 91.5,
      damagePercentage: 62,
      detectedObjects: ['Mudslide mass 450 metric tons', 'Passenger bus partially buried', 'Fallen teak trees'],
      weatherConditions: {
        tempC: 24.8,
        rainfallMmPerHour: 44.0,
        windSpeedKmh: 28,
        visibilityM: 600,
        hazardIndex: 'HIGH'
      },
      structuralRisk: 'Slope soil moisture saturation 98%; secondary mudflow probability 74%.',
      victimConfidence: 88.0
    },
    imageUrl: 'https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?auto=format&fit=crop&w=800&q=80',
    assignedResourceIds: ['RES-RECON-01'],
    recommendation: {
      id: 'REC-003',
      incidentId: 'INC-MNG-003',
      recommendedResourceIds: ['RES-RECON-01'],
      actionSummary: 'Deploy Heavy Earthmover & hydraulic spreaders via Kaikamba bypass.',
      priorityRank: 3,
      explainability: {
        reasons: [
          'Primary road blocked; reroute through Kaikamba-Bajpe peripheral link adds only 7.4 km.',
          'Bus driver radio confirmed 3 trapped passengers with non-critical blunt trauma.'
        ],
        urgencyFormulaScore: 78.5,
        escalationWarning: 'Secondary soil slump risk elevated during continuous torrential precipitation.',
        estimatedTimeSavingMins: 14,
        routeSafetyConfidence: 87.2
      },
      status: 'approved',
      approvedBy: 'CDR. R. SHETTY (COASTAL COMMAND)',
      approvedAt: '30 mins ago'
    }
  },
  {
    id: 'INC-MNG-004',
    title: 'Commercial Building Partial Collapse',
    type: 'collapse',
    location: {
      lat: 12.8682,
      lng: 74.8385,
      address: 'Bunder Old Port Fish Market Complex',
      sector: 'Sector Bravo-3'
    },
    reportedAt: '1 hr ago',
    severity: 72,
    priority: 'P2_HIGH',
    status: 'dispatched',
    victimCount: {
      estimated: 11,
      injured: 5,
      trapped: 2
    },
    vulnerabilityScore: 75,
    escalationRisk: 'moderate',
    aiAnalysis: {
      confidenceScore: 93.0,
      damagePercentage: 58,
      detectedObjects: ['Concrete slab fracture', 'Crushed storefronts', 'Live electrical conduit'],
      weatherConditions: {
        tempC: 27.2,
        rainfallMmPerHour: 18.0,
        windSpeedKmh: 22,
        visibilityM: 2000,
        hazardIndex: 'MODERATE'
      },
      structuralRisk: 'Secondary load-bearing pillar crack under progressive shear strain.',
      victimConfidence: 89.5
    },
    imageUrl: 'https://images.unsplash.com/photo-1516455590571-18256e5bb9ff?auto=format&fit=crop&w=800&q=80',
    assignedResourceIds: ['RES-AMB-01'],
    recommendation: {
      id: 'REC-004',
      incidentId: 'INC-MNG-004',
      recommendedResourceIds: ['RES-AMB-01'],
      actionSummary: 'Acoustic search sensors & rapid shoring crew dispatch.',
      priorityRank: 4,
      explainability: {
        reasons: [
          'Debris clearance requires canine or acoustic search before crane operation.',
          'Power grid breaker tripped at sub-station, eliminating electrocution hazard.'
        ],
        urgencyFormulaScore: 74.0,
        escalationWarning: 'Rubble stability declining with rain accumulation.',
        estimatedTimeSavingMins: 10,
        routeSafetyConfidence: 95.0
      },
      status: 'approved',
      approvedBy: 'SUPT. P. KUMAR',
      approvedAt: '50 mins ago'
    }
  },
  {
    id: 'INC-MNG-005',
    title: 'Cyclone Surge & Power Grid Gridlock',
    type: 'cyclone',
    location: {
      lat: 12.9348,
      lng: 74.7980,
      address: 'Panambur Coastal Fishermen Colony',
      sector: 'Sector Coastal-1'
    },
    reportedAt: '1.5 hrs ago',
    severity: 59,
    priority: 'P3_MODERATE',
    status: 'resolved',
    victimCount: {
      estimated: 28,
      injured: 1,
      trapped: 0
    },
    vulnerabilityScore: 61,
    escalationRisk: 'stable',
    aiAnalysis: {
      confidenceScore: 96.0,
      damagePercentage: 35,
      detectedObjects: ['Uprooted coconut trees (14)', 'Seawall splashover', 'Displaced catamaran boats'],
      weatherConditions: {
        tempC: 25.0,
        rainfallMmPerHour: 32.0,
        windSpeedKmh: 64,
        visibilityM: 1100,
        hazardIndex: 'HIGH'
      },
      structuralRisk: 'Temporary tin sheds blown off; permanent concrete shelters intact.',
      victimConfidence: 95.0
    },
    imageUrl: 'https://images.unsplash.com/photo-1527482797697-8795b05a13fe?auto=format&fit=crop&w=800&q=80',
    assignedResourceIds: [],
    recommendation: undefined
  }
];

export const INITIAL_RESOURCES: RescueResource[] = [
  {
    id: 'RES-BOAT-01',
    name: 'NDRF Gemini Alpha (Rapid Inflatable)',
    type: 'ndrf_boat',
    status: 'available',
    location: {
      lat: 12.8715,
      lng: 74.8450,
      baseStation: 'Mangaluru Coast Guard Base, Panambur'
    },
    speedKmH: 35,
    capacity: 12,
    crewCount: 5,
    equipment: ['Yamaha 40HP Outboard Engine', 'Life Jackets (25)', 'Thermal Throwlines', 'Submersible Radios'],
    fuelBatteryPercent: 94
  },
  {
    id: 'RES-UAV-01',
    name: 'Eagle-X Recon Drone (Thermal/LiDAR)',
    type: 'uav_recon',
    status: 'available',
    location: {
      lat: 12.8820,
      lng: 74.8510,
      baseStation: 'Kottara Chowki Emergency Operations Center'
    },
    speedKmH: 85,
    capacity: 2,
    crewCount: 2,
    equipment: ['FLIR Boson 640 Thermal Sensor', 'Payload Drop Winch (8kg)', '120dB Megaphone', 'Mesh Relay'],
    fuelBatteryPercent: 88
  },
  {
    id: 'RES-AMB-01',
    name: 'ALS-01 Mobile Trauma Unit',
    type: 'ambulance',
    status: 'en_route',
    location: {
      lat: 12.8650,
      lng: 74.8420,
      baseStation: 'Wenlock District Hospital'
    },
    speedKmH: 60,
    capacity: 3,
    crewCount: 4,
    equipment: ['Ventilator', 'Defibrillator', 'Whole Blood Storage', 'Telemetry Uplink to Trauma Center'],
    fuelBatteryPercent: 78,
    assignedIncidentId: 'INC-MNG-004'
  },
  {
    id: 'RES-FIRE-01',
    name: 'FT-07 Heavy Foam Tender',
    type: 'fire_unit',
    status: 'available',
    location: {
      lat: 12.9200,
      lng: 74.8250,
      baseStation: 'Kadri Fire & Rescue Headquarter'
    },
    speedKmH: 50,
    capacity: 6,
    crewCount: 6,
    equipment: ['4500L Aqueous Film Forming Foam (AFFF)', 'Dry Chemical Powder', 'Hydraulic Jaws of Life'],
    fuelBatteryPercent: 92
  },
  {
    id: 'RES-AMB-02',
    name: 'BLS-04 Rapid Paramedic Van',
    type: 'ambulance',
    status: 'available',
    location: {
      lat: 12.9150,
      lng: 74.8480,
      baseStation: 'AJ Hospital & Research Centre'
    },
    speedKmH: 65,
    capacity: 2,
    crewCount: 3,
    equipment: ['Spinal Boards', 'Oxygen Concentrator', 'Burn Triage Kits'],
    fuelBatteryPercent: 85
  },
  {
    id: 'RES-RECON-01',
    name: 'SDRF Quick Response Squad 3',
    type: 'medical_triage',
    status: 'on_scene',
    location: {
      lat: 12.9056,
      lng: 74.9124,
      baseStation: 'Bantwal Taluk Disaster Unit'
    },
    speedKmH: 45,
    capacity: 10,
    crewCount: 8,
    equipment: ['Pneumatic Jackhammers', 'Search Cam Fiber-optic probe', 'Chainsaws'],
    fuelBatteryPercent: 72,
    assignedIncidentId: 'INC-MNG-003'
  }
];

export const ROUTE_HAZARDS: RouteHazard[] = [
  {
    id: 'HAZ-001',
    type: 'flooded_road',
    name: 'NH-66 Jeppinamogaru Underpass Submergence',
    coordinates: [
      [12.8480, 74.8580],
      [12.8465, 74.8624],
      [12.8450, 74.8670]
    ],
    riskLevel: 'impassable',
    severity: 92
  },
  {
    id: 'HAZ-002',
    type: 'debris_blockage',
    name: 'Gurupura Ghat Rockfall Zone',
    coordinates: [
      [12.9040, 74.9100],
      [12.9056, 74.9124],
      [12.9070, 74.9150]
    ],
    riskLevel: 'impassable',
    severity: 85
  },
  {
    id: 'HAZ-003',
    type: 'fire_perimeter',
    name: 'Baikampady Chemical Thermal Hazard Zone (200m radius)',
    coordinates: [
      [12.9530, 74.8000],
      [12.9512, 74.8021],
      [12.9490, 74.8040]
    ],
    riskLevel: 'caution',
    severity: 78
  }
];
