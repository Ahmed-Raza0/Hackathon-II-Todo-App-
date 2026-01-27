from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from database import get_session
from auth import get_current_user
from models import Message, Conversation
from services.chat_service import ChatService
from datetime import datetime


class MessageRequest(BaseModel):
    message: str


class ConversationCreate(BaseModel):
    pass  # No fields needed since we're not using title


router = APIRouter(prefix="/chat")


@router.post("/conversations")
def create_conversation(
    data: ConversationCreate,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Create a new conversation"""
    print(f"📝 Creating conversation for user: {current_user}")
    
    conversation = ChatService.create_conversation(session, current_user)
    
    print(f"✅ Conversation created with ID: {conversation.id}")
    
    # Return in the exact format the frontend expects
    return {
        "id": conversation.id,
        "user_id": conversation.user_id,
        "created_at": conversation.created_at.isoformat() if conversation.created_at else datetime.utcnow().isoformat(),
        "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else datetime.utcnow().isoformat()
    }


@router.get("/conversations")
def list_conversations(
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Get all conversations for the current user"""
    conversations = ChatService.get_all_conversations(session, current_user)
    return conversations


@router.get("/conversations/{conversation_id}")
def get_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Get a specific conversation"""
    conversation = ChatService.get_conversation(session, conversation_id, current_user)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return conversation


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Delete a conversation"""
    success = ChatService.delete_conversation(session, conversation_id, current_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return {"message": "Conversation deleted successfully"}


@router.get("/conversations/{conversation_id}/messages")
def get_messages(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Get all messages in a conversation"""
    print(f"📖 Getting messages for conversation: {conversation_id}")
    
    # Verify conversation belongs to user
    conversation = ChatService.get_conversation(session, conversation_id, current_user)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = ChatService.get_messages_for_conversation(session, conversation_id, current_user)
    return messages


@router.post("/conversations/{conversation_id}/messages")
def send_message(
    conversation_id: int,
    request: MessageRequest,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Send a message in a conversation"""
    print(f"💬 Sending message to conversation: {conversation_id}")
    print(f"💬 Message content: {request.message}")
    
    # Verify conversation belongs to user
    conversation = ChatService.get_conversation(session, conversation_id, current_user)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Process the message
    result = ChatService.process_chat_message(
        session, 
        current_user, 
        request.message, 
        conversation_id
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to process message")
        )
    
    print(f"✅ Message processed successfully")
    
    return {
        "conversation_id": result["conversation_id"],
        "response": result["response"],
        "timestamp": datetime.utcnow().isoformat()
    }