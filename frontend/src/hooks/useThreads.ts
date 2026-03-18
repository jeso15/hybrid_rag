import { useState, useEffect } from 'react';
import type { Thread } from '../types';
import { createThread, listThreads, deleteThread } from '../api/threads';

export function useThreads() {
  const [threads, setThreads] = useState<Thread[]>([]);
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null);

  // Load threads on mount
  useEffect(() => {
    listThreads().then(setThreads).catch(console.error);
  }, []);

  async function handleCreate() {
    const thread = await createThread();
    setThreads((prev) => [thread, ...prev]);
    setActiveThreadId(thread.thread_id);
    return thread;
  }

  async function handleDelete(threadId: string) {
    await deleteThread(threadId);
    setThreads((prev) => prev.filter((t) => t.thread_id !== threadId));
    if (activeThreadId === threadId) {
      setActiveThreadId(null);
    }
  }

  function updateTitle(threadId: string, title: string) {
    setThreads((prev) =>
      prev.map((t) => (t.thread_id === threadId ? { ...t, title } : t))
    );
  }

  return {
    threads,
    activeThreadId,
    selectThread: setActiveThreadId,
    createThread: handleCreate,
    deleteThread: handleDelete,
    updateTitle,
  };
}
