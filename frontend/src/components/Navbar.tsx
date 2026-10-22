import React from 'react';
import { Store, Upload, Download, CheckCircle2, ShieldAlert, Sparkles } from 'lucide-react';
import { SampleDatasetMeta } from '../types/api';

interface NavbarProps {
  currentDatasetName: string;
  currentDatasetSource: string;
  samples: SampleDatasetMeta[];
  selectedSampleId: string;
  onSelectSample: (id: string) => void;
  onOpenUpload: () => void;
  onOpenQualityModal: () => void;
  warningsCount: number;
  onExport: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentDatasetName,
  currentDatasetSource,
  samples,
  selectedSampleId,
  onSelectSample,
  onOpenUpload,
  onOpenQualityModal,
  warningsCount,
  onExport,
}) => {
  return (
    <header className="sticky top-0 z-30 bg-white border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand & Title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-md">
              <Store className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-bold text-slate-900 tracking-tight">
                  Small Shop Sales Analysis
                </h1>
                <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-sky-50 text-sky-700 border border-sky-200">
                  Data Science Studio
                </span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">
                Based on University Academic Project · Pattern Recognition & Quality Audit
              </p>
            </div>
          </div>

          {/* Dataset Source Badge & Actions */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Sample Selector */}
            <div className="relative">
              <select
                aria-label="Select Dataset Source"
                className="text-xs sm:text-sm font-medium bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg px-3 py-2 pr-8 border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 cursor-pointer transition"
                value={selectedSampleId}
                onChange={(e) => onSelectSample(e.target.value)}
              >
                {samples.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.title}
                  </option>
                ))}
              </select>
            </div>

            {/* Quality Audit Indicator */}
            <button
              onClick={onOpenQualityModal}
              className={`flex items-center gap-1.5 text-xs sm:text-sm px-3 py-2 rounded-lg font-medium border transition ${
                warningsCount > 0
                  ? 'bg-amber-50 text-amber-800 border-amber-300 hover:bg-amber-100'
                  : 'bg-emerald-50 text-emerald-800 border-emerald-300 hover:bg-emerald-100'
              }`}
              title="View Data Cleaning & Quality Audit"
            >
              {warningsCount > 0 ? (
                <>
                  <ShieldAlert className="w-4 h-4 text-amber-600" />
                  <span>Quality ({warningsCount})</span>
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>Data Clean</span>
                </>
              )}
            </button>

            {/* Upload Button */}
            <button
              onClick={onOpenUpload}
              className="flex items-center gap-1.5 text-xs sm:text-sm px-3 py-2 rounded-lg font-medium bg-sky-600 hover:bg-sky-700 text-white shadow-sm transition"
            >
              <Upload className="w-4 h-4" />
              <span className="hidden md:inline">Upload Data</span>
            </button>

            {/* Export Cleaned CSV */}
            <button
              onClick={onExport}
              className="flex items-center gap-1.5 text-xs sm:text-sm px-3 py-2 rounded-lg font-medium bg-slate-800 hover:bg-slate-900 text-white shadow-sm transition"
              title="Export Current Clean Dataset to CSV"
            >
              <Download className="w-4 h-4" />
              <span className="hidden md:inline">Export CSV</span>
            </button>
          </div>
        </div>
      </div>
      
      {/* Source Provenance Bar */}
      <div className="bg-slate-100/80 border-t border-slate-200 px-4 py-1.5 text-xs text-slate-600 flex items-center justify-between">
        <div className="max-w-7xl mx-auto w-full flex items-center justify-between px-0 sm:px-4">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-700">Active Source:</span>
            <span className="font-medium text-slate-900">{currentDatasetName}</span>
            <span className={`px-2 py-0.5 rounded text-[10px] font-semibold uppercase tracking-wider ${
              currentDatasetSource === 'report_sample'
                ? 'bg-purple-100 text-purple-800'
                : currentDatasetSource === 'realistic_15_days'
                ? 'bg-blue-100 text-blue-800'
                : currentDatasetSource === 'user_upload'
                ? 'bg-emerald-100 text-emerald-800'
                : 'bg-amber-100 text-amber-800'
            }`}>
              {currentDatasetSource.replace('_', ' ')}
            </span>
          </div>
          <div className="hidden sm:flex items-center gap-1 text-[11px] text-slate-500">
            <Sparkles className="w-3.5 h-3.5 text-sky-600" />
            <span>Deterministic Analytics · Formula: Total = Quantity × Price</span>
          </div>
        </div>
      </div>
    </header>
  );
};
