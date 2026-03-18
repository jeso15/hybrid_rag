import { useChat } from '../../hooks/useChat';
import { MessageList } from './MessageList';
import { InputBar } from '../input/InputBar';
import type { Message } from '../../types';
import './ChatPanel.css';

interface Props {
  threadId: string;
  messages: Message[];
  setMessages: (threadId: string, updater: (prev: Message[]) => Message[]) => void;
  onTitleUpdate: (id: string, title: string) => void;
  onFileUploaded: (trigger: number) => void;
}

export function ChatPanel({ threadId, messages, setMessages, onTitleUpdate, onFileUploaded }: Props) {
  const { isLoading, error, sendMessage, fileRefreshTrigger } = useChat(
    threadId,
    messages,
    setMessages,
    onTitleUpdate,
  );

  // Notify parent when a file is uploaded
  if (fileRefreshTrigger > 0) {
    onFileUploaded(fileRefreshTrigger);
  }

  return (
    <div className="chat-panel">
      <MessageList messages={messages} isLoading={isLoading} />

      {error && (
        <div className="chat-error">{error}</div>
      )}

      <InputBar onSend={sendMessage} isLoading={isLoading} />
    </div>
  );
}
