import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Cell
} from 'recharts';
import { DayOfWeekPerformance } from '../types/api';
import { CalendarDays } from 'lucide-react';

interface DayOfWeekChartProps {
  data: DayOfWeekPerformance[];
}

export const DayOfWeekChart: React.FC<DayOfWeekChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-6 flex flex-col items-center justify-center h-80 text-slate-400">
        <CalendarDays className="w-8 h-8 mb-2 opacity-50" />
        <p className="text-sm">No weekday distribution data available.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
      <div className="mb-4">
        <h2 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <span>Day-of-Week Purchasing Patterns</span>
        </h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Turnover variation from Monday to Sunday
        </p>
      </div>

      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis
              dataKey="day_of_week"
              tick={{ fontSize: 11, fill: '#64748b' }}
              tickLine={false}
              axisLine={{ stroke: '#e2e8f0' }}
              tickFormatter={(d) => d.slice(0, 3)}
            />
            <YAxis
              tick={{ fontSize: 11, fill: '#64748b' }}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => `₹${v}`}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const d = payload[0].payload as DayOfWeekPerformance;
                  const isWeekend = d.day_of_week === 'Saturday' || d.day_of_week === 'Sunday';
                  return (
                    <div className="bg-slate-900 text-white rounded-lg p-3 text-xs shadow-xl border border-slate-800">
                      <div className="flex items-center justify-between gap-2 mb-1">
                        <strong className="text-slate-100">{d.day_of_week}</strong>
                        {isWeekend && (
                          <span className="text-[10px] bg-sky-950 text-sky-300 px-1.5 py-0.5 rounded border border-sky-800">
                            Weekend
                          </span>
                        )}
                      </div>
                      <div className="flex items-center justify-between gap-4 text-sky-400">
                        <span>Total Revenue:</span>
                        <strong className="text-white font-mono">₹{d.total_revenue.toLocaleString()}</strong>
                      </div>
                      <div className="flex items-center justify-between gap-4 text-emerald-400 mt-0.5">
                        <span>Daily Average:</span>
                        <strong className="text-white font-mono">₹{d.avg_daily_revenue.toLocaleString()}</strong>
                      </div>
                      <div className="flex items-center justify-between gap-4 text-indigo-400 mt-0.5">
                        <span>Transactions:</span>
                        <strong className="text-white font-mono">{d.record_count}</strong>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Bar
              dataKey="total_revenue"
              name="Gross Sales (₹)"
              radius={[4, 4, 0, 0]}
              barSize={24}
            >
              {data.map((entry) => {
                const isWeekend = entry.day_of_week === 'Saturday' || entry.day_of_week === 'Sunday';
                return (
                  <Cell
                    key={`dow-${entry.day_of_week}`}
                    fill={isWeekend ? '#0284c7' : '#94a3b8'}
                  />
                );
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
