import React from 'react';
import { Incident } from '../../types';
import { Compass, X, AlertTriangle, CheckCircle, Navigation, ShieldAlert, ArrowRight } from 'lucide-react';
import { soundManager } from '../../utils/audio';

interface RouteAnalysisModalProps {
  incident: Incident | null;
  onClose: () => void;
}

export const RouteAnalysisModal: React.FC<RouteAnalysisModalProps> = ({ incident, onClose }) => {
  if (!incident) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="relative w-full max-w-2xl bg-[#090e1d] border border-cyan-400/40 rounded-2xl p-6 sm:p-8 shadow-2xl glow-cyan text-slate-100">
        
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
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/40 flex items-center justify-center text-cyan-400">
            <Compass className="w-6 h-6 animate-spin-slow" />
          </div>
          <div>
            <span className="text-[10px] font-mono uppercase text-cyan-400 font-bold">
              Cognitive Stage 6 • Hazard-Free Route Analysis
            </span>
            <h3 className="text-xl font-bold text-white font-mono">
              Safe Navigational Corridor: {incident.location.sector}
            </h3>
          </div>
        </div>

        {/* Route Comparison Card */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          
          {/* Primary Route (Hazard Blocked) */}
          <div className="p-4 rounded-xl bg-red-950/30 border border-red-500/40 space-y-2">
            <div className="flex items-center justify-between text-xs font-mono text-red-400 font-bold">
              <span>PRIMARY ARTERIAL ROUTE</span>
              <span className="px-2 py-0.5 rounded bg-red-950 text-red-300 border border-red-500/40">IMPASSABLE</span>
            </div>
            <p className="text-xs text-slate-300">
              NH-66 Highway Main Direct Corridor
            </p>
            <div className="pt-2 border-t border-red-500/20 text-[11px] font-mono text-red-300 space-y-1">
              <div className="flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5 text-red-400 shrink-0" />
                <span>Water depth exceeds 1.8m at underpass</span>
              </div>
              <div>Estimated Vehicle Loss Risk: <strong>96%</strong></div>
              <div>Travel ETA: <strong>BLOCKED (∞)</strong></div>
            </div>
          </div>

          {/* AI Computed Alternate Safe Route */}
          <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/40 space-y-2">
            <div className="flex items-center justify-between text-xs font-mono text-emerald-400 font-bold">
              <span>AI SAFE BYPASS CORRIDOR</span>
              <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-500/40">CLEAR (98.4%)</span>
            </div>
            <p className="text-xs text-slate-300">
              Peripheral Elevated Ring Road via Kuloor-Kaikamba
            </p>
            <div className="pt-2 border-t border-emerald-500/20 text-[11px] font-mono text-emerald-300 space-y-1">
              <div className="flex items-center gap-1.5">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Zero structural submergence</span>
              </div>
              <div>Added Distance: <strong>+3.2 km</strong></div>
              <div>Guaranteed Travel ETA: <strong>11.4 mins</strong></div>
            </div>
          </div>

        </div>

        {/* Tactical Reasoning */}
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-xs font-mono text-slate-300 mb-6 space-y-2">
          <span className="text-[10px] uppercase text-cyan-400 font-bold block">
            Algorithmic Route Optimization Notes:
          </span>
          <p>
            The A* routing heuristic dynamically added an infinite penalty cost to the flooded underpass node (Edge ID: NH66-S4). The peripheral elevated corridor bypasses all current flood crest forecasts and maintains a safety clearance margin of 350 meters from hazardous power transmission lines.
          </p>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end">
          <button
            onClick={() => {
              soundManager.playBlip(600, 0.05);
              onClose();
            }}
            className="px-5 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold font-mono text-xs uppercase tracking-wider transition-all"
          >
            Acknowledge Corridor Clearance
          </button>
        </div>

      </div>
    </div>
  );
};

