import React from 'react';
import { Incident, NextMoveRecommendation, RescueResource } from '../../types';
import { 
  Sparkles, 
  CheckCircle, 
  AlertTriangle, 
  Clock, 
  Compass, 
  ShieldCheck, 
  ArrowRight,
  TrendingUp,
  Cpu,
  FileCheck
} from 'lucide-react';
import { soundManager } from '../../utils/audio';

interface NextMoveCardProps {
  incident: Incident | null;
  resources: RescueResource[];
  onOpenApprovalModal: (recommendation: NextMoveRecommendation) => void;
  onOpenRouteAnalysis: (incident: Incident) => void;
}

export const NextMoveCard: React.FC<NextMoveCardProps> = ({
  incident,
  resources,
  onOpenApprovalModal,
  onOpenRouteAnalysis
}) => {
  if (!incident || !incident.recommendation) {
    return (
      <div className="w-full glass-panel p-6 rounded-2xl border border-cyan-500/20 flex flex-col items-center justify-center text-center min-h-[300px]">
        <Cpu className="w-10 h-10 text-cyan-400/40 mb-3 animate-pulse" />
        <h4 className="font-mono text-sm uppercase text-slate-300 font-bold mb-1">
          Explainable AI Decision Engine (XAI)
        </h4>
        <p className="text-xs text-slate-400 max-w-sm">
          Select an emergency incident from the map or queue to inspect the multi-factor Next-Move recommendation and tactical approval protocol.
        </p>
      </div>
    );
  }

  const rec = incident.recommendation;
  const recommendedUnits = resources.filter(r => rec.recommendedResourceIds.includes(r.id));
  const isApproved = rec.status === 'approved';

  return (
    <div className="w-full glass-panel p-5 rounded-2xl border border-cyan-400/30 flex flex-col justify-between shadow-xl">
      
      {/* Top Header */}
      <div>
        <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-cyan-500/10 border border-cyan-400/40 flex items-center justify-center text-cyan-400">
              <Sparkles className="w-4 h-4 animate-spin-slow" />
            </div>
            <div>
              <span className="font-mono text-xs uppercase font-extrabold text-white tracking-wider flex items-center gap-2">
                AI NEXT-MOVE RECOMMENDATION
                <span className="text-[10px] text-cyan-400 font-normal">#{rec.id}</span>
              </span>
              <p className="text-[10px] font-mono text-slate-400">
                Cognitive Stage 5: Explainable Next-Move Synthesis
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-cyan-950 text-cyan-300 border border-cyan-500/40">
              RANK #{rec.priorityRank} PRIORITY
            </span>
            <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase border ${
              isApproved 
                ? 'bg-emerald-950 text-emerald-400 border-emerald-500/40' 
                : 'bg-amber-950 text-amber-400 border-amber-500/40'
            }`}>
              {rec.status}
            </span>
          </div>
        </div>

        {/* Action Summary Banner */}
        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-cyan-500/30 mb-4">
          <span className="text-[10px] font-mono uppercase text-cyan-400 font-bold block mb-1">
            Recommended Action Plan:
          </span>
          <p className="text-sm font-semibold text-white leading-relaxed">
            {rec.actionSummary}
          </p>
        </div>

        {/* Units to Dispatch */}
        <div className="mb-4">
          <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block mb-2 font-bold">
            Matched Rescue Resources ({recommendedUnits.length}):
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {recommendedUnits.map((u) => (
              <div key={u.id} className="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800 flex items-center justify-between text-xs font-mono">
                <div>
                  <span className="font-bold text-slate-200 block">{u.name}</span>
                  <span className="text-[10px] text-slate-400 capitalize">{u.type.replace('_', ' ')} • Speed: {u.speedKmH} km/h</span>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-emerald-400 font-bold block">{u.fuelBatteryPercent}% Batt/Fuel</span>
                  <span className="text-[9px] text-slate-400">{u.crewCount} Crew</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Explainability Breakdown (The "Why") */}
        <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 mb-4 space-y-2">
          <span className="text-[10px] font-mono uppercase text-slate-400 font-bold flex items-center gap-1.5">
            <CheckCircle className="w-3.5 h-3.5 text-cyan-400" />
            <span>Explainable Reasoning & Factors:</span>
          </span>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {rec.explainability.reasons.map((reason, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-cyan-400 font-mono font-bold">•</span>
                <span>{reason}</span>
              </li>
            ))}
          </ul>

          {/* Escalation Warning */}
          {rec.explainability.escalationWarning && (
            <div className="mt-2 pt-2 border-t border-slate-800 text-[11px] font-mono text-amber-300 flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
              <span>{rec.explainability.escalationWarning}</span>
            </div>
          )}
        </div>

        {/* Formula & Metrics Row */}
        <div className="grid grid-cols-3 gap-2 font-mono text-center text-xs mb-4">
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">
            <span className="text-[9px] text-slate-500 uppercase block">Urgency Score</span>
            <span className="font-bold text-cyan-400">{rec.explainability.urgencyFormulaScore} / 100</span>
          </div>

          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">
            <span className="text-[9px] text-slate-500 uppercase block">Time Saved</span>
            <span className="font-bold text-emerald-400">-{rec.explainability.estimatedTimeSavingMins} mins</span>
          </div>

          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">
            <span className="text-[9px] text-slate-500 uppercase block">Route Safety</span>
            <span className="font-bold text-blue-400">{rec.explainability.routeSafetyConfidence}%</span>
          </div>
        </div>
      </div>

      {/* Responder Decision Buttons (Step 8: Human Approval) */}
      <div className="pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3">
        <button
          onClick={() => {
            soundManager.playBlip(720, 0.08);
            onOpenRouteAnalysis(incident);
          }}
          className="text-xs font-mono text-slate-400 hover:text-cyan-400 flex items-center gap-1 transition-colors"
        >
          <Compass className="w-3.5 h-3.5 text-cyan-400" />
          <span>View Safe Corridor Route</span>
        </button>

        {isApproved ? (
          <div className="flex items-center gap-2 text-xs font-mono text-emerald-400 font-bold bg-emerald-950/80 px-3 py-1.5 rounded-lg border border-emerald-500/40">
            <FileCheck className="w-4 h-4 text-emerald-400" />
            <span>DISPATCH APPROVED BY {rec.approvedBy}</span>
          </div>
        ) : (
          <button
            onClick={() => {
              soundManager.playBlip(920, 0.1);
              onOpenApprovalModal(rec);
            }}
            className="px-5 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 shadow-lg shadow-emerald-500/20 hover:scale-105 active:scale-95 transition-all"
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Review & Authorize Dispatch</span>
          </button>
        )}
      </div>

    </div>
  );
};

