import client from './client';
import type { Thread } from '../types';

export async function createThread(): Promise<Thread> {
  const res = await client.post('/threads');
  return res.data;
}

export async function listThreads(): Promise<Thread[]> {
  const res = await client.get('/threads');
  return res.data;
}

export async function deleteThread(threadId: string): Promise<void> {
  await client.delete(`/threads/${threadId}`);
}
