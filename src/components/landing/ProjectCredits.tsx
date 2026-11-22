import React from 'react';
import { Award, GraduationCap, Building2, User, Users, BookOpen } from 'lucide-react';

export const ProjectCredits: React.FC = () => {
  const students = [
    { name: 'PREETHESH', usn: '4JK24CI082', role: 'System Architecture & AI Resource Optimization' },
    { name: 'PAVAN KUMAR', usn: '4JK24CI080', role: 'Full-Stack Command HUD & GIS Navigation' },
    { name: 'YASHASH', usn: '4JK24CI121', role: 'Computer Vision & Damage Triage Pipelines' },
    { name: 'MUGIL KUMAR', usn: '4JK24CI074', role: 'Explainable AI & Natural Language Ingestion' },
  ];

  return (
    <section id="credits" className="relative py-20 px-4 lg:px-8 bg-[#070b14] border-t border-slate-800">
      <div className="max-w-6xl mx-auto">
        
        {/* VTU Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-400 text-xs font-mono mb-2">
            <GraduationCap className="w-4 h-4" />
            <span>VISVESVARAYA TECHNOLOGICAL UNIVERSITY (VTU) BELAGAVI</span>
          </div>
          <h2 className="text-2xl sm:text-4xl font-extrabold text-white uppercase tracking-tight">
            Academic Project Synopsis Attribution
          </h2>
          <p className="text-slate-400 text-sm mt-2 max-w-xl mx-auto">
            Department of CSE (Artificial Intelligence & Machine Learning)
            <br />
            A J Institute of Engineering and Technology, Mangaluru, Karnataka
          </p>
        </div>

        {/* Institution Info Card */}
        <div className="glass-panel p-6 rounded-2xl border border-cyan-500/20 mb-8 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-xl bg-gradient-to-tr from-amber-500/20 to-cyan-500/20 border border-cyan-400/40 flex items-center justify-center text-cyan-300">
              <Building2 className="w-8 h-8 text-cyan-400" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">A J INSTITUTE OF ENGINEERING AND TECHNOLOGY</h3>
              <p className="text-xs text-slate-300">NH-66, Kottara Chowki, Mangaluru – 575006, Karnataka, India</p>
              <p className="text-[11px] text-cyan-400 font-mono mt-0.5">Approved by AICTE | Affiliated to VTU Belagavi | Accredited by NAAC & NBA</p>
            </div>
          </div>

          <div className="text-left md:text-right border-t md:border-t-0 md:border-l border-slate-800 pt-4 md:pt-0 md:pl-6">
            <span className="text-[10px] font-mono uppercase text-slate-400">Academic Year</span>
            <div className="text-sm font-bold text-white font-mono">2026 – 2027</div>
            <span className="text-xs text-emerald-400 font-semibold">Bachelor of Engineering in AIML</span>
          </div>
        </div>

        {/* Faculty Leadership */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
          <div className="glass-card p-4 rounded-xl border border-slate-800">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                <User className="w-5 h-5" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase text-cyan-400">Project Guide</span>
                <h4 className="text-sm font-bold text-white">Dr. Pradeep Udupa</h4>
                <p className="text-[11px] text-slate-400">Associate Professor, CSE (AI&ML)</p>
              </div>
            </div>
          </div>

          <div className="glass-card p-4 rounded-xl border border-slate-800">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/30">
                <User className="w-5 h-5" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase text-blue-400">Mini Project Coordinator</span>
                <h4 className="text-sm font-bold text-white">Mrs. Deeptha Hegde</h4>
                <p className="text-[11px] text-slate-400">Assistant Professor, CSE (AI&ML)</p>
              </div>
            </div>
          </div>

          <div className="glass-card p-4 rounded-xl border border-slate-800">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/30">
                <User className="w-5 h-5" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase text-purple-400">Head of Department (HOD)</span>
                <h4 className="text-sm font-bold text-white">Mr. Chanchal Antony</h4>
                <p className="text-[11px] text-slate-400">Department of CSE (AI&ML)</p>
              </div>
            </div>
          </div>
        </div>

        {/* Student Team Grid */}
        <div className="mb-10">
          <h4 className="text-xs font-mono uppercase text-slate-400 font-semibold mb-4 flex items-center gap-2">
            <Users className="w-4 h-4 text-cyan-400" />
            <span>Student Investigators (B.E. AIML Candidates)</span>
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {students.map((student, idx) => (
              <div 
                key={idx}
                className="glass-card p-4 rounded-xl border border-slate-800 hover:border-cyan-500/40 transition-all hover:scale-[1.02]"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono font-bold text-cyan-400 bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-500/30">
                    {student.usn}
                  </span>
                  <span className="text-[10px] font-mono text-slate-500">#{idx + 1}</span>
                </div>
                <h5 className="font-bold text-white text-sm mb-1">{student.name}</h5>
                <p className="text-[11px] text-slate-400 leading-snug">{student.role}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Academic Citations from Synopsis */}
        <div className="p-6 rounded-2xl bg-slate-950/80 border border-slate-800">
          <div className="flex items-center gap-2 mb-3">
            <BookOpen className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-mono uppercase text-slate-300 font-bold">Key Academic Foundations & References</span>
          </div>
          <ul className="text-[11px] text-slate-400 space-y-1.5 font-mono">
            <li>[1] H. Zheng, X. Zhao, X. Yang, and B. Chen, "Predictive Resource Request for Disaster Response: A Deep Learning-Based Optimization Model," <em>Info Systems Research</em>, 2024.</li>
            <li>[2] W. Wang, K. Yang, L. Yang, and Z. Gao, "Distributionally Robust Chance-Constrained Programming for Disaster Vehicle Routing," <em>Omega</em>, 2023.</li>
            <li>[3] T. I. Faiz, C. Vogiatzis, J. Liu, and M. Noor-E-Alam, "Two-Echelon Vehicle and UAV Routing for Post-Disaster Logistics," <em>Networks</em>, 2024.</li>
            <li>[4] United Nations Office for Disaster Risk Reduction (UNDRR) & WMO, "Leveraging AI to Enhance Multi-Hazard Early Warning Systems," 2026.</li>
          </ul>
        </div>

      </div>
    </section>
  );
};

