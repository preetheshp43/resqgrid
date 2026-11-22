import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, 
  Volume2, 
  VolumeX, 
  PlusCircle, 
  RotateCcw, 
  ArrowLeft, 
  Radio, 
  Clock, 
  Sparkles,
  Zap
} from 'lucide-react';
import { soundManager } from '../../utils/audio';

interface TacticalNavbarProps {
  onBackToLanding: () => void;
  onOpenIntakeModal: () => void;
  onTriggerAutoOptimize: () => void;
  onResetSimulation: () => void;
  activeIncidentsCount: number;
  criticalP1Count: number;
}

export const TacticalNavbar: React.FC<TacticalNavbarProps> = ({
  onBackToLanding,
  onOpenIntakeModal,
  onTriggerAutoOptimize,
  onResetSimulation,
  activeIncidentsCount,
  criticalP1Count
}) => {
  const [muted, setMuted] = useState(soundManager.getMuted());
  const [currentTime, setCurrentTime] = useState<string>('');

  useEffect(() => {
    const updateClock = () => {
      const now = new Date();
      setCurrentTime(now.toLocaleTimeString('en-US', { hour12: false }) + ' IST');
    };
    updateClock();
    const interval = setInterval(updateClock, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleToggleAudio = () => {
    const isMuted = soundManager.toggleMute();
    setMuted(isMuted);
    if (!isMuted) soundManager.playBlip(750, 0.08);
  };

  return (
    <header className="w-full bg-[#070b14] border-b border-cyan-500/20 px-4 py-2.5 flex flex-wrap items-center justify-between gap-4 select-none">
      
      {/* Left: Brand & Return */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => {
            soundManager.playBlip();
            onBackToLanding();
          }}
          className="p-1.5 rounded-lg bg-slate-900 border border-slate-700/60 text-slate-400 hover:text-cyan-400 hover:border-cyan-500/40 transition-all flex items-center gap-1.5 text-xs font-mono"
          title="Return to 3D Experience"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">3D Overview</span>
        </button>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-red-950/80 border border-red-500/40 flex items-center justify-center glow-alert">
            <Radio className="w-4 h-4 text-red-400 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono font-extrabold text-sm text-white tracking-wider">
                RESQGRID <span className="text-cyan-400">COMMAND HUB</span>
              </span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-red-950 text-red-400 border border-red-500/40 animate-pulse">
                DEFCON 2 : ACTIVE DISASTER
              </span>
            </div>
            <div className="text-[10px] font-mono text-slate-400 hidden sm:block">
              SECTOR: COASTAL KARNATAKA (MANGALURU METRO) • OSM GIS SYNCHRONIZED
            </div>
          </div>
        </div>
      </div>

      {/* Center: Live Tactical Badges */}
      <div className="hidden xl:flex items-center gap-3 text-xs font-mono">
        <div className="flex items-center gap-2 px-3 py-1 rounded bg-slate-900/80 border border-slate-800">
          <Clock className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-slate-300 font-semibold">{currentTime}</span>
        </div>

        <div className="flex items-center gap-2 px-3 py-1 rounded bg-red-950/50 border border-red-500/30 text-red-300">
          <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
          <span>CRITICAL P1: <strong>{criticalP1Count}</strong></span>
        </div>

        <div className="flex items-center gap-2 px-3 py-1 rounded bg-cyan-950/50 border border-cyan-500/30 text-cyan-300">
          <span>ACTIVE INCIDENTS: <strong>{activeIncidentsCount}</strong></span>
        </div>
      </div>

      {/* Right: Quick Command Actions */}
      <div className="flex items-center gap-2.5">
        
        {/* Auto Optimize Button */}
        <button
          onClick={() => {
            soundManager.playTelemetrySweep();
            onTriggerAutoOptimize();
          }}
          className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-cyan-900/60 to-blue-900/60 border border-cyan-400/40 text-cyan-300 hover:text-white text-xs font-mono font-bold flex items-center gap-1.5 shadow-sm hover:shadow-cyan-500/20 transition-all"
        >
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span className="hidden sm:inline">AI Auto-Optimize Resources</span>
          <span className="sm:hidden">Optimize</span>
        </button>

        {/* Report New Incident Button */}
        <button
          onClick={() => {
            soundManager.playAlertSiren();
            onOpenIntakeModal();
          }}
          className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-red-600 to-rose-700 hover:from-red-500 hover:to-rose-600 text-white font-mono font-bold text-xs uppercase tracking-wider flex items-center gap-1.5 shadow-lg shadow-red-600/25 hover:scale-105 active:scale-95 transition-all"
        >
          <PlusCircle className="w-3.5 h-3.5" />
          <span>Report SOS Incident</span>
        </button>

        {/* Reset Simulation Button */}
        <button
          onClick={() => {
            soundManager.playBlip(500, 0.1);
            onResetSimulation();
          }}
          className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition-colors"
          title="Reset Simulation State"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>

        {/* Audio Mute Toggle */}
        <button
          onClick={handleToggleAudio}
          className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-cyan-400 transition-colors"
          title={muted ? 'Unmute tactical audio' : 'Mute tactical audio'}
        >
          {muted ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />}
        </button>

      </div>
    </header>
  );
};

