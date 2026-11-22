import React, { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { 
  FileText, 
  BrainCircuit, 
  AlertTriangle, 
  ListOrdered, 
  Truck, 
  Compass, 
  Sparkles, 
  UserCheck, 
  LayoutDashboard,
  CheckCircle2,
  ArrowRight,
  Shield,
  Layers
} from 'lucide-react';
import { soundManager } from '../../utils/audio';

gsap.registerPlugin(ScrollTrigger);

interface WorkflowStep {
  step: number;
  title: string;
  synopsisCategory: string;
  cognitiveStage: string;
  icon: React.ElementType;
  summary: string;
  technicalDetails: string[];
  aiFormula: string;
  badgeColor: string;
}

const WORKFLOW_STEPS: WorkflowStep[] = [
  {
    step: 1,
    title: 'Input Collection & Multi-Source Ingestion',
    synopsisCategory: 'Data Intake Layer',
    cognitiveStage: '1. Understand',
    icon: FileText,
    summary: 'Aggregates structured and unstructured disaster reports from citizens, emergency responders, mobile feeds, geo-referenced drone imagery, and real-time weather stations.',
    technicalDetails: [
      'Multi-channel report ingestion (SMS, WhatsApp SOS, Web Form, Drone telemetry)',
      'High-precision GPS coordinate reverse-geocoding',
      'Dynamic weather overlay (rainfall intensity, wind vector, atmospheric pressure)'
    ],
    aiFormula: 'Input_Vector = { Images, GeoCoords, TextSOS, SensorPpm, WeatherMatrix }',
    badgeColor: 'border-blue-500/40 text-blue-400 bg-blue-950/40'
  },
  {
    step: 2,
    title: 'Incident Analysis (NLP & Computer Vision)',
    synopsisCategory: 'AI Vision & Language Processing',
    cognitiveStage: '2. Correlate',
    icon: BrainCircuit,
    summary: 'Employs Convolutional Neural Networks and Large Language Models to classify disaster type, detect victims in imagery, and quantify structural damage levels.',
    technicalDetails: [
      'Computer Vision YOLO/Vision-Transformer: Automated victim and roof detection',
      'NLP Emergency Named Entity Recognition (NER) for critical SOS triage',
      'Synthetic visual confidence scoring with multi-angle cross-referencing'
    ],
    aiFormula: 'Damage_Score = f_CV(Image) * 0.6 + f_NLP(ReportText) * 0.4',
    badgeColor: 'border-cyan-500/40 text-cyan-400 bg-cyan-950/40'
  },
  {
    step: 3,
    title: 'Risk & Escalation Assessment',
    synopsisCategory: 'Vulnerability Analysis',
    cognitiveStage: '3. Assess',
    icon: AlertTriangle,
    summary: 'Calculates dynamic vulnerability based on population density, age demographics (infants/seniors), structural degradation speed, and predictive disaster spread models.',
    technicalDetails: [
      'Topographical floodwater surge velocity integration',
      'Chemical / Wildfire plume dispersal prediction using Gaussian plume modeling',
      'Escalation rate grading: Rapid, Moderate, or Stable trajectory'
    ],
    aiFormula: 'Risk_Index = (Severity * 0.45) + (Vulnerability * 0.35) + (EscalationFactor * 0.20)',
    badgeColor: 'border-amber-500/40 text-amber-400 bg-amber-950/40'
  },
  {
    step: 4,
    title: 'Priority Assessment & Dynamic Triage',
    synopsisCategory: 'Crisis Queue Prioritization',
    cognitiveStage: '3. Assess',
    icon: ListOrdered,
    summary: 'Ranks active incidents into standardized emergency tiers (P1 Critical, P2 High, P3 Moderate) to prevent responder cognitive overload during simultaneous catastrophes.',
    technicalDetails: [
      'Deterministic ranking matrix factoring in life jeopardy and rescue window limits',
      'Autonomous queue re-ranking when environmental conditions degrade',
      'Instant alert broadcast for life-threatening P1 incidents'
    ],
    aiFormula: 'Priority_Rank = ArgMax(TrappedVictims * UrgencyFactor / AccessTime)',
    badgeColor: 'border-rose-500/40 text-rose-400 bg-rose-950/40'
  },
  {
    step: 5,
    title: 'Resource Optimization & Fleet Allocation',
    synopsisCategory: 'Combinatorial Optimization',
    cognitiveStage: '4. Predict',
    icon: Truck,
    summary: 'Solves the multi-depot emergency vehicle allocation problem to pair available rescue assets (NDRF boats, trauma ambulances, fire tenders, UAVs) with incidents.',
    technicalDetails: [
      'Bipartite matching & Mixed Integer Linear Programming (MILP)',
      'Vehicle state verification: battery/fuel levels, paramedic crew capacity',
      'Avoids over-allocation and maintains regional backup reserves'
    ],
    aiFormula: 'Min Σ C_ij * X_ij subject to Capacity and Specialization constraints',
    badgeColor: 'border-emerald-500/40 text-emerald-400 bg-emerald-950/40'
  },
  {
    step: 6,
    title: 'Route Analysis & Hazard-Aware Navigation',
    synopsisCategory: 'GIS & Pathfinding Engine',
    cognitiveStage: '4. Predict',
    icon: Compass,
    summary: 'Computes verified safe navigational corridors by dynamically avoiding flooded underpasses, landslides, and toxic smoke zones using OpenStreetMap GIS graph topology.',
    technicalDetails: [
      'A* pathfinding with real-time dynamic hazard penalty weights',
      'Live road status updates (water depth, fallen trees, bridge collapse)',
      'Alternative contingency route calculation with accurate travel ETA'
    ],
    aiFormula: 'Path_Cost = Distance + Σ (Hazard_Penalty_k / Safety_Margin)',
    badgeColor: 'border-purple-500/40 text-purple-400 bg-purple-950/40'
  },
  {
    step: 7,
    title: 'Explainable AI Next-Move Recommendation',
    synopsisCategory: 'Decision Support Engine',
    cognitiveStage: '5. Recommend',
    icon: Sparkles,
    summary: 'Generates transparent, auditable action proposals detailing exactly WHY a particular unit is dispatched, what time is saved, and what hazards are mitigated.',
    technicalDetails: [
      'Natural language explanation of algorithmic decision rationale',
      'Quantified time-saving and survival impact metrics',
      'Audit logging for post-disaster judicial and operational review'
    ],
    aiFormula: 'XAI_Output = { ActionPlan, Justifications, TimeSaved_Δt, Confidence }',
    badgeColor: 'border-cyan-400/40 text-cyan-300 bg-cyan-950/40'
  },
  {
    step: 8,
    title: 'Human-in-the-Loop Responder Approval',
    synopsisCategory: 'Commander Authorization',
    cognitiveStage: 'Human Decision',
    icon: UserCheck,
    summary: 'Ensures the final execution authority remains strictly with certified human emergency commanders, allowing one-click approval, modification, or tactical override.',
    technicalDetails: [
      'Commander verification interface with full situational dossier',
      'Flexible resource override before physical unit dispatch',
      'Cryptographic electronic signature timestamping'
    ],
    aiFormula: 'Dispatch_Authorized = Boolean(Commander_Key) ∧ Validation_Checks',
    badgeColor: 'border-teal-500/40 text-teal-400 bg-teal-950/40'
  },
  {
    step: 9,
    title: 'Unified Command Dashboard Display',
    synopsisCategory: 'Tactical GIS Command Center',
    cognitiveStage: 'Real-Time Monitoring',
    icon: LayoutDashboard,
    summary: 'Visualizes live incidents, telemetry feeds, resource markers, and safe route polylines on an interactive dark military-grade GIS situational map.',
    technicalDetails: [
      'OpenStreetMap / Leaflet custom dark tactical cartography',
      'Real-time casualty counters, fleet readiness, and audio alert triggers',
      'Seamless coordination between regional EOC and field rescue teams'
    ],
    aiFormula: 'Display_HUD = Render(GeoJSON, TelemetryStreams, DispatchedUnits)',
    badgeColor: 'border-indigo-500/40 text-indigo-400 bg-indigo-950/40'
  }
];

export const GSAPWorkflowSection: React.FC = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const [activeStep, setActiveStep] = useState<number>(1);

  useEffect(() => {
    const el = sectionRef.current;
    if (!el) return;

    try {
      const ctx = gsap.context(() => {
        gsap.from('.workflow-step-item', {
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            toggleActions: 'play none none none'
          },
          y: 20,
          opacity: 0.4,
          stagger: 0.05,
          duration: 0.6,
          ease: 'power2.out'
        });
      }, el);

      return () => {
        try {
          ctx.revert();
        } catch {
          // Ignored
        }
      };
    } catch (err) {
      console.warn('GSAP animation skipped:', err);
    }
  }, []);

  const currentStepData = WORKFLOW_STEPS[activeStep - 1];

  return (
    <section id="workflow" ref={sectionRef} className="relative py-24 px-4 lg:px-8 bg-[#070b14] overflow-hidden">
      {/* Background Ambience */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-600/10 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-[140px] pointer-events-none" />

      <div className="max-w-7xl mx-auto">
        
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-400 text-xs font-mono mb-3">
            <Layers className="w-3.5 h-3.5" />
            <span>SYNOPSIS PROCESS DESCRIPTION • FIG. 1 REPRODUCTION</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight uppercase">
            9-Stage AI Response <span className="text-cyan-400 text-glow-cyan">Pipeline</span>
          </h2>
          <p className="max-w-2xl mx-auto text-slate-400 text-sm sm:text-base mt-3">
            From raw citizen SOS reports to optimized dispatch and explainable tactical decisions with human authorization.
          </p>
        </div>

        {/* Step Selector Ribbon */}
        <div className="flex items-center justify-between gap-1 overflow-x-auto pb-4 mb-10 scrollbar-none border-b border-slate-800">
          {WORKFLOW_STEPS.map((s) => {
            const Icon = s.icon;
            const isSelected = s.step === activeStep;
            return (
              <button
                key={s.step}
                onClick={() => {
                  setActiveStep(s.step);
                  soundManager.playBlip(600 + s.step * 40, 0.08);
                }}
                className={`flex items-center gap-2.5 px-4 py-2.5 rounded-xl whitespace-nowrap transition-all ${
                  isSelected
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/50 shadow-lg shadow-cyan-500/10'
                    : 'text-slate-400 hover:text-white hover:bg-slate-900 border border-transparent'
                }`}
              >
                <div className={`w-6 h-6 rounded-md flex items-center justify-center text-xs font-mono font-bold ${
                  isSelected ? 'bg-cyan-400 text-slate-950' : 'bg-slate-800 text-slate-400'
                }`}>
                  {s.step}
                </div>
                <Icon className="w-4 h-4" />
                <span className="text-xs font-medium hidden md:inline">{s.title.split(' ')[0]} {s.title.split(' ')[1]}</span>
              </button>
            );
          })}
        </div>

        {/* Active Stage Detailed Showcase */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch mb-16">
          
          {/* Left: Interactive Stage Dossier */}
          <div className="lg:col-span-7 glass-panel p-6 sm:p-8 rounded-2xl border border-cyan-500/20 flex flex-col justify-between">
            <div>
              <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
                <span className={`px-3 py-1 rounded-full text-xs font-mono font-semibold border ${currentStepData.badgeColor}`}>
                  STAGE {currentStepData.step} OF 9: {currentStepData.cognitiveStage}
                </span>
                <span className="text-xs font-mono text-slate-400">
                  {currentStepData.synopsisCategory}
                </span>
              </div>

              <h3 className="text-2xl sm:text-3xl font-bold text-white mb-4 flex items-center gap-3">
                <currentStepData.icon className="w-8 h-8 text-cyan-400" />
                <span>{currentStepData.title}</span>
              </h3>

              <p className="text-slate-300 text-base leading-relaxed mb-6 font-sans">
                {currentStepData.summary}
              </p>

              <div className="space-y-3 mb-6">
                <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 font-semibold">
                  Core Technical Capabilities:
                </h4>
                {currentStepData.technicalDetails.map((detail, idx) => (
                  <div key={idx} className="flex items-start gap-3 text-sm text-slate-200">
                    <CheckCircle2 className="w-4 h-4 text-cyan-400 mt-0.5 shrink-0" />
                    <span>{detail}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Algorithmic Formulation / Math representation */}
            <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 font-mono text-xs text-cyan-300/90 flex flex-col gap-1.5">
              <span className="text-[10px] text-slate-500 uppercase tracking-widest">Mathematical Formulation / AI Function</span>
              <code className="text-cyan-300 font-semibold">{currentStepData.aiFormula}</code>
            </div>
          </div>

          {/* Right: Cognitive Stage Pipeline Diagram Card */}
          <div className="lg:col-span-5 glass-card p-6 sm:p-8 rounded-2xl border border-slate-800 flex flex-col justify-between">
            <div>
              <h4 className="text-sm font-mono uppercase tracking-wider text-slate-400 font-bold mb-4 flex items-center gap-2">
                <Shield className="w-4 h-4 text-cyan-400" />
                <span>AI Cognitive Stages (Fig. 1)</span>
              </h4>

              <div className="space-y-3">
                {[
                  { stage: '1. Understand', desc: 'Collect and understand incident information (reports, images, location, weather).', active: currentStepData.cognitiveStage.includes('Understand') },
                  { stage: '2. Correlate', desc: 'Combine and analyze data to identify key incident details.', active: currentStepData.cognitiveStage.includes('Correlate') },
                  { stage: '3. Assess', desc: 'Evaluate severity, risk, vulnerability, and incident priority ranking.', active: currentStepData.cognitiveStage.includes('Assess') },
                  { stage: '4. Predict', desc: 'Predict impact, resource requirements, and hazard-free routes.', active: currentStepData.cognitiveStage.includes('Predict') },
                  { stage: '5. Recommend', desc: 'Generate the best action plan with explainable human-auditable reasons.', active: currentStepData.cognitiveStage.includes('Recommend') },
                  { stage: 'Human Control', desc: 'Authorized responder validates, modifies, or approves final action.', active: currentStepData.cognitiveStage.includes('Human') },
                ].map((item, idx) => (
                  <div 
                    key={idx}
                    className={`p-3 rounded-lg border transition-all ${
                      item.active 
                        ? 'bg-cyan-500/15 border-cyan-400/50 shadow-md shadow-cyan-500/10' 
                        : 'bg-slate-900/40 border-slate-800/80 opacity-70'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className={`text-xs font-mono font-bold ${item.active ? 'text-cyan-300' : 'text-slate-300'}`}>
                        {item.stage}
                      </span>
                      {item.active && (
                        <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                      )}
                    </div>
                    <p className="text-[11px] text-slate-400 leading-snug">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>Next Stage:</span>
              <button 
                onClick={() => {
                  const next = activeStep >= 9 ? 1 : activeStep + 1;
                  setActiveStep(next);
                  soundManager.playBlip(700, 0.08);
                }}
                className="text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-semibold"
              >
                <span>Stage {activeStep >= 9 ? 1 : activeStep + 1}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
};

