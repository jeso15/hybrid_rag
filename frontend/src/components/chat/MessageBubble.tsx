import type { Message } from '../../types';
import { SourcesDrawer } from './SourcesDrawer';
import { getDownloadUrl } from '../../api/messages';
import './MessageBubble.css';

interface Props {
  message: Message;
}

// Renders message content, turning [File: filename.pdf] into a download link
function renderContent(content: string) {
  const parts = content.split(/(\[File: [^\]]+\])/g);

  return parts.map((part, i) => {
    const match = part.match(/^\[File: (.+)\]$/);
    if (match) {
      const filename = match[1];
      return (
        <a
          key={i}
          href={getDownloadUrl(filename)}
          download={filename}
          className="file-link"
          title={`Download ${filename}`}
        >
          📄 {filename}
        </a>
      );
    }
    return <span key={i}>{part}</span>;
  });
}

export function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user';

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      <div className="bubble-label">{isUser ? 'You' : 'Assistant'}</div>
      <div className="bubble-content">
        <p>{renderContent(message.content)}</p>
        {!isUser && message.sources && (
          <SourcesDrawer sources={message.sources} />
        )}
      </div>
    </div>
  );
}
