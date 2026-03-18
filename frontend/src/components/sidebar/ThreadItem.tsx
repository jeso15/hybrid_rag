import type { Thread } from '../../types';
import './ThreadItem.css';

interface Props {
  thread: Thread;
  isActive: boolean;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
}

export function ThreadItem({ thread, isActive, onSelect, onDelete }: Props) {
  function handleDelete(e: React.MouseEvent) {
    e.stopPropagation();
    onDelete(thread.thread_id);
  }

  return (
    <div
      className={`thread-item ${isActive ? 'active' : ''}`}
      onClick={() => onSelect(thread.thread_id)}
    >
      <span className="thread-title">{thread.title}</span>
      <button className="thread-delete" onClick={handleDelete} title="Delete thread">
        ✕
      </button>
    </div>
  );
}
