import React from 'react';
import { Sparkles, TrendingUp, AlertTriangle, ArrowRight, Lightbulb } from 'lucide-react';
import { InsightItem } from '../types/api';

interface AutomatedFindingsProps {
  insights: InsightItem[];
}

export const AutomatedFindings: React.FC<AutomatedFindingsProps> = ({ insights }) => {
  if (!insights || insights.length === 0) return null;

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl p-6 text-white mb-6 shadow-md border border-slate-700">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-700/60">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-lg bg-sky-500/20 text-sky-400">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white tracking-tight">
              Evidence-Based Sales Insights & Findings
            </h2>
            <p className="text-xs text-slate-400">
              Computed deterministically from transactions according to project report methodology
            </p>
          </div>
        </div>
        <span className="text-xs bg-slate-800 text-slate-300 px-3 py-1 rounded-full border border-slate-700 font-mono">
          {insights.length} Patterns Detected
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {insights.map((item, idx) => {
          const isHigh = item.importance === 'high';
          const isWarning = item.category === 'inventory_risk';

          return (
            <div
              key={idx}
              className={`rounded-xl p-4 border transition ${
                isWarning
                  ? 'bg-amber-950/20 border-amber-800/40'
                  : isHigh
                  ? 'bg-sky-950/20 border-sky-800/40'
                  : 'bg-slate-800/60 border-slate-700/60'
              }`}
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <span
                  className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded ${
                    isWarning
                      ? 'bg-amber-900/60 text-amber-300'
                      : isHigh
                      ? 'bg-sky-900/60 text-sky-300'
                      : 'bg-slate-700 text-slate-300'
                  }`}
                >
                  {item.category.replace('_', ' ')}
                </span>
                {item.metric_value && (
                  <span className="text-xs font-mono font-semibold text-emerald-400">
                    {item.metric_value}
                  </span>
                )}
              </div>
              <h4 className="text-sm font-semibold text-slate-100 mb-1">
                {item.title}
              </h4>
              <p className="text-xs text-slate-300 leading-relaxed">
                {item.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
