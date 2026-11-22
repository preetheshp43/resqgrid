import React, { useState } from 'react';
import { Incident, DisasterType, PriorityLevel } from '../../types';
import { 
  FilePlus, 
  X, 
  Camera, 
  MapPin, 
  BrainCircuit, 
  Sparkles, 
  CheckCircle, 
  AlertTriangle 
} from 'lucide-react';
import { soundManager } from '../../utils/audio';

interface IncidentIntakeModalProps {
  onClose: () => void;
  onSubmitIncident: (newInc: Incident) => void;
}

export const IncidentIntakeModal: React.FC<IncidentIntakeModalProps> = ({
  onClose,
  onSubmitIncident
}) => {
  const [title, setTitle] = useState('');
  const [disasterType, setDisasterType] = useState<DisasterType>('flood');
  const [address, setAddress] = useState('Ullal Coastal Colony, South Mangaluru');
  const [lat, setLat] = useState('12.8050');
  const [lng, setLng] = useState('74.8520');
  const [estimatedVictims, setEstimatedVictims] = useState<number>(12);
  const [trappedVictims, setTrappedVictims] = useState<number>(4);
  const [imageUrl, setImageUrl] = useState('https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80');
  
  // Simulated AI CV Pipeline State
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [cvCompleted, setCvCompleted] = useState(false);
  const [detectedDamage, setDetectedDamage] = useState(82);
  const [confidence, setConfidence] = useState(97.2);

  const handleSimulateCV = () => {
    setIsAnalyzing(true);
    soundManager.playTelemetrySweep();
    setTimeout(() => {
      setIsAnalyzing(false);
      setCvCompleted(true);
      setDetectedDamage(Math.floor(75 + Math.random() * 20));
      setConfidence(parseFloat((94 + Math.random() * 5).toFixed(1)));
      soundManager.playApprovedChime();
    }, 1200);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    soundManager.playApprovedChime();

    const priority: PriorityLevel = 
      trappedVictims > 3 || detectedDamage > 75 
        ? 'P1_CRITICAL' 
        : estimatedVictims > 5 
        ? 'P2_HIGH' 
        : 'P3_MODERATE';

    const newInc: Incident = {
      id: `INC-MNG-${Math.floor(100 + Math.random() * 900)}`,
      title: title || `${disasterType.toUpperCase()} Emergency at ${address}`,
      type: disasterType,
      location: {
        lat: parseFloat(lat) || 12.85,
        lng: parseFloat(lng) || 74.85,
        address: address,
        sector: 'Sector Urban-SOS'
      },
      reportedAt: 'Just now',
      severity: detectedDamage,
      priority: priority,
      status: 'awaiting_approval',
      victimCount: {
        estimated: estimatedVictims,
        injured: Math.max(1, Math.floor(estimatedVictims * 0.3)),
        trapped: trappedVictims
      },
      vulnerabilityScore: 84,
      escalationRisk: priority === 'P1_CRITICAL' ? 'rapid' : 'moderate',
      aiAnalysis: {
        confidenceScore: confidence,
        damagePercentage: detectedDamage,
        detectedObjects: ['Water level 1.6m', 'Trapped civilians on rooftop (4)', 'Downed transformer nearby'],
        weatherConditions: {
          tempC: 27,
          rainfallMmPerHour: 55,
          windSpeedKmh: 42,
          visibilityM: 900,
          hazardIndex: 'HIGH'
        },
        structuralRisk: 'High hydrostatic wall pressure; critical evacuation window < 40m.',
        victimConfidence: 94.8
      },
      imageUrl: imageUrl,
      assignedResourceIds: [],
      recommendation: {
        id: `REC-${Math.floor(100 + Math.random() * 900)}`,
        incidentId: `INC-MNG-TEMP`,
        recommendedResourceIds: ['RES-BOAT-01', 'RES-UAV-01'],
        actionSummary: `High-priority dispatch of NDRF Inflatable Craft and Thermal Recon Drone to ${address}.`,
        priorityRank: 1,
        explainability: {
          reasons: [
            `${trappedVictims} trapped victims verified via Computer Vision object detection.`,
            `Flood escalation model indicates +0.35m rise over next 30 minutes.`,
            `Direct vehicular road is impassable; water transport is mandatory.`
          ],
          urgencyFormulaScore: 92.4,
          escalationWarning: 'Water level threshold approaching electrical substation line.',
          estimatedTimeSavingMins: 21,
          routeSafetyConfidence: 93.5
        },
        status: 'proposed'
      }
    };

    onSubmitIncident(newInc);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="relative w-full max-w-2xl bg-[#090e1d] border border-cyan-400/40 rounded-2xl p-6 sm:p-8 shadow-2xl glow-cyan text-slate-100 max-h-[90vh] overflow-y-auto">
        
        {/* Close Button */}
        <button
          onClick={() => {
            soundManager.playBlip(500, 0.05);
            onClose();
          }}
          className="absolute top-4 right-4 p-2 rounded-lg bg-slate-900 border border-slate-700 text-slate-400 hover:text-white"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-red-500/10 border border-red-500/40 flex items-center justify-center text-red-400">
            <FilePlus className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] font-mono uppercase text-red-400 font-bold">
              Cognitive Stage 1 & 2 • Input Collection & AI Vision Triage
            </span>
            <h3 className="text-xl font-bold text-white font-mono">
              Citizen / Agency Emergency Incident Intake
            </h3>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          
          {/* Disaster Type & Title */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-mono uppercase text-slate-300 font-bold mb-1.5">
                Disaster Classification
              </label>
              <select
                value={disasterType}
                onChange={(e) => setDisasterType(e.target.value as DisasterType)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2 text-xs font-mono text-white focus:outline-none focus:border-cyan-400"
              >
                <option value="flood">Flood & Submergence</option>
                <option value="fire">Fire & Hazard Flare</option>
                <option value="landslide">Landslide & Mudflow</option>
                <option value="collapse">Structural Collapse</option>
                <option value="cyclone">Cyclone & Gale Surge</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-mono uppercase text-slate-300 font-bold mb-1.5">
                Incident Summary / Title
              </label>
              <input
                type="text"
                placeholder="e.g. Flooded Residential Block"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2 text-xs text-white focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          {/* Location & GPS */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="sm:col-span-1">
              <label className="block text-xs font-mono uppercase text-slate-300 font-bold mb-1.5">
                Location Address
              </label>
              <input
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-xs font-mono uppercase text-slate-300 font-bold mb-1.5">
                Latitude (GPS)
              </label>
              <input
                type="text"
                value={lat}
                onChange={(e) => setLat(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs font-mono text-white focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-xs font-mono uppercase text-slate-300 font-bold mb-1.5">
                Longitude (GPS)
              </label>
              <input
                type="text"
                value={lng}
                onChange={(e) => setLng(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs font-mono text-white focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          {/* Victims Count */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-mono uppercase text-slate-300 font-bold mb-1.5">
                Estimated Total Victims
              </label>
              <input
                type="number"
                min="1"
                max="500"
                value={estimatedVictims}
                onChange={(e) => setEstimatedVictims(parseInt(e.target.value) || 1)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2 text-xs font-mono text-white focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-xs font-mono uppercase text-slate-300 font-bold mb-1.5">
                Trapped / High Jeopardy Victims
              </label>
              <input
                type="number"
                min="0"
                max="500"
                value={trappedVictims}
                onChange={(e) => setTrappedVictims(parseInt(e.target.value) || 0)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2 text-xs font-mono text-white focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          {/* Computer Vision Simulation Box */}
          <div className="p-4 rounded-xl bg-slate-950/80 border border-cyan-500/30">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-mono uppercase font-bold text-cyan-400 flex items-center gap-1.5">
                <BrainCircuit className="w-4 h-4" />
                <span>AI Computer Vision Damage Classifier</span>
              </span>
              <button
                type="button"
                onClick={handleSimulateCV}
                disabled={isAnalyzing}
                className="px-3 py-1 rounded-md bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 text-[11px] font-mono hover:bg-cyan-500/30 flex items-center gap-1.5 transition-all"
              >
                <Sparkles className="w-3 h-3 text-cyan-400" />
                <span>{isAnalyzing ? 'Extracting Features...' : 'Run CV Pipeline'}</span>
              </button>
            </div>

            {cvCompleted ? (
              <div className="grid grid-cols-3 gap-2 font-mono text-xs text-center">
                <div className="p-2 rounded bg-slate-900/80 border border-slate-800">
                  <span className="text-[9px] text-slate-500 block">Structural Damage</span>
                  <span className="font-bold text-red-400">{detectedDamage}%</span>
                </div>
                <div className="p-2 rounded bg-slate-900/80 border border-slate-800">
                  <span className="text-[9px] text-slate-500 block">CV Confidence</span>
                  <span className="font-bold text-emerald-400">{confidence}%</span>
                </div>
                <div className="p-2 rounded bg-slate-900/80 border border-slate-800">
                  <span className="text-[9px] text-slate-500 block">Detected Triage</span>
                  <span className="font-bold text-amber-400">P1 Immediate</span>
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-400">
                Click "Run CV Pipeline" to simulate convolutional object extraction and structural damage grading from imagery.
              </p>
            )}
          </div>

          {/* Submit Actions */}
          <div className="pt-4 border-t border-slate-800 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 text-slate-300 text-xs font-mono hover:text-white"
            >
              Cancel
            </button>

            <button
              type="submit"
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 shadow-lg shadow-red-600/30 hover:scale-105 transition-all"
            >
              <FilePlus className="w-4 h-4" />
              <span>Ingest Incident into Live Triage</span>
            </button>
          </div>

        </form>

      </div>
    </div>
  );
};

