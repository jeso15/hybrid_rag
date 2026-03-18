import { useState, useRef, type KeyboardEvent } from 'react';
import './InputBar.css';

interface Props {
  onSend: (question: string, file?: File) => void;
  isLoading: boolean;
}

export function InputBar({ onSend, isLoading }: Props) {
  const [text, setText] = useState('');
  const [stagedFile, setStagedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  function handleSend() {
    const question = text.trim();
    if (!question && !stagedFile) return;
    onSend(question, stagedFile ?? undefined);
    setText('');
    setStagedFile(null);
    // Reset textarea height
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function handleTextChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
    setText(e.target.value);
    // Auto-resize up to 5 rows
    const el = e.target;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 140) + 'px';
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) setStagedFile(file);
    // Reset so same file can be re-selected
    e.target.value = '';
  }

  const canSend = !isLoading && (text.trim().length > 0 || stagedFile !== null);

  return (
    <div className="input-bar-wrapper">
      {stagedFile && (
        <div className="file-badge">
          <span>📄 {stagedFile.name}</span>
          <button onClick={() => setStagedFile(null)}>✕</button>
        </div>
      )}

      <div className="input-bar">
        <button
          className="upload-btn"
          onClick={() => fileInputRef.current?.click()}
          title="Upload PDF or Word file"
          disabled={isLoading}
        >
          ＋
        </button>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />

        <textarea
          ref={textareaRef}
          className="input-textarea"
          value={text}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question... (Shift+Enter for new line)"
          rows={1}
          disabled={isLoading}
        />

        <button
          className="send-btn"
          onClick={handleSend}
          disabled={!canSend}
          title="Send"
        >
          ↑
        </button>
      </div>

      <p className="input-hint">Enter to send · Shift+Enter for new line</p>
    </div>
  );
}
