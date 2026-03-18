import './EmptyState.css';

interface Props {
  onCreate: () => void;
}

export function EmptyState({ onCreate }: Props) {
  return (
    <div className="empty-state">
      <div className="empty-icon">⬡</div>
      <h2>Hybrid RAG</h2>
      <p>Upload a PDF or Word document and ask questions about it.</p>
      <button className="empty-start-btn" onClick={onCreate}>
        Start a new chat
      </button>
    </div>
  );
}
