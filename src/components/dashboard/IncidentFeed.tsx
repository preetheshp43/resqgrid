import React, { useState } from 'react';
import { Incident, PriorityLevel, DisasterType } from '../../types';
import { 
  AlertCircle, 
  Search, 
  Filter, 
  Users, 
  TrendingUp, 
  Clock, 
  ShieldCheck, 
  Activity,
  Flame,
  Waves,
  Mountain,
  Home,
  Wind
} from 'lucide-react';
import { soundManager } from '../../utils/audio';

interface IncidentFeedProps {
  incidents: Incident[];
  selectedIncident: Incident | null;
  onSelectIncident: (inc: Incident) => void;
}

export const IncidentFeed: React.FC<IncidentFeedProps> = ({
  incidents,
  selectedIncident,
  onSelectIncident
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [priorityFilter, setPriorityFilter] = useState<string>('ALL');
  const [typeFilter, setTypeFilter] = useState<string>('ALL');

  const filteredIncidents = incidents.filter(inc => {
    const matchesSearch = inc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          inc.location.address.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          inc.id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesPriority = priorityFilter === 'ALL' || inc.priority === priorityFilter;
    const matchesType = typeFilter === 'ALL' || inc.type === typeFilter;
    return matchesSearch && matchesPriority && matchesType;
  });

  const getDisasterIcon = (type: DisasterType) => {
    switch (type) {
      case 'flood': return <Waves className="w-4 h-4 text-cyan-400" />;
      case 'fire': return <Flame className="w-4 h-4 text-red-500" />;
      case 'landslide': return <Mountain className="w-4 h-4 text-amber-500" />;
      case 'collapse': return <Home className="w-4 h-4 text-orange-400" />;
      case 'cyclone': return <Wind className="w-4 h-4 text-blue-400" />;
      default: return <AlertCircle className="w-4 h-4 text-slate-400" />;
    }
  };

  const getPriorityBadge = (priority: PriorityLevel) => {
    switch (priority) {
      case 'P1_CRITICAL':
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-red-950 text-red-400 border border-red-500/40">P1 CRITICAL</span>;
      case 'P2_HIGH':
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-950 text-amber-400 border border-amber-500/40">P2 HIGH</span>;
      case 'P3_MODERATE':
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-950 text-cyan-400 border border-cyan-500/40">P3 MODERATE</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono text-slate-400">P4 LOW</span>;
    }
  };

  return (
    <div className="w-full h-full flex flex-col glass-panel rounded-2xl border border-cyan-500/20 overflow-hidden">
      
      {/* Header & Search */}
      <div className="p-4 border-b border-slate-800 bg-[#070b14]/70">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-cyan-400" />
            <h3 className="font-mono text-xs uppercase tracking-wider font-bold text-white">
              Incident Priority Queue ({filteredIncidents.length})
            </h3>
          </div>
          <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-500/30">
            AI Triage Sync
          </span>
        </div>

        {/* Search Input */}
        <div className="relative mb-3">
          <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search sector, location, or incident ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-900/90 border border-slate-700/80 rounded-lg pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
          />
        </div>

        {/* Priority Filter Tabs */}
        <div className="flex items-center gap-1.5 text-[11px] font-mono">
          {['ALL', 'P1_CRITICAL', 'P2_HIGH', 'P3_MODERATE'].map((p) => (
            <button
              key={p}
              onClick={() => {
                setPriorityFilter(p);
                soundManager.playBlip(650, 0.05);
              }}
              className={`px-2 py-1 rounded-md transition-all ${
                priorityFilter === p
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/40 font-bold'
                  : 'text-slate-400 hover:text-white bg-slate-900/60'
              }`}
            >
              {p === 'ALL' ? 'ALL' : p.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Incidents List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2.5">
        {filteredIncidents.length === 0 ? (
          <div className="py-12 text-center text-xs font-mono text-slate-500">
            No emergency reports match the selected filters.
          </div>
        ) : (
          filteredIncidents.map((inc) => {
            const isSelected = selectedIncident?.id === inc.id;
            return (
              <div
                key={inc.id}
                onClick={() => {
                  soundManager.playBlip(780, 0.06);
                  onSelectIncident(inc);
                }}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-cyan-950/40 border-cyan-400 shadow-md shadow-cyan-500/15'
                    : 'bg-slate-900/50 border-slate-800/80 hover:border-slate-700 hover:bg-slate-900/80'
                }`}
              >
                {/* Top Row: Type & Priority & Time */}
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {getDisasterIcon(inc.type)}
                    <span className="font-mono text-xs font-bold text-white">{inc.id}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono text-slate-500 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {inc.reportedAt}
                    </span>
                    {getPriorityBadge(inc.priority)}
                  </div>
                </div>

                {/* Title & Location */}
                <h4 className="text-sm font-semibold text-slate-100 mb-1 leading-snug">
                  {inc.title}
                </h4>
                <p className="text-xs text-slate-400 mb-2.5 font-mono">
                  {inc.location.address} • {inc.location.sector}
                </p>

                {/* Metrics Pill Grid */}
                <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800/80 font-mono text-[11px]">
                  <div>
                    <span className="text-slate-500 block text-[9px] uppercase">Trapped</span>
                    <span className="font-bold text-red-400 flex items-center gap-1">
                      <Users className="w-3 h-3" />
                      {inc.victimCount.trapped} / {inc.victimCount.estimated}
                    </span>
                  </div>

                  <div>
                    <span className="text-slate-500 block text-[9px] uppercase">Severity</span>
                    <span className="font-bold text-amber-400">
                      {inc.severity}%
                    </span>
                  </div>

                  <div>
                    <span className="text-slate-500 block text-[9px] uppercase">AI Confidence</span>
                    <span className="font-bold text-cyan-400">
                      {inc.aiAnalysis.confidenceScore}%
                    </span>
                  </div>
                </div>

                {/* Status Indicator Bar */}
                <div className="mt-2.5 flex items-center justify-between text-[10px] font-mono text-slate-400">
                  <span className="capitalize">
                    Status: <strong className={inc.status === 'dispatched' ? 'text-emerald-400' : 'text-amber-400'}>{inc.status.replace('_', ' ')}</strong>
                  </span>
                  {inc.assignedResourceIds.length > 0 && (
                    <span className="text-cyan-300 font-semibold">
                      Units Deployed: {inc.assignedResourceIds.length}
                    </span>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>

    </div>
  );
};

