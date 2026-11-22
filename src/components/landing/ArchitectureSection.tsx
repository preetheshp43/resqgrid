import React from 'react';
import { 
  Cpu, 
  Database, 
  Map, 
  Server, 
  Eye, 
  GitBranch, 
  FileCode, 
  Network,
  Binary
} from 'lucide-react';

export const ArchitectureSection: React.FC = () => {
  return (
    <section id="architecture" className="relative py-24 px-4 lg:px-8 bg-[#050811] border-t border-slate-900">
      <div className="max-w-7xl mx-auto">
        
        {/* Title */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-400 text-xs font-mono mb-3">
            <Network className="w-3.5 h-3.5" />
            <span>SOFTWARE & HARDWARE SYSTEM SPECIFICATION</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight uppercase">
            Technical <span className="text-cyan-400 text-glow-cyan">Architecture</span>
          </h2>
          <p className="max-w-2xl mx-auto text-slate-400 text-sm sm:text-base mt-3">
            Engineered per the VTU BE(AIML) requirements: Python FastAPI, PyTorch Computer Vision, React + TypeScript, and OpenStreetMap GIS.
          </p>
        </div>

        {/* 3-Tier Layered Architecture Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          
          {/* Frontend Tier */}
          <div className="glass-panel p-6 rounded-2xl border border-cyan-500/20 flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-6">
                <FileCode className="w-6 h-6" />
              </div>
              <span className="text-xs font-mono text-cyan-400 font-semibold uppercase tracking-wider">CLIENT & GIS TIER</span>
              <h3 className="text-xl font-bold text-white mt-1 mb-3">React, TypeScript & 3D WebGL</h3>
              <p className="text-sm text-slate-300 leading-relaxed mb-4">
                Single-Page Application providing military-grade responsive HUD, 3D interactive holographic radar, GSAP scroll triggers, and Leaflet OpenStreetMap layers.
              </p>
            </div>
            <div className="pt-4 border-t border-slate-800 space-y-2 font-mono text-xs text-slate-400">
              <div className="flex justify-between"><span>Core:</span> <span className="text-slate-200">React 18 + TS</span></div>
              <div className="flex justify-between"><span>Styling:</span> <span className="text-slate-200">Tailwind CSS</span></div>
              <div className="flex justify-between"><span>3D Engine:</span> <span className="text-cyan-300">Three.js WebGL</span></div>
              <div className="flex justify-between"><span>Mapping:</span> <span className="text-slate-200">Leaflet / OSM GIS</span></div>
            </div>
          </div>

          {/* Backend & Optimization Tier */}
          <div className="glass-panel p-6 rounded-2xl border border-blue-500/20 flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-400 mb-6">
                <Server className="w-6 h-6" />
              </div>
              <span className="text-xs font-mono text-blue-400 font-semibold uppercase tracking-wider">INTELLIGENCE TIER</span>
              <h3 className="text-xl font-bold text-white mt-1 mb-3">FastAPI & Combinatorial Engine</h3>
              <p className="text-sm text-slate-300 leading-relaxed mb-4">
                High-throughput asynchronous Python microservice executing the Hungarian allocation algorithm, dynamic Dijkstra hazard routing, and Explainable AI generation.
              </p>
            </div>
            <div className="pt-4 border-t border-slate-800 space-y-2 font-mono text-xs text-slate-400">
              <div className="flex justify-between"><span>Framework:</span> <span className="text-slate-200">Python 3.11 / FastAPI</span></div>
              <div className="flex justify-between"><span>Optimization:</span> <span className="text-blue-300">SciPy / OR-Tools MILP</span></div>
              <div className="flex justify-between"><span>Routing:</span> <span className="text-slate-200">A* Hazard Penalty</span></div>
              <div className="flex justify-between"><span>Database:</span> <span className="text-slate-200">PostgreSQL / Supabase</span></div>
            </div>
          </div>

          {/* AI / CV Models Tier */}
          <div className="glass-panel p-6 rounded-2xl border border-purple-500/20 flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 mb-6">
                <Eye className="w-6 h-6" />
              </div>
              <span className="text-xs font-mono text-purple-400 font-semibold uppercase tracking-wider">PERCEPTION TIER</span>
              <h3 className="text-xl font-bold text-white mt-1 mb-3">Multi-Modal CV & NLP</h3>
              <p className="text-sm text-slate-300 leading-relaxed mb-4">
                Computer vision damage assessment pipelines, victim localization from drone feeds, and automated named entity extraction from civilian panic dispatches.
              </p>
            </div>
            <div className="pt-4 border-t border-slate-800 space-y-2 font-mono text-xs text-slate-400">
              <div className="flex justify-between"><span>Vision:</span> <span className="text-purple-300">YOLOv8 + ResNet</span></div>
              <div className="flex justify-between"><span>NLP:</span> <span className="text-slate-200">BERT / LLM Classifier</span></div>
              <div className="flex justify-between"><span>Thermal:</span> <span className="text-slate-200">FLIR Infrared Parser</span></div>
              <div className="flex justify-between"><span>Explainability:</span> <span className="text-purple-300">SHAP / XAI Rationale</span></div>
            </div>
          </div>

        </div>

        {/* Requirements Matrix from Synopsis */}
        <div className="glass-card p-6 sm:p-8 rounded-2xl border border-slate-800">
          <div className="flex items-center gap-2 mb-6">
            <Binary className="w-5 h-5 text-cyan-400" />
            <h3 className="text-lg font-bold text-white font-mono uppercase">
              Hardware & Software System Requirements Matrix
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
            <div className="space-y-3">
              <h4 className="font-mono text-xs text-cyan-400 font-semibold uppercase">Hardware Specifications</h4>
              <ul className="space-y-2 text-slate-300">
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                  <span><strong>Workstation:</strong> Intel Core i7 / AMD Ryzen 7, 16GB+ RAM</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                  <span><strong>Camera / Sensors:</strong> Mobile optical camera, drone thermal sensor input</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                  <span><strong>Display:</strong> High-resolution multi-panel command display</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                  <span><strong>Network:</strong> Low-latency 4G/5G and satellite emergency backhaul</span>
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-mono text-xs text-blue-400 font-semibold uppercase">Software Specifications</h4>
              <ul className="space-y-2 text-slate-300">
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />
                  <span><strong>OS:</strong> Windows 10/11 / Linux (Ubuntu 22.04 LTS)</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />
                  <span><strong>Frontend:</strong> React 18, TypeScript, Tailwind CSS, Three.js, GSAP</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />
                  <span><strong>Backend:</strong> Python 3.11, FastAPI, Pydantic, Uvicorn</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />
                  <span><strong>Mapping & GIS:</strong> OpenStreetMap, Leaflet GeoJSON layer engine</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

      </div>
    </section>
  );
};

