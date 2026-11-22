import React, { useState, Component, ErrorInfo, ReactNode } from 'react';
import { Navbar } from './components/landing/Navbar';
import { HeroSection } from './components/landing/HeroSection';
import { GSAPWorkflowSection } from './components/landing/GSAPWorkflowSection';
import { ArchitectureSection } from './components/landing/ArchitectureSection';
import { ProjectCredits } from './components/landing/ProjectCredits';
import { CommandDashboard } from './components/dashboard/CommandDashboard';
import { Terminal, ShieldAlert, RefreshCw } from 'lucide-react';
import { soundManager } from './utils/audio';

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  public state: ErrorBoundaryState = { hasError: false };

  public static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('RESQGRID UI caught an error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-[#050811] text-slate-100 flex flex-col items-center justify-center p-6 text-center font-mono">
          <div className="p-4 rounded-full bg-red-950/80 border border-red-500/40 text-red-400 mb-4 animate-pulse">
            <ShieldAlert className="w-10 h-10" />
          </div>
          <h2 className="text-xl font-bold text-white mb-2">RESQGRID DIAGNOSTIC RECOVERY</h2>
          <p className="text-xs text-slate-400 max-w-md mb-6 leading-relaxed">
            The telemetry display encountered a rendering exception: {this.state.error?.message}
          </p>
          <button
            onClick={() => {
              this.setState({ hasError: false });
              window.location.reload();
            }}
            className="px-5 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs uppercase flex items-center gap-2 hover:bg-cyan-400 transition-all"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Reset Telemetry Systems</span>
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'landing' | 'dashboard'>('landing');

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-[#050811] text-slate-100 font-sans selection:bg-cyan-500 selection:text-black">
        {activeTab === 'landing' ? (
          <div className="relative">
            {/* Main Top Navigation */}
            <Navbar
              onOpenDashboard={() => setActiveTab('dashboard')}
              activeTab={activeTab}
              setActiveTab={setActiveTab}
            />

            {/* 3D Hero Section */}
            <HeroSection
              onOpenDashboard={() => setActiveTab('dashboard')}
            />

            {/* 9-Stage GSAP & ScrollTrigger Workflow Section */}
            <GSAPWorkflowSection />

            {/* System Architecture & Hardware/Software Specs */}
            <ArchitectureSection />

            {/* VTU Capstone Credits & Faculty Attribution */}
            <ProjectCredits />

            {/* Floating Command Center Quick Pill */}
            <div className="fixed bottom-6 right-6 z-40">
              <button
                onClick={() => {
                  soundManager.playApprovedChime();
                  setActiveTab('dashboard');
                }}
                className="px-5 py-3 rounded-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold text-xs uppercase tracking-wider flex items-center gap-2.5 shadow-xl shadow-cyan-500/30 hover:scale-105 active:scale-95 transition-all glow-cyan"
              >
                <Terminal className="w-4 h-4" />
                <span>Enter Command Dashboard</span>
              </button>
            </div>

            {/* Footer */}
            <footer className="py-8 px-4 text-center font-mono text-xs text-slate-500 border-t border-slate-900 bg-[#04060c]">
              <p>
                RESQGRID © 2026-2027 • AI-Powered Disaster Response Intelligence & Resource Optimization
              </p>
              <p className="text-[10px] text-slate-600 mt-1">
                Department of CSE (AI & ML) • A J Institute of Engineering & Technology, Mangaluru • VTU Belagavi
              </p>
            </footer>
          </div>
        ) : (
          /* Centralized Mission Command Center */
          <CommandDashboard
            onBackToLanding={() => setActiveTab('landing')}
          />
        )}
      </div>
    </ErrorBoundary>
  );
};

export default App;
