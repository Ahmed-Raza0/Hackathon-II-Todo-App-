import { apiClient } from '@/lib/api';

export interface ChatMessage {
  id?: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<any>;
  timestamp: string;
}

export class ChatService {
  static async sendMessage(userId: string, request: ChatRequest): Promise<ChatResponse> {
    return apiClient.post(`/api/${userId}/chat`, request);
  }

  static async getConversation(userId: string, conversationId: number): Promise<ChatMessage[]> {
    // This would typically be handled differently since messages are accessed through the chat endpoint
    // For now, we'll return an empty array since chat history is part of the conversation flow
    return [];
  }
}