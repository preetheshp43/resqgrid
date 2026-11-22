import React, { useState } from 'react';
import { NextMoveRecommendation, RescueResource } from '../../types';
import { 
  ShieldCheck, 
  X, 
  AlertTriangle, 
  CheckCircle, 
  Truck, 
  UserCheck, 
  FileText,
  Lock
} from 'lucide-react';
import { soundManager } from '../../utils/audio';

interface HumanApprovalModalProps {
  recommendation: NextMoveRecommendation | null;
  resources: RescueResource[];
  onClose: () => void;
  onApprove: (recId: string, commanderName: string, notes: string) => void;
}

export const HumanApprovalModal: React.FC<HumanApprovalModalProps> = ({
  recommendation,
  resources,
  onClose,
  onApprove
}) => {
  if (!recommendation) return null;

  const [commanderName, setCommanderName] = useState('CDR. PREETHESH (CHIEF OF OPERATIONS)');
  const [commanderNotes, setCommanderNotes] = useState(
    'Tactical dispatch approved. Prioritize infant extraction and establish thermal beacon perimeter immediately.'
  );

  const matchedUnits = resources.filter(r => recommendation.recommendedResourceIds.includes(r.id));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    soundManager.playApprovedChime();
    onApprove(recommendation.id, commanderName, commanderNotes);
    onClose();
  };

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
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] font-mono uppercase text-emerald-400 font-bold">
              Cognitive Stage 8 • Human-in-the-Loop Protocol
            </span>
            <h3 className="text-xl font-bold text-white font-mono">
              Authorize AI Tactical Recommendation #{recommendation.id}
            </h3>
          </div>
        </div>

        {/* Synopsis Compliance Notice */}
        <div className="p-3 rounded-xl bg-cyan-950/40 border border-cyan-500/30 text-xs text-slate-300 font-mono mb-6 flex items-start gap-2.5">
          <Lock className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
          <span>
            <strong>Human Approval Mandate:</strong> As specified in the VTU BE(AIML) synopsis, autonomous recommendation engines must keep final execution decisions under the cryptographic control of authorized human incident commanders.
          </span>
        </div>

        {/* Action Summary */}
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 mb-6 space-y-2">
          <span className="text-[10px] font-mono uppercase text-slate-400 font-bold block">
            Target Operation:
          </span>
          <p className="text-sm font-semibold text-white">
            {recommendation.actionSummary}
          </p>

          <div className="pt-2 border-t border-slate-800 flex flex-wrap gap-2">
            {matchedUnits.map(u => (
              <span key={u.id} className="text-xs font-mono bg-slate-950 text-cyan-300 px-2.5 py-1 rounded border border-cyan-500/30">
                {u.name} ({u.type.replace('_', ' ')})
              </span>
            ))}
          </div>
        </div>

        {/* Approval Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-mono uppercase text-slate-300 font-bold mb-1.5">
              Authorized Incident Commander Name / USN
            </label>
            <input
              type="text"
              required
              value={commanderName}
              onChange={(e) => setCommanderName(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2 text-xs font-mono text-white focus:outline-none focus:border-cyan-400"
            />
          </div>

          <div>
            <label className="block text-xs font-mono uppercase text-slate-300 font-bold mb-1.5">
              Operational Directives & Field Notes
            </label>
            <textarea
              rows={3}
              value={commanderNotes}
              onChange={(e) => setCommanderNotes(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2 text-xs font-sans text-white focus:outline-none focus:border-cyan-400"
            />
          </div>

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
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 shadow-lg shadow-emerald-500/25 hover:scale-105 transition-all"
            >
              <UserCheck className="w-4 h-4" />
              <span>Confirm & Dispatch Units</span>
            </button>
          </div>
        </form>

      </div>
    </div>
  );
};

