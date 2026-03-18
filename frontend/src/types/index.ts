export interface Thread {
  thread_id: string;
  title: string;
  created_at: string;
}

export interface Source {
  text: string;
  metadata: Record<string, unknown>;
  score: number;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: Date;
}

export interface QueryResponse {
  answer: string;
  sources: Source[];
  thread_id: string;
}
