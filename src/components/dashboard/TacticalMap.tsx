import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { Incident, RescueResource, RouteHazard } from '../../types';
import { soundManager } from '../../utils/audio';

interface TacticalMapProps {
  incidents: Incident[];
  resources: RescueResource[];
  hazards: RouteHazard[];
  selectedIncident: Incident | null;
  onSelectIncident: (inc: Incident) => void;
  onOpenRouteAnalysis: (inc: Incident) => void;
}

export const TacticalMap: React.FC<TacticalMapProps> = ({
  incidents,
  resources,
  hazards,
  selectedIncident,
  onSelectIncident,
  onOpenRouteAnalysis
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const markersLayerRef = useRef<L.LayerGroup | null>(null);
  const routesLayerRef = useRef<L.LayerGroup | null>(null);

  // Initialize Map
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    // Center on Mangaluru coastal coordinate
    const map = L.map(mapContainerRef.current, {
      center: [12.8950, 74.8500],
      zoom: 12,
      zoomControl: false,
      attributionControl: false
    });

    // Dark Matter CartoDB Basemap Tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
      subdomains: 'abcd',
    }).addTo(map);

    // Zoom control at bottom right
    L.control.zoom({ position: 'bottomright' }).addTo(map);

    markersLayerRef.current = L.layerGroup().addTo(map);
    routesLayerRef.current = L.layerGroup().addTo(map);
    mapInstanceRef.current = map;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // Sync Markers, Hazards and Polylines
  useEffect(() => {
    const map = mapInstanceRef.current;
    const markersLayer = markersLayerRef.current;
    const routesLayer = routesLayerRef.current;
    if (!map || !markersLayer || !routesLayer) return;

    markersLayer.clearLayers();
    routesLayer.clearLayers();

    // 1. Draw Route Hazards (Circles & Polylines)
    hazards.forEach((hazard) => {
      const hazardColor = hazard.type === 'flooded_road' ? '#00f0ff' : hazard.type === 'fire_perimeter' ? '#ff3366' : '#ffb020';
      
      // Draw hazard polyline
      const poly = L.polyline(hazard.coordinates, {
        color: hazardColor,
        weight: 5,
        opacity: 0.8,
        dashArray: '8, 8'
      }).addTo(routesLayer);

      poly.bindPopup(`
        <div style="font-family: monospace; font-size: 11px;">
          <strong style="color: ${hazardColor};">HAZARD ZONE: ${hazard.name}</strong><br/>
          Status: <span style="color: #ff3366; font-weight: bold;">${hazard.riskLevel.toUpperCase()}</span><br/>
          Severity Impact: ${hazard.severity}%
        </div>
      `);

      // Pulsing hazard danger perimeter circle
      if (hazard.coordinates.length > 0) {
        L.circle(hazard.coordinates[0], {
          radius: 350,
          color: hazardColor,
          fillColor: hazardColor,
          fillOpacity: 0.15,
          weight: 1
        }).addTo(routesLayer);
      }
    });

    // 2. Draw Incident Markers
    incidents.forEach((inc) => {
      const isSelected = selectedIncident?.id === inc.id;
      const isP1 = inc.priority === 'P1_CRITICAL';
      const isP2 = inc.priority === 'P2_HIGH';
      const badgeColor = isP1 ? '#ff3366' : isP2 ? '#ffb020' : '#00f0ff';

      const customHtml = `
        <div style="position: relative; width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; cursor: pointer;">
          <div style="position: absolute; width: 100%; height: 100%; border-radius: 50%; background-color: ${badgeColor}; opacity: 0.35; animation: ping 1.4s cubic-bezier(0, 0, 0.2, 1) infinite;"></div>
          <div style="position: relative; width: 26px; height: 26px; border-radius: 50%; background-color: #070b14; border: 2px solid ${badgeColor}; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 14px ${badgeColor};">
            <span style="font-size: 12px;">${inc.type === 'flood' ? '🌊' : inc.type === 'fire' ? '🔥' : inc.type === 'landslide' ? '⛰️' : inc.type === 'collapse' ? '🏚️' : '🌪️'}</span>
          </div>
          ${isSelected ? `<div style="position: absolute; -top: 4px; -right: 4px; width: 10px; height: 10px; border-radius: 50%; background-color: #00f0ff; border: 2px solid #000;"></div>` : ''}
        </div>
      `;

      const icon = L.divIcon({
        html: customHtml,
        className: 'custom-disaster-marker',
        iconSize: [34, 34],
        iconAnchor: [17, 17],
      });

      const marker = L.marker([inc.location.lat, inc.location.lng], { icon }).addTo(markersLayer);

      marker.on('click', () => {
        soundManager.playBlip(800, 0.08);
        onSelectIncident(inc);
      });

      // Quick tooltip
      marker.bindTooltip(`
        <div style="font-family: monospace; font-size: 10px; padding: 2px;">
          <span style="color: ${badgeColor}; font-weight: bold;">[${inc.priority}] ${inc.id}</span><br/>
          <span>${inc.title}</span><br/>
          <span style="color: #cbd5e1;">Victims: ${inc.victimCount.estimated} | Severity: ${inc.severity}%</span>
        </div>
      `, { direction: 'top', offset: [0, -14] });
    });

    // 3. Draw Resource Units (Boats, Ambulances, UAVs)
    resources.forEach((res) => {
      const resIconEmoji = res.type === 'ndrf_boat' ? '🚤' : res.type === 'ambulance' ? '🚑' : res.type === 'fire_unit' ? '🚒' : res.type === 'uav_recon' ? '🛸' : '🏥';
      const isAvailable = res.status === 'available';
      const statusColor = isAvailable ? '#00e676' : '#00f0ff';

      const resHtml = `
        <div style="width: 28px; height: 28px; border-radius: 6px; background-color: #0d1527; border: 1.5px solid ${statusColor}; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 10px ${statusColor}80; cursor: pointer;">
          <span style="font-size: 13px;">${resIconEmoji}</span>
        </div>
      `;

      const icon = L.divIcon({
        html: resHtml,
        className: 'custom-resource-marker',
        iconSize: [28, 28],
        iconAnchor: [14, 14],
      });

      const resMarker = L.marker([res.location.lat, res.location.lng], { icon }).addTo(markersLayer);

      resMarker.bindTooltip(`
        <div style="font-family: monospace; font-size: 10px;">
          <strong style="color: ${statusColor};">${res.name}</strong><br/>
          <span>Status: ${res.status.toUpperCase()}</span><br/>
          <span>Battery/Fuel: ${res.fuelBatteryPercent}%</span>
        </div>
      `, { direction: 'bottom' });

      // If unit is assigned to an incident, draw dynamic green safe route polyline
      if (res.assignedIncidentId) {
        const targetInc = incidents.find(i => i.id === res.assignedIncidentId);
        if (targetInc) {
          // Calculate midpoint to simulate bypass around hazard
          const midLat = (res.location.lat + targetInc.location.lat) / 2 + 0.005;
          const midLng = (res.location.lng + targetInc.location.lng) / 2 - 0.008;

          L.polyline([
            [res.location.lat, res.location.lng],
            [midLat, midLng],
            [targetInc.location.lat, targetInc.location.lng]
          ], {
            color: '#00e676',
            weight: 3.5,
            dashArray: '6, 6',
            opacity: 0.9
          }).addTo(routesLayer);
        }
      }
    });

    // Pan smoothly to selected incident
    if (selectedIncident) {
      map.flyTo([selectedIncident.location.lat, selectedIncident.location.lng], 13.5, {
        duration: 1.2
      });
    }

  }, [incidents, resources, hazards, selectedIncident]);

  return (
    <div className="relative w-full h-full min-h-[460px] rounded-2xl overflow-hidden border border-cyan-500/20 glass-panel shadow-2xl">
      {/* Leaflet Map Div */}
      <div ref={mapContainerRef} className="w-full h-full z-0" />

      {/* Map Tactical HUD Overlays */}
      <div className="absolute top-3 left-3 z-10 flex flex-col gap-1.5 pointer-events-none">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-950/80 border border-cyan-500/30 text-cyan-400 font-mono text-xs backdrop-blur-md">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
          <span className="font-bold">GIS SITUATIONAL OVERVIEW (OSM DARK)</span>
        </div>

        <div className="flex items-center gap-2 px-2.5 py-1 rounded bg-slate-950/70 border border-slate-800 text-[10px] font-mono text-slate-400 backdrop-blur-sm">
          <span>COASTAL KARNATAKA SECTOR • MANGALURU</span>
        </div>
      </div>

      {/* Map Legend Overlay */}
      <div className="absolute bottom-3 left-3 z-10 p-2.5 rounded-xl bg-slate-950/85 border border-slate-800 text-[11px] font-mono text-slate-300 backdrop-blur-md flex flex-wrap gap-3">
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-red-500 shadow-sm shadow-red-500" />
          <span>P1 Critical</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-400 shadow-sm shadow-amber-400" />
          <span>P2 High</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400" />
          <span>P3 Moderate</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-sm bg-emerald-400" />
          <span>Rescue Fleet Unit</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-4 h-0.5 bg-emerald-400" />
          <span>Safe Route Corridor</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-4 h-0.5 border-b border-dashed border-cyan-400" />
          <span>Hazard Bypass Area</span>
        </div>
      </div>

      {/* Route Analysis Trigger Pill if incident selected */}
      {selectedIncident && (
        <div className="absolute top-3 right-3 z-10">
          <button
            onClick={() => {
              soundManager.playBlip(880, 0.08);
              onOpenRouteAnalysis(selectedIncident);
            }}
            className="px-3 py-1.5 rounded-lg bg-cyan-950/90 border border-cyan-400/50 hover:bg-cyan-900 text-cyan-300 text-xs font-mono font-semibold flex items-center gap-2 shadow-lg backdrop-blur-md hover:scale-105 transition-all"
          >
            <span>Inspect Hazard Clearance Corridor</span>
            <span className="text-cyan-400 font-bold">→</span>
          </button>
        </div>
      )}
    </div>
  );
};

