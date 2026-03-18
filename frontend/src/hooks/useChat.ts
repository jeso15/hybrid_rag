import { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import type { Message } from '../types';
import { sendQuery, uploadFile } from '../api/messages';

export function useChat(
  threadId: string | null,
  messages: Message[],
  setMessages: (threadId: string, updater: (prev: Message[]) => Message[]) => void,
  onTitleUpdate?: (id: string, title: string) => void,
) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileRefreshTrigger, setFileRefreshTrigger] = useState(0);

  async function sendMessage(question: string, file?: File) {
    if (!threadId) return;
    setError(null);
    setIsLoading(true);

    // Add user message optimistically
    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content: file ? `[File: ${file.name}]\n${question}` : question,
      timestamp: new Date(),
    };
    setMessages(threadId, (prev) => [...prev, userMessage]);

    try {
      // Upload file first if provided
      if (file) {
        await uploadFile(threadId, file);
        setFileRefreshTrigger((n) => n + 1);
      }

      // Send query
      const response = await sendQuery(threadId, question);

      const assistantMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date(),
      };
      setMessages(threadId, (prev) => [...prev, assistantMessage]);

      // Update thread title from first question
      if (messages.length === 0 && onTitleUpdate) {
        onTitleUpdate(threadId, question.slice(0, 50));
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Something went wrong.';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }

  return { messages, isLoading, error, sendMessage, fileRefreshTrigger };
}
