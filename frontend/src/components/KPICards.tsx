import React from 'react';
import { IndianRupee, ShoppingBag, Receipt, Calendar, TrendingUp, Award, AlertCircle } from 'lucide-react';
import { SalesSummaryKPIs } from '../types/api';

interface KPICardsProps {
  kpis: SalesSummaryKPIs;
}

export const KPICards: React.FC<KPICardsProps> = ({ kpis }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4 mb-6">
      {/* Total Revenue */}
      <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm hover:border-sky-300 transition group">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Total Revenue
          </span>
          <div className="p-2 rounded-lg bg-sky-50 text-sky-600 group-hover:bg-sky-600 group-hover:text-white transition">
            <IndianRupee className="w-4 h-4" />
          </div>
        </div>
        <div className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
          ₹{kpis.total_revenue.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </div>
        <div className="text-[11px] text-slate-500 mt-1">
          {kpis.total_records} transactions recorded
        </div>
      </div>

      {/* Total Quantity Sold */}
      <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm hover:border-indigo-300 transition group">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Units Sold
          </span>
          <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition">
            <ShoppingBag className="w-4 h-4" />
          </div>
        </div>
        <div className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
          {kpis.total_quantity_sold.toLocaleString()}
        </div>
        <div className="text-[11px] text-slate-500 mt-1">
          Across {kpis.unique_products} distinct SKUs
        </div>
      </div>

      {/* Average Daily Sales */}
      <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm hover:border-emerald-300 transition group">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Daily Average
          </span>
          <div className="p-2 rounded-lg bg-emerald-50 text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition">
            <Calendar className="w-4 h-4" />
          </div>
        </div>
        <div className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
          ₹{kpis.avg_revenue_per_day.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </div>
        <div className="text-[11px] text-slate-500 mt-1">
          Over {kpis.unique_days} active trading days
        </div>
      </div>

      {/* Average Transaction Value */}
      <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm hover:border-violet-300 transition group">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Avg Order / Line
          </span>
          <div className="p-2 rounded-lg bg-violet-50 text-violet-600 group-hover:bg-violet-600 group-hover:text-white transition">
            <Receipt className="w-4 h-4" />
          </div>
        </div>
        <div className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
          ₹{kpis.avg_revenue_per_record.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </div>
        <div className="text-[11px] text-slate-500 mt-1">
          In {kpis.unique_categories} categories
        </div>
      </div>

      {/* Top Product by Revenue */}
      <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm hover:border-amber-300 transition group">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Revenue Leader
          </span>
          <div className="p-2 rounded-lg bg-amber-50 text-amber-600 group-hover:bg-amber-600 group-hover:text-white transition">
            <Award className="w-4 h-4" />
          </div>
        </div>
        <div className="text-base sm:text-lg font-bold text-slate-900 truncate" title={kpis.best_selling_by_revenue?.name}>
          {kpis.best_selling_by_revenue?.name || 'N/A'}
        </div>
        <div className="text-[11px] text-amber-700 font-medium mt-1">
          {kpis.best_selling_by_revenue ? `₹${kpis.best_selling_by_revenue.value.toLocaleString()} (${kpis.best_selling_by_revenue.category})` : 'No data'}
        </div>
      </div>

      {/* Volume Leader or Lowest Contributor */}
      <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm hover:border-rose-300 transition group">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Volume Leader
          </span>
          <div className="p-2 rounded-lg bg-rose-50 text-rose-600 group-hover:bg-rose-600 group-hover:text-white transition">
            <TrendingUp className="w-4 h-4" />
          </div>
        </div>
        <div className="text-base sm:text-lg font-bold text-slate-900 truncate" title={kpis.best_selling_by_quantity?.name}>
          {kpis.best_selling_by_quantity?.name || 'N/A'}
        </div>
        <div className="text-[11px] text-rose-700 font-medium mt-1">
          {kpis.best_selling_by_quantity ? `${kpis.best_selling_by_quantity.value.toLocaleString()} Units (${kpis.best_selling_by_quantity.category})` : 'No data'}
        </div>
      </div>
    </div>
  );
};
