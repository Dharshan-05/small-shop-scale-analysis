import React, { useState } from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell
} from 'recharts';
import { ProductPerformance } from '../types/api';
import { Award } from 'lucide-react';

interface ProductPerformanceChartProps {
  products: ProductPerformance[];
}

const CATEGORY_COLORS: Record<string, string> = {
  Snacks: '#0284c7',
  Beverages: '#6366f1',
  Grocery: '#10b981',
  'Personal Care': '#f59e0b',
  Household: '#ec4899',
  General: '#64748b'
};

export const ProductPerformanceChart: React.FC<ProductPerformanceChartProps> = ({ products }) => {
  const [metric, setMetric] = useState<'revenue' | 'quantity'>('revenue');

  if (!products || products.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-6 flex flex-col items-center justify-center h-80 text-slate-400">
        <Award className="w-8 h-8 mb-2 opacity-50" />
        <p className="text-sm">No product sales recorded.</p>
      </div>
    );
  }

  // Sort based on selected metric and take top 8 for clean display
  const sorted = [...products].sort((a, b) =>
    metric === 'revenue' ? b.total_revenue - a.total_revenue : b.total_quantity - a.total_quantity
  ).slice(0, 8);

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <h2 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <span>Product Performance Rankings</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Comparative performance across SKUs (Top 8)
          </p>
        </div>

        {/* Metric Toggle */}
        <div className="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs">
          <button
            onClick={() => setMetric('revenue')}
            className={`px-2.5 py-1 rounded-md font-medium transition ${
              metric === 'revenue'
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            By Revenue (₹)
          </button>
          <button
            onClick={() => setMetric('quantity')}
            className={`px-2.5 py-1 rounded-md font-medium transition ${
              metric === 'quantity'
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            By Volume (Units)
          </button>
        </div>
      </div>

      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={sorted}
            layout="vertical"
            margin={{ top: 5, right: 20, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
            <XAxis
              type="number"
              tick={{ fontSize: 11, fill: '#64748b' }}
              tickLine={false}
              axisLine={{ stroke: '#e2e8f0' }}
              tickFormatter={(v) => (metric === 'revenue' ? `₹${v}` : `${v}`)}
            />
            <YAxis
              type="category"
              dataKey="product_name"
              tick={{ fontSize: 11, fill: '#334155', fontWeight: 500 }}
              tickLine={false}
              axisLine={false}
              width={85}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const p = payload[0].payload as ProductPerformance;
                  return (
                    <div className="bg-slate-900 text-white rounded-lg p-3 text-xs shadow-xl border border-slate-800">
                      <div className="font-semibold text-slate-100">{p.product_name}</div>
                      <div className="text-[10px] text-slate-400 mb-1">{p.product_category}</div>
                      <div className="flex items-center justify-between gap-4 text-sky-400">
                        <span>Gross Revenue:</span>
                        <strong className="text-white font-mono">₹{p.total_revenue.toLocaleString()}</strong>
                      </div>
                      <div className="flex items-center justify-between gap-4 text-indigo-400 mt-0.5">
                        <span>Units Sold:</span>
                        <strong className="text-white font-mono">{p.total_quantity.toLocaleString()}</strong>
                      </div>
                      <div className="flex items-center justify-between gap-4 text-emerald-400 mt-0.5">
                        <span>Revenue Share:</span>
                        <strong className="text-white font-mono">{p.revenue_share_pct}%</strong>
                      </div>
                      {p.unit_price_avg > 0 && (
                        <div className="flex items-center justify-between gap-4 text-slate-400 mt-0.5">
                          <span>Avg Unit Price:</span>
                          <strong className="text-white font-mono">₹{p.unit_price_avg.toLocaleString()}</strong>
                        </div>
                      )}
                    </div>
                  );
                }
                return null;
              }}
            />
            <Bar
              dataKey={metric === 'revenue' ? 'total_revenue' : 'total_quantity'}
              radius={[0, 4, 4, 0]}
              barSize={18}
            >
              {sorted.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={CATEGORY_COLORS[entry.product_category] || '#0ea5e9'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
