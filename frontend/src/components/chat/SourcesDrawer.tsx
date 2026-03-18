import { useState } from 'react';
import type { Source } from '../../types';
import './SourcesDrawer.css';

interface Props {
  sources: Source[];
}

export function SourcesDrawer({ sources }: Props) {
  const [open, setOpen] = useState(false);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="sources-drawer">
      <button className="sources-toggle" onClick={() => setOpen((o) => !o)}>
        {open ? '▾' : '▸'} {sources.length} source{sources.length > 1 ? 's' : ''}
      </button>

      {open && (
        <div className="sources-list">
          {sources.map((src, i) => (
            <div key={i} className="source-item">
              <div className="source-meta">
                <span className="source-file">
                  {(src.metadata?.source_file as string) || 'Unknown'}
                </span>
                <span className="source-score">
                  {src.score != null ? `${(src.score * 100).toFixed(0)}%` : ''}
                </span>
              </div>
              <p className="source-text">{src.text?.slice(0, 200)}…</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
