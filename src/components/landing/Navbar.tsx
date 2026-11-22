import React, { useState } from 'react';
import { ShieldAlert, Volume2, VolumeX, Terminal, Cpu, ArrowUpRight } from 'lucide-react';
import { soundManager } from '../../utils/audio';

interface NavbarProps {
  onOpenDashboard: () => void;
  activeTab: 'landing' | 'dashboard';
  setActiveTab: (tab: 'landing' | 'dashboard') => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpenDashboard, activeTab, setActiveTab }) => {
  const [muted, setMuted] = useState(soundManager.getMuted());

  const handleToggleAudio = () => {
    const isMuted = soundManager.toggleMute();
    setMuted(isMuted);
    if (!isMuted) {
      soundManager.playBlip(720, 0.1);
    }
  };

  return (
    <header className="fixed top-0 left-0 w-full z-50 px-4 lg:px-8 py-3.5 glass-panel border-b border-cyan-500/20">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand */}
        <div 
          className="flex items-center gap-3 cursor-pointer group"
          onClick={() => {
            setActiveTab('landing');
            soundManager.playBlip(600, 0.08);
          }}
        >
          <div className="relative w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500/20 to-red-500/20 border border-cyan-400/40 flex items-center justify-center glow-cyan group-hover:border-cyan-300 transition-all">
            <ShieldAlert className="w-5 h-5 text-cyan-400 group-hover:text-cyan-300 animate-pulse" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-red-500 rounded-full animate-ping" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold tracking-wider text-lg text-white font-mono group-hover:text-cyan-400 transition-colors">
                RESQ<span className="text-cyan-400">GRID</span>
              </span>
              <span className="hidden sm:inline-block px-1.5 py-0.5 rounded text-[10px] font-mono font-semibold bg-cyan-950/80 text-cyan-400 border border-cyan-500/30">
                v2.4-AI
              </span>
            </div>
            <p className="text-[10px] text-slate-400 hidden sm:block tracking-tight">
              AI-Powered Disaster Response Intelligence & Optimization
            </p>
          </div>
        </div>

        {/* Center Nav items */}
        <nav className="hidden md:flex items-center gap-1 bg-slate-900/60 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => {
              setActiveTab('landing');
              soundManager.playBlip();
            }}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
              activeTab === 'landing'
                ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            Overview & 3D Experience
          </button>
          <a
            href="#workflow"
            onClick={() => soundManager.playBlip()}
            className="px-3 py-1.5 rounded-md text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all"
          >
            9-Stage AI Workflow
          </a>
          <a
            href="#architecture"
            onClick={() => soundManager.playBlip()}
            className="px-3 py-1.5 rounded-md text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all"
          >
            System Architecture
          </a>
          <a
            href="#credits"
            onClick={() => soundManager.playBlip()}
            className="px-3 py-1.5 rounded-md text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all"
          >
            VTU Synopsis Team
          </a>
        </nav>

        {/* Right CTA / Controls */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleToggleAudio}
            className="p-2 rounded-lg bg-slate-900/70 border border-slate-700/60 text-slate-400 hover:text-cyan-400 transition-colors"
            title={muted ? 'Unmute tactical audio' : 'Mute audio'}
          >
            {muted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4 text-cyan-400 animate-pulse" />}
          </button>

          <button
            onClick={() => {
              soundManager.playApprovedChime();
              onOpenDashboard();
            }}
            className="relative group overflow-hidden px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-bold text-xs uppercase tracking-wider flex items-center gap-2 shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40 hover:scale-[1.02] transition-all"
          >
            <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
            <Terminal className="w-4 h-4" />
            <span>Launch Command HUD</span>
            <ArrowUpRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
          </button>
        </div>

      </div>
    </header>
  );
};

