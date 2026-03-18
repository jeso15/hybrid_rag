import { useEffect, useState } from 'react';
import { listFiles, getDownloadUrl } from '../../api/messages';
import './FileList.css';

interface Props {
  threadId: string;
  refreshTrigger: number;
}

export function FileList({ threadId, refreshTrigger }: Props) {
  const [files, setFiles] = useState<{ filename: string; uploaded_at: string }[]>([]);

  useEffect(() => {
    listFiles(threadId).then(setFiles).catch(() => setFiles([]));
  }, [threadId, refreshTrigger]);

  if (files.length === 0) return null;

  return (
    <div className="file-list">
      <p className="file-list-label">Files</p>
      {files.map((f) => (
        <a
          key={f.filename}
          className="file-item"
          href={getDownloadUrl(f.filename)}
          download={f.filename}
          title={`Download ${f.filename}`}
        >
          <span className="file-icon">📄</span>
          <span className="file-name">{f.filename}</span>
          <span className="file-download">↓</span>
        </a>
      ))}
    </div>
  );
}
