import React, { useState, useRef } from 'react';
import { X, Upload, FileText, Check, AlertCircle, Loader2 } from 'lucide-react';
import { ColumnMappingConfig, UploadPreviewResponse } from '../types/api';
import { uploadPreview } from '../services/api';

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAnalyze: (file: File, mapping: ColumnMappingConfig) => Promise<void>;
}

export const UploadModal: React.FC<UploadModalProps> = ({ isOpen, onClose, onAnalyze }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewData, setPreviewData] = useState<UploadPreviewResponse | null>(null);
  const [mapping, setMapping] = useState<ColumnMappingConfig>({ date_col: 'Date' });
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setSelectedFile(file);
    setError(null);
    setLoading(true);

    try {
      const res = await uploadPreview(file);
      setPreviewData(res);
      setMapping(res.suggested_mapping);
    } catch (err: any) {
      setError(err.message || 'Failed to inspect file');
    } finally {
      setLoading(false);
    }
  };

  const handleConfirm = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);

    try {
      await onAnalyze(selectedFile, mapping);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to analyze dataset');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-200">
        {/* Header */}
        <div className="p-5 border-b border-slate-200 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-sky-50 text-sky-600">
              <Upload className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">
                Upload Small Shop Sales Dataset
              </h2>
              <p className="text-xs text-slate-500">
                Supports CSV and Excel files (.xlsx / .csv) with flexible column mapping
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
        <div className="p-5 overflow-y-auto space-y-4 text-xs">
          {error && (
            <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {/* File Selector Box */}
          <div
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-slate-300 hover:border-sky-500 rounded-xl p-6 text-center cursor-pointer bg-slate-50 hover:bg-sky-50/50 transition group"
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept=".csv,.xlsx,.xls,.txt"
              className="hidden"
            />
            <div className="w-12 h-12 rounded-full bg-white shadow-sm border border-slate-200 flex items-center justify-center mx-auto mb-2 text-slate-500 group-hover:text-sky-600 transition">
              <FileText className="w-6 h-6" />
            </div>
            <p className="font-semibold text-slate-800 text-sm">
              {selectedFile ? selectedFile.name : 'Click to select CSV or Excel dataset'}
            </p>
            <p className="text-[11px] text-slate-500 mt-1">
              Supports standard report format or arbitrary retail transaction exports
            </p>
          </div>

          {loading && (
            <div className="flex items-center justify-center py-6 text-slate-500 gap-2">
              <Loader2 className="w-5 h-5 animate-spin text-sky-600" />
              <span>Processing dataset...</span>
            </div>
          )}

          {/* Column Mapping Section */}
          {previewData && !loading && (
            <div className="space-y-4">
              <div className="bg-sky-50 border border-sky-200 rounded-xl p-3 text-sky-900">
                <div className="font-semibold text-xs mb-0.5">
                  Detected {previewData.total_rows} rows and {previewData.columns.length} columns.
                </div>
                <p className="text-[11px] text-sky-800">
                  Verify or adjust the column assignments below so our analytics engine accurately maps your metrics.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-200">
                {/* Date */}
                <div>
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">
                    Date Column <span className="text-rose-500">*</span>
                  </label>
                  <select
                    className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-sky-500"
                    value={mapping.date_col}
                    onChange={(e) => setMapping({ ...mapping, date_col: e.target.value })}
                  >
                    {previewData.columns.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Day of Week */}
                <div>
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">
                    Day of Week Column (Optional)
                  </label>
                  <select
                    className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-sky-500"
                    value={mapping.day_col || ''}
                    onChange={(e) => setMapping({ ...mapping, day_col: e.target.value || null })}
                  >
                    <option value="">Auto-calculate from Date</option>
                    {previewData.columns.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Product Name */}
                <div>
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">
                    Product / Item Name Column
                  </label>
                  <select
                    className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-sky-500"
                    value={mapping.product_col || ''}
                    onChange={(e) => setMapping({ ...mapping, product_col: e.target.value || null })}
                  >
                    <option value="">None (Use 'Item')</option>
                    {previewData.columns.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Category */}
                <div>
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">
                    Category / Department Column
                  </label>
                  <select
                    className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-sky-500"
                    value={mapping.category_col || ''}
                    onChange={(e) => setMapping({ ...mapping, category_col: e.target.value || null })}
                  >
                    <option value="">None (Use 'General')</option>
                    {previewData.columns.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Quantity */}
                <div>
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">
                    Quantity Sold Column
                  </label>
                  <select
                    className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-sky-500"
                    value={mapping.quantity_col || ''}
                    onChange={(e) => setMapping({ ...mapping, quantity_col: e.target.value || null })}
                  >
                    <option value="">None (Count 1 unit per row)</option>
                    {previewData.columns.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Price */}
                <div>
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">
                    Unit Price Column
                  </label>
                  <select
                    className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-sky-500"
                    value={mapping.price_col || ''}
                    onChange={(e) => setMapping({ ...mapping, price_col: e.target.value || null })}
                  >
                    <option value="">None</option>
                    {previewData.columns.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Precalculated Total Sales */}
                <div className="sm:col-span-2">
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">
                    Pre-Calculated Total Sales Column (Avoids Re-Multiplying)
                  </label>
                  <select
                    className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs focus:ring-2 focus:ring-sky-500"
                    value={mapping.total_sales_col || ''}
                    onChange={(e) => setMapping({ ...mapping, total_sales_col: e.target.value || null })}
                  >
                    <option value="">Calculate dynamically: Quantity × Price</option>
                    {previewData.columns.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 bg-slate-50 rounded-b-2xl flex items-center justify-between">
          <button
            onClick={onClose}
            className="px-4 py-2 text-slate-600 hover:text-slate-800 text-xs font-semibold"
          >
            Cancel
          </button>
          <button
            onClick={handleConfirm}
            disabled={!selectedFile || loading}
            className="px-5 py-2 bg-sky-600 hover:bg-sky-700 disabled:opacity-50 text-white rounded-lg text-xs font-semibold shadow-sm transition flex items-center gap-1.5"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4" />}
            <span>Analyze Dataset</span>
          </button>
        </div>
      </div>
    </div>
  );
};
