import React from 'react';
import { X, ShieldCheck, AlertTriangle, AlertCircle, Calendar, Copy, CheckCircle2 } from 'lucide-react';
import { DataQualityReport } from '../types/api';

interface DataQualityModalProps {
  isOpen: boolean;
  onClose: () => void;
  report: DataQualityReport;
}

export const DataQualityModal: React.FC<DataQualityModalProps> = ({ isOpen, onClose, report }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-200">
        {/* Header */}
        <div className="p-5 border-b border-slate-200 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-sky-50 text-sky-600">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">
                Data Quality Audit & Preprocessing Log
              </h2>
              <p className="text-xs text-slate-500">
                Transparent auditing of data health, calendar reconciliation, and imputation
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 overflow-y-auto space-y-5 text-xs text-slate-700">
          {/* Summary Stat Badges */}
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3">
              <div className="text-[11px] font-medium text-slate-500">Raw Input Rows</div>
              <div className="text-lg font-bold text-slate-900 font-mono mt-0.5">
                {report.total_raw_rows}
              </div>
            </div>
            <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3">
              <div className="text-[11px] font-medium text-emerald-700">Accepted Rows</div>
              <div className="text-lg font-bold text-emerald-800 font-mono mt-0.5">
                {report.accepted_rows}
              </div>
            </div>
            <div className="bg-amber-50 border border-amber-200 rounded-xl p-3">
              <div className="text-[11px] font-medium text-amber-700">Date/Day Corrections</div>
              <div className="text-lg font-bold text-amber-800 font-mono mt-0.5">
                {report.date_corrections_count}
              </div>
            </div>
            <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-3">
              <div className="text-[11px] font-medium text-indigo-700">Duplicates Handled</div>
              <div className="text-lg font-bold text-indigo-800 font-mono mt-0.5">
                {report.duplicate_rows_detected}
              </div>
              <div className="text-[10px] text-indigo-600 mt-0.5">
                {report.duplicate_rows_removed > 0
                  ? `${report.duplicate_rows_removed} removed`
                  : 'preserved'}
              </div>
            </div>
            <div className="bg-rose-50 border border-rose-200 rounded-xl p-3">
              <div className="text-[11px] font-medium text-rose-700">Rejected Rows</div>
              <div className="text-lg font-bold text-rose-800 font-mono mt-0.5">
                {report.rejected_rows}
              </div>
            </div>
          </div>

          {/* Warnings Section */}
          {report.warnings.length > 0 && (
            <div className="bg-amber-50 border border-amber-200 rounded-xl p-3.5 space-y-2">
              <div className="font-semibold text-amber-900 flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4 text-amber-600" />
                <span>Quality Notices & Observations:</span>
              </div>
              <ul className="list-disc list-inside space-y-1 text-amber-800">
                {report.warnings.map((w, i) => (
                  <li key={i}>{w}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Issue Log List */}
          <div>
            <h4 className="font-bold text-slate-900 mb-2">Detailed Row-Level Operations:</h4>
            {report.issues.length === 0 ? (
              <div className="flex items-center gap-2 p-3 bg-emerald-50 text-emerald-800 rounded-lg">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>No row-level anomalies detected. Dataset passed all validation checks cleanly!</span>
              </div>
            ) : (
              <div className="max-h-60 overflow-y-auto rounded-lg border border-slate-200 divide-y divide-slate-100">
                {report.issues.map((issue, idx) => (
                  <div key={idx} className="p-2.5 flex items-start justify-between gap-3 bg-white">
                    <div>
                      <div className="flex items-center gap-1.5">
                        <span
                          className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                            issue.severity === 'error'
                              ? 'bg-rose-100 text-rose-800'
                              : 'bg-amber-100 text-amber-800'
                          }`}
                        >
                          {issue.issue_type.replace(/_/g, ' ')}
                        </span>
                        <span className="font-medium text-slate-800">
                          Row {issue.row_index + 1} ({issue.column})
                        </span>
                      </div>
                      {issue.details && (
                        <p className="text-[11px] text-slate-600 mt-1">{issue.details}</p>
                      )}
                    </div>
                    <span className="font-mono text-[11px] text-slate-500 whitespace-nowrap bg-slate-100 px-2 py-0.5 rounded">
                      {issue.action_taken}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Methodology Card */}
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-slate-600 text-[11px] leading-relaxed">
            <strong className="text-slate-800 block mb-1">Audit Protocol Reference:</strong>
            Sales formula: <code>Total = Quantity × Unit Price</code> (or preserved if pre-calculated). Day-of-week verification computes the genuine Gregorian calendar day to correct manual student entry errors (such as 01-02-2026 being a Sunday rather than Monday). Duplicate Policy: <code>{report.duplicate_policy || 'remove_exact'}</code> (exact duplicate rows are {report.duplicate_policy === 'keep_all' ? 'preserved for multi-item records' : 'removed to protect against double-counting'}).
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 bg-slate-50 rounded-b-2xl flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-semibold transition"
          >
            Close Audit Log
          </button>
        </div>
      </div>
    </div>
  );
};
