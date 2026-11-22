import React, { useState } from 'react';
import { 
  Incident, 
  RescueResource, 
  RouteHazard, 
  NextMoveRecommendation 
} from '../../types';
import { 
  INITIAL_INCIDENTS, 
  INITIAL_RESOURCES, 
  ROUTE_HAZARDS 
} from '../../data/mockData';
import { TacticalNavbar } from './TacticalNavbar';
import { TacticalMap } from './TacticalMap';
import { IncidentFeed } from './IncidentFeed';
import { NextMoveCard } from './NextMoveCard';
import { ResourceFleet } from './ResourceFleet';
import { HumanApprovalModal } from './HumanApprovalModal';
import { IncidentIntakeModal } from './IncidentIntakeModal';
import { RouteAnalysisModal } from './RouteAnalysisModal';
import { soundManager } from '../../utils/audio';

interface CommandDashboardProps {
  onBackToLanding: () => void;
}

export const CommandDashboard: React.FC<CommandDashboardProps> = ({ onBackToLanding }) => {
  const [incidents, setIncidents] = useState<Incident[]>(INITIAL_INCIDENTS);
  const [resources, setResources] = useState<RescueResource[]>(INITIAL_RESOURCES);
  const [hazards] = useState<RouteHazard[]>(ROUTE_HAZARDS);
  
  // Selection state
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(INITIAL_INCIDENTS[0]);

  // Modal states
  const [approvalModalOpen, setApprovalModalOpen] = useState(false);
  const [currentRecForApproval, setCurrentRecForApproval] = useState<NextMoveRecommendation | null>(null);
  const [intakeModalOpen, setIntakeModalOpen] = useState(false);
  const [routeModalIncident, setRouteModalIncident] = useState<Incident | null>(null);

  // Critical P1 Count
  const criticalP1Count = incidents.filter(i => i.priority === 'P1_CRITICAL' && i.status !== 'resolved').length;
  const activeIncidentsCount = incidents.filter(i => i.status !== 'resolved').length;

  // Handle Approving a Recommendation (Step 8 of Synopsis)
  const handleApproveRecommendation = (recId: string, commanderName: string, notes: string) => {
    setIncidents(prevIncidents =>
      prevIncidents.map(inc => {
        if (inc.recommendation && inc.recommendation.id === recId) {
          const updatedRec: NextMoveRecommendation = {
            ...inc.recommendation,
            status: 'approved',
            approvedBy: commanderName,
            approvedAt: 'Just now',
            notes: notes
          };
          return {
            ...inc,
            status: 'dispatched',
            assignedResourceIds: [
              ...inc.assignedResourceIds,
              ...updatedRec.recommendedResourceIds
            ],
            recommendation: updatedRec
          };
        }
        return inc;
      })
    );

    // Update resources status to en_route
    if (currentRecForApproval) {
      const unitsToDispatch = currentRecForApproval.recommendedResourceIds;
      setResources(prevRes =>
        prevRes.map(res => {
          if (unitsToDispatch.includes(res.id)) {
            return {
              ...res,
              status: 'en_route',
              assignedIncidentId: currentRecForApproval.incidentId
            };
          }
          return res;
        })
      );
    }
  };

  // AI Auto-Optimize Resources (Step 5 of Synopsis)
  const handleTriggerAutoOptimize = () => {
    // Pairs available resources with pending incidents
    setIncidents(prevIncidents => {
      const unassignedCritical = prevIncidents.filter(
        i => i.status === 'awaiting_approval' && i.assignedResourceIds.length === 0
      );
      if (unassignedCritical.length === 0) return prevIncidents;

      return prevIncidents.map(inc => {
        if (inc.status === 'awaiting_approval' && inc.recommendation) {
          return {
            ...inc,
            recommendation: {
              ...inc.recommendation,
              actionSummary: `[AUTO-OPTIMIZED] Immediate priority dispatch allocated via Hungarian Algorithm matrix.`
            }
          };
        }
        return inc;
      });
    });

    soundManager.playApprovedChime();
  };

  // Reset Simulation
  const handleResetSimulation = () => {
    setIncidents(INITIAL_INCIDENTS);
    setResources(INITIAL_RESOURCES);
    setSelectedIncident(INITIAL_INCIDENTS[0]);
  };

  // Intake new report
  const handleAddIncident = (newInc: Incident) => {
    setIncidents(prev => [newInc, ...prev]);
    setSelectedIncident(newInc);
    soundManager.playAlertSiren();
  };

  return (
    <div className="w-full min-h-screen bg-[#050811] text-slate-100 flex flex-col">
      
      {/* Top Tactical Command Navbar */}
      <TacticalNavbar
        onBackToLanding={onBackToLanding}
        onOpenIntakeModal={() => setIntakeModalOpen(true)}
        onTriggerAutoOptimize={handleTriggerAutoOptimize}
        onResetSimulation={handleResetSimulation}
        activeIncidentsCount={activeIncidentsCount}
        criticalP1Count={criticalP1Count}
      />

      {/* Main Command Dashboard Layout */}
      <main className="flex-1 p-3 sm:p-5 flex flex-col gap-4">
        
        {/* Top Split: Tactical Map (Left) + Incident Triage Queue (Right) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-stretch min-h-[500px]">
          
          {/* Tactical GIS Map */}
          <div className="lg:col-span-8 h-[480px] lg:h-auto">
            <TacticalMap
              incidents={incidents}
              resources={resources}
              hazards={hazards}
              selectedIncident={selectedIncident}
              onSelectIncident={(inc) => setSelectedIncident(inc)}
              onOpenRouteAnalysis={(inc) => setRouteModalIncident(inc)}
            />
          </div>

          {/* Incident Priority Queue */}
          <div className="lg:col-span-4 h-[480px] lg:h-auto">
            <IncidentFeed
              incidents={incidents}
              selectedIncident={selectedIncident}
              onSelectIncident={(inc) => setSelectedIncident(inc)}
            />
          </div>

        </div>

        {/* Bottom Split: Next-Move Explainable Recommendation (Left) + Rescue Fleet Readiness (Right) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-stretch">
          
          {/* Next-Move Recommendation Engine (Step 7 & 8) */}
          <div className="lg:col-span-6">
            <NextMoveCard
              incident={selectedIncident}
              resources={resources}
              onOpenApprovalModal={(rec) => {
                setCurrentRecForApproval(rec);
                setApprovalModalOpen(true);
              }}
              onOpenRouteAnalysis={(inc) => setRouteModalIncident(inc)}
            />
          </div>

          {/* Rescue Fleet Readiness Overview (Step 5) */}
          <div className="lg:col-span-6">
            <ResourceFleet
              resources={resources}
            />
          </div>

        </div>

      </main>

      {/* Modals */}
      {approvalModalOpen && (
        <HumanApprovalModal
          recommendation={currentRecForApproval}
          resources={resources}
          onClose={() => setApprovalModalOpen(false)}
          onApprove={handleApproveRecommendation}
        />
      )}

      {intakeModalOpen && (
        <IncidentIntakeModal
          onClose={() => setIntakeModalOpen(false)}
          onSubmitIncident={handleAddIncident}
        />
      )}

      {routeModalIncident && (
        <RouteAnalysisModal
          incident={routeModalIncident}
          onClose={() => setRouteModalIncident(null)}
        />
      )}

    </div>
  );
};

