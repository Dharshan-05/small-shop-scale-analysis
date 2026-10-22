import {
  SalesAnalyticsResponse,
  SampleDatasetMeta,
  UploadPreviewResponse,
  ColumnMappingConfig
} from '../types/api';

const API_BASE = '/api';

export async function fetchHealth(): Promise<{ status: string; app: string; version: string }> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Backend health check failed');
  return res.json();
}

export async function fetchSamples(): Promise<SampleDatasetMeta[]> {
  const res = await fetch(`${API_BASE}/samples`);
  if (!res.ok) throw new Error('Failed to load sample dataset list');
  return res.json();
}

export async function fetchSampleAnalysis(
  sampleId: string,
  params?: {
    startDate?: string;
    endDate?: string;
    categories?: string[];
    products?: string[];
  }
): Promise<SalesAnalyticsResponse> {
  const query = new URLSearchParams();
  if (params?.startDate) query.set('start_date', params.startDate);
  if (params?.endDate) query.set('end_date', params.endDate);
  if (params?.categories) {
    params.categories.forEach((c) => query.append('categories', c));
  }
  if (params?.products) {
    params.products.forEach((p) => query.append('products', p));
  }

  const qs = query.toString();
  const url = `${API_BASE}/samples/${sampleId}/analyze${qs ? `?${qs}` : ''}`;
  const res = await fetch(url);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Analysis failed' }));
    throw new Error(err.detail || 'Analysis request failed');
  }
  return res.json();
}

export async function uploadPreview(file: File): Promise<UploadPreviewResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/upload/preview`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Preview upload failed' }));
    throw new Error(err.detail || 'Preview upload failed');
  }
  return res.json();
}

export async function uploadAndAnalyze(
  file: File,
  mapping: ColumnMappingConfig,
  params?: {
    startDate?: string;
    endDate?: string;
    categories?: string[];
    products?: string[];
  }
): Promise<SalesAnalyticsResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('mapping', JSON.stringify(mapping));
  if (params?.startDate) formData.append('start_date', params.startDate);
  if (params?.endDate) formData.append('end_date', params.endDate);
  if (params?.categories) formData.append('categories', JSON.stringify(params.categories));
  if (params?.products) formData.append('products', JSON.stringify(params.products));

  const res = await fetch(`${API_BASE}/upload/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'File analysis failed' }));
    throw new Error(err.detail || 'File analysis failed');
  }
  return res.json();
}

export async function exportSampleFullCSV(
  sampleId: string,
  params?: {
    startDate?: string;
    endDate?: string;
    categories?: string[];
    products?: string[];
  }
): Promise<Blob> {
  const query = new URLSearchParams();
  if (params?.startDate) query.set('start_date', params.startDate);
  if (params?.endDate) query.set('end_date', params.endDate);
  if (params?.categories) {
    params.categories.forEach((c) => query.append('categories', c));
  }
  if (params?.products) {
    params.products.forEach((p) => query.append('products', p));
  }

  const qs = query.toString();
  const res = await fetch(`${API_BASE}/samples/${sampleId}/export${qs ? `?${qs}` : ''}`);
  if (!res.ok) {
    throw new Error('Failed to export full dataset CSV');
  }
  return res.blob();
}

export async function exportUploadFullCSV(
  file: File,
  mapping: ColumnMappingConfig,
  params?: {
    startDate?: string;
    endDate?: string;
    categories?: string[];
    products?: string[];
  }
): Promise<Blob> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('mapping', JSON.stringify(mapping));
  if (params?.startDate) formData.append('start_date', params.startDate);
  if (params?.endDate) formData.append('end_date', params.endDate);
  if (params?.categories) formData.append('categories', JSON.stringify(params.categories));
  if (params?.products) formData.append('products', JSON.stringify(params.products));

  const res = await fetch(`${API_BASE}/upload/export`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    throw new Error('Failed to export uploaded dataset CSV');
  }
  return res.blob();
}
