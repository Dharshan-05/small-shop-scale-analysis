import React from 'react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend
} from 'recharts';
import { CategoryPerformance } from '../types/api';
import { PieChart as PieIcon } from 'lucide-react';

interface CategoryPieChartProps {
  categories: CategoryPerformance[];
}

const COLORS = ['#0284c7', '#6366f1', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#64748b'];

export const CategoryPieChart: React.FC<CategoryPieChartProps> = ({ categories }) => {
  if (!categories || categories.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-6 flex flex-col items-center justify-center h-80 text-slate-400">
        <PieIcon className="w-8 h-8 mb-2 opacity-50" />
        <p className="text-sm">No category breakdown available.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
      <div className="mb-4">
        <h2 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <span>Category Sales Contribution</span>
        </h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Revenue proportion across merchandise departments
        </p>
      </div>

      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={categories}
              dataKey="total_revenue"
              nameKey="product_category"
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={85}
              paddingAngle={3}
            >
              {categories.map((_, index) => (
                <Cell key={`cat-cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const c = payload[0].payload as CategoryPerformance;
                  return (
                    <div className="bg-slate-900 text-white rounded-lg p-3 text-xs shadow-xl border border-slate-800">
                      <div className="font-semibold text-slate-100">{c.product_category}</div>
                      <div className="flex items-center justify-between gap-4 text-sky-400 mt-1">
                        <span>Revenue:</span>
                        <strong className="text-white font-mono">₹{c.total_revenue.toLocaleString()}</strong>
                      </div>
                      <div className="flex items-center justify-between gap-4 text-emerald-400 mt-0.5">
                        <span>Share:</span>
                        <strong className="text-white font-mono">{c.revenue_share_pct}%</strong>
                      </div>
                      <div className="flex items-center justify-between gap-4 text-slate-400 mt-0.5">
                        <span>Units Sold:</span>
                        <strong className="text-white font-mono">{c.total_quantity.toLocaleString()}</strong>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Legend
              layout="horizontal"
              verticalAlign="bottom"
              align="center"
              wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }}
              iconType="circle"
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
