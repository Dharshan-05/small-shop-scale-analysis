import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { KPICards } from './components/KPICards';
import { FilterBar } from './components/FilterBar';
import { DailySalesChart } from './components/DailySalesChart';
import { ProductPerformanceChart } from './components/ProductPerformanceChart';
import { CategoryPieChart } from './components/CategoryPieChart';
import { DayOfWeekChart } from './components/DayOfWeekChart';
import { AutomatedFindings } from './components/AutomatedFindings';
import { DataTable } from './components/DataTable';
import { DataQualityModal } from './components/DataQualityModal';
import { UploadModal } from './components/UploadModal';
import {
  fetchSamples,
  fetchSampleAnalysis,
  uploadAndAnalyze
} from './services/api';
import {
  SalesAnalyticsResponse,
  SampleDatasetMeta,
  ColumnMappingConfig
} from './types/api';
import { Loader2, AlertCircle, RefreshCw } from 'lucide-react';

export const App: React.FC = () => {
  const [samples, setSamples] = useState<SampleDatasetMeta[]>([]);
  const [selectedSampleId, setSelectedSampleId] = useState<string>('report_sample');
  const [data, setData] = useState<SalesAnalyticsResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');

  // Modals
  const [isQualityModalOpen, setIsQualityModalOpen] = useState<boolean>(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState<boolean>(false);

  // Active custom uploaded file ref
  const [uploadedFile, setUploadedFile] = useState<{
    file: File;
    mapping: ColumnMappingConfig;
  } | null>(null);

  // Initial Load
  useEffect(() => {
    async function init() {
      try {
        const sampleList = await fetchSamples();
        setSamples(sampleList);
        await loadSample('report_sample');
      } catch (err: any) {
        setError(err.message || 'Failed to initialize dashboard');
        setLoading(false);
      }
    }
    init();
  }, []);

  const loadSample = async (
    sampleId: string,
    filters?: {
      startDate?: string;
      endDate?: string;
      categories?: string[];
      products?: string[];
    }
  ) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchSampleAnalysis(sampleId, filters);
      setData(res);
      setSelectedSampleId(sampleId);
      setUploadedFile(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load analysis');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectSample = (id: string) => {
    setStartDate('');
    setEndDate('');
    setSelectedCategories([]);
    setSearchTerm('');
    loadSample(id);
  };

  const handleToggleCategory = (cat: string) => {
    const next = selectedCategories.includes(cat)
      ? selectedCategories.filter((c) => c !== cat)
      : [...selectedCategories, cat];
    setSelectedCategories(next);
    applyActiveFilters(next, startDate, endDate, searchTerm);
  };

  const handleStartDateChange = (date: string) => {
    setStartDate(date);
    applyActiveFilters(selectedCategories, date, endDate, searchTerm);
  };

  const handleEndDateChange = (date: string) => {
    setEndDate(date);
    applyActiveFilters(selectedCategories, startDate, date, searchTerm);
  };

  const handleSearchChange = (term: string) => {
    setSearchTerm(term);
    applyActiveFilters(selectedCategories, startDate, endDate, term);
  };

  const handleResetFilters = () => {
    setStartDate('');
    setEndDate('');
    setSelectedCategories([]);
    setSearchTerm('');
    if (uploadedFile) {
      handleUploadedAnalysis(uploadedFile.file, uploadedFile.mapping);
    } else {
      loadSample(selectedSampleId);
    }
  };

  const applyActiveFilters = (
    cats: string[],
    start: string,
    end: string,
    search: string
  ) => {
    const filterPayload = {
      startDate: start || undefined,
      endDate: end || undefined,
      categories: cats.length > 0 ? cats : undefined,
      products: search ? [search] : undefined,
    };

    if (uploadedFile) {
      handleUploadedAnalysis(uploadedFile.file, uploadedFile.mapping, filterPayload);
    } else {
      loadSample(selectedSampleId, filterPayload);
    }
  };

  const handleUploadedAnalysis = async (
    file: File,
    mapping: ColumnMappingConfig,
    filterPayload?: any
  ) => {
    setLoading(true);
    setError(null);
    try {
      const res = await uploadAndAnalyze(file, mapping, filterPayload);
      setData(res);
      setUploadedFile({ file, mapping });
      setSelectedSampleId('user_upload');
    } catch (err: any) {
      setError(err.message || 'Analysis failed on uploaded file');
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = () => {
    if (!data || !data.records_preview || data.records_preview.length === 0) return;

    const headers = Object.keys(data.records_preview[0]);
    const csvRows = [
      headers.join(','),
      ...data.records_preview.map((row) =>
        headers.map((h) => JSON.stringify(row[h] ?? '')).join(',')
      ),
    ];
    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `sales_cleaned_${data.dataset_source}_export.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar
        currentDatasetName={data?.dataset_name || 'Loading...'}
        currentDatasetSource={data?.dataset_source || 'report_sample'}
        samples={samples}
        selectedSampleId={selectedSampleId}
        onSelectSample={handleSelectSample}
        onOpenUpload={() => setIsUploadModalOpen(true)}
        onOpenQualityModal={() => setIsQualityModalOpen(true)}
        warningsCount={(data?.quality_report.warnings.length || 0) + (data?.quality_report.date_corrections_count || 0)}
        onExport={handleExportCSV}
      />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6">
        {/* Error Notification */}
        {error && (
          <div className="p-4 mb-6 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 flex items-center justify-between shadow-sm">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0" />
              <div className="text-xs font-medium">{error}</div>
            </div>
            <button
              onClick={() => handleResetFilters()}
              className="px-3 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold"
            >
              Retry
            </button>
          </div>
        )}

        {/* Loading Overlay */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-20 text-slate-500">
            <Loader2 className="w-8 h-8 animate-spin text-sky-600 mb-3" />
            <p className="text-sm font-medium">Computing sales patterns & aggregates...</p>
          </div>
        )}

        {/* Main Analytics Content */}
        {!loading && data && (
          <>
            {/* KPI Summary Cards */}
            <KPICards kpis={data.kpis} />

            {/* Evidence-Based Findings */}
            <AutomatedFindings insights={data.insights} />

            {/* Interactive Filters Bar */}
            <FilterBar
              categories={data.available_categories}
              selectedCategories={selectedCategories}
              onToggleCategory={handleToggleCategory}
              startDate={startDate}
              endDate={endDate}
              onStartDateChange={handleStartDateChange}
              onEndDateChange={handleEndDateChange}
              searchTerm={searchTerm}
              onSearchChange={handleSearchChange}
              onResetFilters={handleResetFilters}
              minDate={data.min_date}
              maxDate={data.max_date}
              filteredCount={data.records_preview.length}
            />

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              <DailySalesChart data={data.daily_trends} />
              <ProductPerformanceChart products={data.product_performance} />
              <CategoryPieChart categories={data.category_performance} />
              <DayOfWeekChart data={data.day_of_week_performance} />
            </div>

            {/* Cleaned Records Interactive Table */}
            <DataTable records={data.records_preview} onExport={handleExportCSV} />
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-6 text-xs text-slate-500 text-center">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div>
            Small Shop Sales Pattern Analysis Using Data Science · Full-Stack Implementation
          </div>
          <div className="text-slate-400">
            Built with React, Vite, Tailwind CSS, FastAPI & Pandas · Python 3.11
          </div>
        </div>
      </footer>

      {/* Modals */}
      {data && (
        <DataQualityModal
          isOpen={isQualityModalOpen}
          onClose={() => setIsQualityModalOpen(false)}
          report={data.quality_report}
        />
      )}

      <UploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onAnalyze={handleUploadedAnalysis}
      />
    </div>
  );
};
