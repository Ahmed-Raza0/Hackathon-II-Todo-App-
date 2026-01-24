from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # User who owns this message
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)