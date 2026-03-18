import client from './client';
import type { QueryResponse } from '../types';

export async function sendQuery(threadId: string, question: string): Promise<QueryResponse> {
  const res = await client.post('/query', { thread_id: threadId, question });
  return res.data;
}

export async function uploadFile(threadId: string, file: File): Promise<{ num_chunks: number }> {
  const formData = new FormData();
  formData.append('file', file);
  const res = await client.post(`/threads/${threadId}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
}

export async function listFiles(threadId: string): Promise<{ filename: string; uploaded_at: string }[]> {
  const res = await client.get(`/threads/${threadId}/files`);
  return res.data;
}

export function getDownloadUrl(filename: string): string {
  return `http://localhost:8000/files/${encodeURIComponent(filename)}`;
}
