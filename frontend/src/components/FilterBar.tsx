import React from 'react';
import { Filter, X, Calendar, Tag, Search } from 'lucide-react';

interface FilterBarProps {
  categories: string[];
  selectedCategories: string[];
  onToggleCategory: (cat: string) => void;
  startDate: string;
  endDate: string;
  onStartDateChange: (date: string) => void;
  onEndDateChange: (date: string) => void;
  searchTerm: string;
  onSearchChange: (val: string) => void;
  onResetFilters: () => void;
  minDate?: string | null;
  maxDate?: string | null;
  filteredCount: number;
}

export const FilterBar: React.FC<FilterBarProps> = ({
  categories,
  selectedCategories,
  onToggleCategory,
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
  searchTerm,
  onSearchChange,
  onResetFilters,
  minDate,
  maxDate,
  filteredCount,
}) => {
  const hasActiveFilters =
    selectedCategories.length > 0 ||
    startDate !== '' ||
    endDate !== '' ||
    searchTerm !== '';

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 mb-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4">
        {/* Left: Filter Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 uppercase tracking-wider mr-1">
            <Filter className="w-3.5 h-3.5 text-sky-600" />
            <span>Filter Data</span>
          </div>

          {/* Search box */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search product..."
              className="text-xs bg-slate-50 border border-slate-200 rounded-lg pl-8 pr-3 py-1.5 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500 w-36 sm:w-44"
              value={searchTerm}
              onChange={(e) => onSearchChange(e.target.value)}
            />
          </div>

          {/* Date Range Inputs */}
          <div className="flex items-center gap-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1">
            <Calendar className="w-3.5 h-3.5 text-slate-400" />
            <input
              type="date"
              aria-label="Filter Start Date"
              className="bg-transparent text-slate-700 focus:outline-none text-xs cursor-pointer"
              value={startDate}
              min={minDate || undefined}
              max={maxDate || undefined}
              onChange={(e) => onStartDateChange(e.target.value)}
            />
            <span className="text-slate-400">to</span>
            <input
              type="date"
              aria-label="Filter End Date"
              className="bg-transparent text-slate-700 focus:outline-none text-xs cursor-pointer"
              value={endDate}
              min={minDate || undefined}
              max={maxDate || undefined}
              onChange={(e) => onEndDateChange(e.target.value)}
            />
          </div>

          {/* Category Chips */}
          <div className="flex flex-wrap items-center gap-1.5">
            {categories.slice(0, 6).map((cat) => {
              const isSelected = selectedCategories.includes(cat);
              return (
                <button
                  key={cat}
                  onClick={() => onToggleCategory(cat)}
                  className={`text-xs px-2.5 py-1 rounded-full font-medium transition ${
                    isSelected
                      ? 'bg-sky-600 text-white shadow-sm'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }`}
                >
                  {cat}
                </button>
              );
            })}
          </div>
        </div>

        {/* Right: Active Count & Reset */}
        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-500 font-medium">
            Showing <strong className="text-slate-900">{filteredCount}</strong> records
          </span>

          {hasActiveFilters && (
            <button
              onClick={onResetFilters}
              className="flex items-center gap-1 text-xs text-rose-600 hover:text-rose-700 font-medium bg-rose-50 hover:bg-rose-100 px-2.5 py-1 rounded-lg transition"
            >
              <X className="w-3.5 h-3.5" />
              <span>Clear</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
