import type { Thread } from '../../types';
import { ThreadItem } from './ThreadItem';
import { FileList } from './FileList';
import './Sidebar.css';

interface Props {
  threads: Thread[];
  activeThreadId: string | null;
  fileRefreshTrigger: number;
  onCreate: () => void;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
}

export function Sidebar({ threads, activeThreadId, fileRefreshTrigger, onCreate, onSelect, onDelete }: Props) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <span className="sidebar-logo">Hybrid RAG</span>
        <button className="new-chat-btn" onClick={onCreate} title="New chat">
          ＋
        </button>
      </div>

      <div className="thread-list">
        {threads.length === 0 && (
          <p className="no-threads">No chats yet. Start one!</p>
        )}
        {threads.map((thread) => (
          <div key={thread.thread_id}>
            <ThreadItem
              thread={thread}
              isActive={thread.thread_id === activeThreadId}
              onSelect={onSelect}
              onDelete={onDelete}
            />
            {thread.thread_id === activeThreadId && (
              <FileList threadId={thread.thread_id} refreshTrigger={fileRefreshTrigger} />
            )}
          </div>
        ))}
      </div>
    </aside>
  );
}
