import React, { useState } from 'react';
import { ArrowUpDown, Download, Search, ChevronLeft, ChevronRight } from 'lucide-react';

interface DataTableProps {
  records: Record<string, any>[];
  onExport: () => void;
}

export const DataTable: React.FC<DataTableProps> = ({ records, onExport }) => {
  const [sortCol, setSortCol] = useState<string>('date');
  const [sortAsc, setSortAsc] = useState<boolean>(true);
  const [page, setPage] = useState<number>(1);
  const pageSize = 10;

  if (!records || records.length === 0) {
    return null;
  }

  const handleSort = (col: string) => {
    if (sortCol === col) {
      setSortAsc(!sortAsc);
    } else {
      setSortCol(col);
      setSortAsc(true);
    }
  };

  const sorted = [...records].sort((a, b) => {
    const valA = a[sortCol];
    const valB = b[sortCol];
    if (valA === valB) return 0;
    if (valA === undefined || valA === null) return 1;
    if (valB === undefined || valB === null) return -1;
    if (typeof valA === 'number' && typeof valB === 'number') {
      return sortAsc ? valA - valB : valB - valA;
    }
    return sortAsc
      ? String(valA).localeCompare(String(valB))
      : String(valB).localeCompare(String(valA));
  });

  const totalPages = Math.ceil(sorted.length / pageSize) || 1;
  const paginated = sorted.slice((page - 1) * pageSize, page * pageSize);

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm mb-8">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <h2 className="text-sm font-bold text-slate-900 tracking-tight">
            Cleaned Sales Transaction Records
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Verified line-item transactions ready for audit & export ({records.length} records)
          </p>
        </div>

        <button
          onClick={onExport}
          className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg font-medium bg-slate-100 hover:bg-slate-200 text-slate-800 transition"
        >
          <Download className="w-3.5 h-3.5 text-slate-600" />
          <span>Export Table to CSV</span>
        </button>
      </div>

      <div className="overflow-x-auto rounded-lg border border-slate-200">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <th
                onClick={() => handleSort('date')}
                className="py-2.5 px-3 cursor-pointer hover:bg-slate-100 transition"
              >
                <div className="flex items-center gap-1">
                  <span>Date</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>
              <th
                onClick={() => handleSort('day_of_week')}
                className="py-2.5 px-3 cursor-pointer hover:bg-slate-100 transition"
              >
                <div className="flex items-center gap-1">
                  <span>Day (Verified)</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>
              <th
                onClick={() => handleSort('product_category')}
                className="py-2.5 px-3 cursor-pointer hover:bg-slate-100 transition"
              >
                <div className="flex items-center gap-1">
                  <span>Category</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>
              <th
                onClick={() => handleSort('product_name')}
                className="py-2.5 px-3 cursor-pointer hover:bg-slate-100 transition"
              >
                <div className="flex items-center gap-1">
                  <span>Product Name</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>
              <th
                onClick={() => handleSort('quantity_sold')}
                className="py-2.5 px-3 cursor-pointer hover:bg-slate-100 transition text-right"
              >
                <div className="flex items-center justify-end gap-1">
                  <span>Quantity</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>
              <th
                onClick={() => handleSort('unit_price')}
                className="py-2.5 px-3 cursor-pointer hover:bg-slate-100 transition text-right"
              >
                <div className="flex items-center justify-end gap-1">
                  <span>Unit Price</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>
              <th
                onClick={() => handleSort('total_sales')}
                className="py-2.5 px-3 cursor-pointer hover:bg-slate-100 transition text-right"
              >
                <div className="flex items-center justify-end gap-1">
                  <span>Total Sales</span>
                  <ArrowUpDown className="w-3 h-3 text-slate-400" />
                </div>
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {paginated.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-50 transition">
                <td className="py-2.5 px-3 font-mono text-slate-600">{row.date}</td>
                <td className="py-2.5 px-3 font-medium text-slate-700">{row.day_of_week}</td>
                <td className="py-2.5 px-3">
                  <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-700">
                    {row.product_category}
                  </span>
                </td>
                <td className="py-2.5 px-3 font-semibold text-slate-900">{row.product_name}</td>
                <td className="py-2.5 px-3 font-mono text-right text-slate-800">
                  {Number(row.quantity_sold).toLocaleString()}
                </td>
                <td className="py-2.5 px-3 font-mono text-right text-slate-600">
                  {row.unit_price !== null && row.unit_price !== undefined
                    ? `₹${Number(row.unit_price).toFixed(2)}`
                    : '-'}
                </td>
                <td className="py-2.5 px-3 font-mono text-right font-bold text-sky-700">
                  ₹{Number(row.total_sales).toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination Bar */}
      <div className="flex items-center justify-between mt-3 text-xs text-slate-500">
        <div>
          Showing {(page - 1) * pageSize + 1} to{' '}
          {Math.min(page * pageSize, sorted.length)} of {sorted.length} entries
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="p-1 rounded border border-slate-200 disabled:opacity-30 hover:bg-slate-100 transition"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="px-2 font-medium text-slate-700">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="p-1 rounded border border-slate-200 disabled:opacity-30 hover:bg-slate-100 transition"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
