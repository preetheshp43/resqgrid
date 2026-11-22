import React from 'react';
import { RescueResource } from '../../types';
import { Truck, BatteryCharging, Radio, Users, CheckCircle2, AlertCircle } from 'lucide-react';
import { soundManager } from '../../utils/audio';

interface ResourceFleetProps {
  resources: RescueResource[];
  onTriggerUnitAction?: (resource: RescueResource) => void;
}

export const ResourceFleet: React.FC<ResourceFleetProps> = ({ resources, onTriggerUnitAction }) => {
  return (
    <div className="w-full glass-panel rounded-2xl border border-cyan-500/20 p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Truck className="w-4 h-4 text-cyan-400" />
          <h3 className="font-mono text-xs uppercase tracking-wider font-bold text-white">
            Rescue Fleet Readiness ({resources.length} Units Active)
          </h3>
        </div>
        <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30">
          Optimization Matrix Ready
        </span>
      </div>

      {/* Resources Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {resources.map((res) => {
          const isAvail = res.status === 'available';
          const isEnRoute = res.status === 'en_route';
          const isOnScene = res.status === 'on_scene';

          return (
            <div 
              key={res.id}
              className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[10px] font-mono font-bold text-cyan-400 bg-cyan-950/60 px-1.5 py-0.5 rounded border border-cyan-500/30">
                    {res.id}
                  </span>
                  <span className={`text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded-full ${
                    isAvail 
                      ? 'bg-emerald-950/80 text-emerald-400 border border-emerald-500/40' 
                      : isEnRoute
                      ? 'bg-blue-950/80 text-blue-400 border border-blue-500/40'
                      : 'bg-amber-950/80 text-amber-400 border border-amber-500/40'
                  }`}>
                    {res.status.replace('_', ' ')}
                  </span>
                </div>

                <h4 className="text-xs font-bold text-white mb-1">{res.name}</h4>
                <p className="text-[10px] text-slate-400 font-mono mb-2">Base: {res.location.baseStation}</p>
                
                {/* Equipment Badges */}
                <div className="flex flex-wrap gap-1 mb-2">
                  {res.equipment.slice(0, 2).map((eq, idx) => (
                    <span key={idx} className="text-[9px] bg-slate-950 text-slate-300 px-1.5 py-0.5 rounded border border-slate-800">
                      {eq}
                    </span>
                  ))}
                  {res.equipment.length > 2 && (
                    <span className="text-[9px] text-slate-500">+{res.equipment.length - 2} more</span>
                  )}
                </div>
              </div>

              {/* Bottom Fuel & Crew Row */}
              <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-[10px] font-mono">
                <span className="text-slate-400 flex items-center gap-1">
                  <Users className="w-3 h-3 text-cyan-400" />
                  Crew: {res.crewCount} | Cap: {res.capacity}
                </span>

                <span className="text-emerald-400 font-bold flex items-center gap-1">
                  <BatteryCharging className="w-3 h-3" />
                  {res.fuelBatteryPercent}%
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

