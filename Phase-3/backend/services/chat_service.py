from typing import Optional, Dict, Any, List
from sqlmodel import Session, select
from models import Conversation, Message
from tools.task_tools import TaskMCPTools
from datetime import datetime


class ChatService:
    """Service class for chat-related operations"""

    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
            user_id=user_id
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation(session: Session, conversation_id: int, user_id: str) -> Optional[Conversation]:
        """Get a specific conversation for a user"""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def get_all_conversations(session: Session, user_id: str) -> List[Conversation]:
        """Get all conversations for a user"""
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.created_at.desc())
        return list(session.exec(statement).all())

    @staticmethod
    def delete_conversation(session: Session, conversation_id: int, user_id: str) -> bool:
        """Delete a conversation"""
        conversation = ChatService.get_conversation(session, conversation_id, user_id)
        if not conversation:
            return False
        
        # Delete all messages in the conversation
        statement = select(Message).where(Message.conversation_id == conversation_id)
        messages = session.exec(statement).all()
        for message in messages:
            session.delete(message)
        
        # Delete the conversation
        session.delete(conversation)
        session.commit()
        return True

    @staticmethod
    def get_messages_for_conversation(session: Session, conversation_id: int, user_id: str) -> List[Message]:
        """Get all messages for a specific conversation"""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
        return list(session.exec(statement).all())

    @staticmethod
    def add_message(session: Session, user_id: str, conversation_id: int, role: str, content: str) -> Message:
        """Add a message to a conversation"""
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def process_chat_message(
        session: Session, 
        user_id: str, 
        message_content: str, 
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Process a chat message and return response with tool calls"""
        # Get or create conversation
        if conversation_id:
            conversation = ChatService.get_conversation(session, conversation_id, user_id)
            if not conversation:
                return {
                    "success": False,
                    "error": "Conversation not found"
                }
        else:
            conversation = ChatService.create_conversation(session, user_id)

        # Add user message
        user_message = ChatService.add_message(
            session, user_id, conversation.id, "user", message_content
        )

        # Process with AI and tools
        response_text, tool_calls = ChatService._process_with_ai_and_tools(
            message_content, session, user_id
        )

        # Add assistant message
        assistant_message = ChatService.add_message(
            session, user_id, conversation.id, "assistant", response_text
        )

        return {
            "success": True,
            "conversation_id": conversation.id,
            "response": response_text,
            "tool_calls": tool_calls,
            "user_message_id": user_message.id,
            "assistant_message_id": assistant_message.id
        }

    @staticmethod
    def _process_with_ai_and_tools(
        message: str, 
        session: Session, 
        user_id: str
    ) -> tuple[str, List[Dict[str, Any]]]:
        """Internal method to process message with AI and tool calls"""
        message_lower = message.lower()
        tool_calls = []

        # Handle task-related commands
        if "add task" in message_lower or "create task" in message_lower:
            # Extract task title from message
            task_title = ""
            if "add task" in message_lower:
                task_parts = message_lower.split("add task", 1)
                if len(task_parts) > 1:
                    task_title = task_parts[1].strip()
            elif "create task" in message_lower:
                task_parts = message_lower.split("create task", 1)
                if len(task_parts) > 1:
                    task_title = task_parts[1].strip()

            # Clean up the task title
            task_title = task_title.strip('"').strip("'").strip()

            if task_title:
                # Call add_task MCP tool
                result = TaskMCPTools.add_task(session, user_id, task_title)
                tool_calls.append({
                    "name": "add_task",
                    "arguments": {"title": task_title},
                    "result": result
                })

                if result["success"]:
                    response = f"I've created a task for you: '{result['task']['title']}'"
                else:
                    response = f"Sorry, I couldn't create the task: {result['error']}"
            else:
                response = "I need a title for the task you want to create."

        elif "show tasks" in message_lower or "list tasks" in message_lower or "my tasks" in message_lower:
            # Determine status filter
            status_filter = "all"
            if "completed" in message_lower:
                status_filter = "completed"
            elif "pending" in message_lower:
                status_filter = "pending"

            # Call list_tasks MCP tool
            result = TaskMCPTools.list_tasks(session, user_id, status_filter)
            tool_calls.append({
                "name": "list_tasks",
                "arguments": {"status": status_filter},
                "result": result
            })

            if result["success"]:
                if result["count"] == 0:
                    response = "You don't have any tasks."
                else:
                    task_list = [f"- {task['title']}" for task in result["tasks"]]
                    response = f"You have {result['count']} tasks:\n" + "\n".join(task_list)
            else:
                response = f"Sorry, I couldn't retrieve your tasks: {result['error']}"

        elif "complete task" in message_lower or "mark task" in message_lower:
            response = "I'd need more information to mark a specific task as complete. Please tell me which task by name or ID."

        elif "hello" in message_lower or "hi" in message_lower:
            response = "Hello! I'm your AI assistant. You can ask me to create, list, or manage your tasks."
        
        else:
            response = f"I received your message: '{message}'. You can ask me to create or manage tasks. Try saying 'create task Buy groceries' or 'list my tasks'."

        return response, tool_calls