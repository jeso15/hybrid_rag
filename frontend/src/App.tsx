import { useState } from 'react';
import { useThreads } from './hooks/useThreads';
import { Sidebar } from './components/sidebar/Sidebar';
import { ChatPanel } from './components/chat/ChatPanel';
import { EmptyState } from './components/chat/EmptyState';
import type { Message } from './types';
import './App.css';

export default function App() {
  const { threads, activeThreadId, selectThread, createThread, deleteThread, updateTitle } = useThreads();
  const [fileRefreshTrigger, setFileRefreshTrigger] = useState(0);

  // Per-thread message history — survives tab switching
  const [messagesByThread, setMessagesByThread] = useState<Record<string, Message[]>>({});

  function setMessages(threadId: string, updater: (prev: Message[]) => Message[]) {
    setMessagesByThread((prev) => ({
      ...prev,
      [threadId]: updater(prev[threadId] ?? []),
    }));
  }

  const activeMessages = activeThreadId ? (messagesByThread[activeThreadId] ?? []) : [];

  return (
    <div className="app-layout">
      <Sidebar
        threads={threads}
        activeThreadId={activeThreadId}
        fileRefreshTrigger={fileRefreshTrigger}
        onCreate={createThread}
        onSelect={selectThread}
        onDelete={deleteThread}
      />

      <main className="app-main">
        {activeThreadId ? (
          <ChatPanel
            key={activeThreadId}
            threadId={activeThreadId}
            messages={activeMessages}
            setMessages={setMessages}
            onTitleUpdate={updateTitle}
            onFileUploaded={setFileRefreshTrigger}
          />
        ) : (
          <EmptyState onCreate={createThread} />
        )}
      </main>
    </div>
  );
}
