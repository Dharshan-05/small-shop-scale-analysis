import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Area,
  ComposedChart
} from 'recharts';
import { DailySalesTrend } from '../types/api';
import { TrendingUp } from 'lucide-react';

interface DailySalesChartProps {
  data: DailySalesTrend[];
}

export const DailySalesChart: React.FC<DailySalesChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-6 flex flex-col items-center justify-center h-80 text-slate-400">
        <TrendingUp className="w-8 h-8 mb-2 opacity-50" />
        <p className="text-sm">No daily sales data available for current selection.</p>
      </div>
    );
  }

  // Format date for chart display: DD-MM
  const chartData = data.map((d) => ({
    ...d,
    displayDate: d.date.length >= 10 ? d.date.slice(5) : d.date,
    dayLabel: `${d.date.slice(5)} (${d.day_of_week.slice(0, 3)})`
  }));

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <span>Daily Sales Trend</span>
            <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-sky-50 text-sky-700 border border-sky-200">
              Time Series
            </span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Turnover (₹) and transaction velocity across the reporting period
          </p>
        </div>
      </div>

      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
            <defs>
              <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#0284c7" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#0284c7" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis
              dataKey="dayLabel"
              tick={{ fontSize: 11, fill: '#64748b' }}
              tickLine={false}
              axisLine={{ stroke: '#e2e8f0' }}
            />
            <YAxis
              yAxisId="left"
              tick={{ fontSize: 11, fill: '#64748b' }}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => `₹${v}`}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              tick={{ fontSize: 11, fill: '#94a3b8' }}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  const item = payload[0].payload as DailySalesTrend;
                  return (
                    <div className="bg-slate-900 text-white rounded-lg p-3 text-xs shadow-xl border border-slate-800">
                      <div className="font-semibold text-slate-200 mb-1">
                        {item.date} ({item.day_of_week})
                      </div>
                      <div className="flex items-center justify-between gap-4 text-sky-400">
                        <span>Total Revenue:</span>
                        <strong className="text-white font-mono">₹{item.total_revenue.toLocaleString()}</strong>
                      </div>
                      <div className="flex items-center justify-between gap-4 text-indigo-400 mt-0.5">
                        <span>Quantity Sold:</span>
                        <strong className="text-white font-mono">{item.total_quantity.toLocaleString()} units</strong>
                      </div>
                      <div className="flex items-center justify-between gap-4 text-slate-400 mt-0.5">
                        <span>Transactions:</span>
                        <strong className="text-white font-mono">{item.transaction_count}</strong>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }}
              iconType="circle"
            />
            <Area
              yAxisId="left"
              type="monotone"
              dataKey="total_revenue"
              name="Revenue (₹)"
              fill="url(#revenueGrad)"
              stroke="#0284c7"
              strokeWidth={2.5}
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="total_quantity"
              name="Units Sold"
              stroke="#6366f1"
              strokeWidth={1.5}
              dot={{ r: 3, fill: '#6366f1' }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
