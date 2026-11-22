import React from 'react';
import { Hero3DScene } from '../3d/Hero3DScene';
import { soundManager } from '../../utils/audio';
import { 
  ShieldAlert, 
  Cpu, 
  MapPin, 
  Navigation, 
  ChevronDown, 
  Flame, 
  Waves, 
  Zap,
  Activity
} from 'lucide-react';

interface HeroSectionProps {
  onOpenDashboard: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({ onOpenDashboard }) => {
  return (
    <section className="relative min-h-screen w-full flex items-center justify-center overflow-hidden pt-20 pb-16">
      {/* 3D WebGL Background Scene */}
      <div className="absolute inset-0 z-0 opacity-85">
        <Hero3DScene />
      </div>

      {/* Cyber Grid Background Matrix */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(0,240,255,0.15),rgba(255,255,255,0))] pointer-events-none" />
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#050811]/70 to-[#050811] pointer-events-none" />

      {/* Foreground Hero Content */}
      <div className="relative z-10 max-w-6xl mx-auto px-4 lg:px-8 text-center flex flex-col items-center">
        
        {/* VTU Capstone Badge */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-950/70 border border-cyan-400/40 text-cyan-300 text-xs font-mono mb-6 backdrop-blur-md shadow-lg shadow-cyan-500/10">
          <Activity className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
          <span>VTU BE CSE(AIML) CAPSTONE PROJECT • AJIET MANGALURU</span>
        </div>

        {/* Main Title */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white mb-6 uppercase">
          Autonomous <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-blue-500 text-glow-cyan">Disaster Response</span>
          <br />
          <span className="text-2xl sm:text-4xl lg:text-5xl font-mono text-slate-300 tracking-normal font-bold">
            Intelligence & Resource Optimization
          </span>
        </h1>

        {/* Subtitle */}
        <p className="max-w-3xl mx-auto text-base sm:text-lg text-slate-300/90 leading-relaxed mb-10 font-sans">
          A real-time cognitive command system that ingests multi-modal disaster reports, synthesizes Computer Vision & NLP damage analytics, prioritizes crisis sectors, optimizes rescue fleets, and delivers explainable next-move action plans with human commander oversight.
        </p>

        {/* CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-4 mb-16">
          <button
            onClick={() => {
              soundManager.playApprovedChime();
              onOpenDashboard();
            }}
            className="px-8 py-4 rounded-xl bg-gradient-to-r from-cyan-500 via-cyan-400 to-blue-600 text-slate-950 font-extrabold text-sm uppercase tracking-wider shadow-xl shadow-cyan-500/25 hover:shadow-cyan-500/50 hover:scale-105 active:scale-95 transition-all flex items-center gap-3"
          >
            <ShieldAlert className="w-5 h-5" />
            <span>Launch Tactical Command HUD</span>
          </button>

          <a
            href="#workflow"
            onClick={() => soundManager.playBlip(750, 0.1)}
            className="px-7 py-4 rounded-xl glass-card text-white hover:text-cyan-400 border border-slate-700 hover:border-cyan-500/40 text-sm font-semibold tracking-wide transition-all flex items-center gap-2 hover:bg-slate-900/80"
          >
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>Explore 9-Stage AI Pipeline</span>
          </a>
        </div>

        {/* Live System Metrics Bar */}
        <div className="w-full grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 rounded-2xl glass-panel border border-cyan-500/20 backdrop-blur-xl">
          <div className="flex flex-col items-center p-3 text-center border-r border-slate-800/80 last:border-0">
            <span className="font-mono text-2xl sm:text-3xl font-extrabold text-cyan-400 text-glow-cyan">&lt; 1.8s</span>
            <span className="text-xs text-slate-400 font-medium mt-1">Multi-modal AI Triage Latency</span>
          </div>

          <div className="flex flex-col items-center p-3 text-center border-r border-slate-800/80 last:border-0">
            <span className="font-mono text-2xl sm:text-3xl font-extrabold text-emerald-400 text-glow-cyan">98.6%</span>
            <span className="text-xs text-slate-400 font-medium mt-1">Resource Matching Efficiency</span>
          </div>

          <div className="flex flex-col items-center p-3 text-center border-r border-slate-800/80 last:border-0">
            <span className="font-mono text-2xl sm:text-3xl font-extrabold text-amber-400">Zero Hazard</span>
            <span className="text-xs text-slate-400 font-medium mt-1">Adaptive Route Clearance</span>
          </div>

          <div className="flex flex-col items-center p-3 text-center">
            <span className="font-mono text-2xl sm:text-3xl font-extrabold text-rose-500 text-glow-alert">100%</span>
            <span className="text-xs text-slate-400 font-medium mt-1">Human-in-the-Loop Control</span>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="mt-12 flex flex-col items-center gap-2 text-slate-500 animate-bounce">
          <span className="text-[11px] font-mono tracking-widest uppercase">Scroll To Explore System Architecture</span>
          <ChevronDown className="w-4 h-4 text-cyan-400" />
        </div>

      </div>
    </section>
  );
};

