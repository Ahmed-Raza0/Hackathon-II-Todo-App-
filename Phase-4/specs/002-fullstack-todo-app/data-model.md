# Data Model: Full-Stack Todo Application

## Entities

### User
Represents a registered user with authentication credentials managed by Better Auth

**Attributes:**
- `id`: string, Primary Key (assigned by Better Auth)
- `email`: string, unique (assigned by Better Auth)
- `name`: string (assigned by Better Auth)
- `created_at`: timestamp (assigned by Better Auth)

**Relationships:**
- One-to-many with Task (user has many tasks)
- One-to-many with Conversation (user has many conversations)
- One-to-many with Message (user has many messages)

**Validation:**
- Email must be valid email format
- Name must be 1-100 characters

### Task
Represents a user's todo item

**Attributes:**
- `id`: integer, Primary Key
- `user_id`: string, Foreign Key → User.id
- `title`: string, not null
- `description`: text, nullable
- `completed`: boolean, default false
- `created_at`: timestamp
- `updated_at`: timestamp

**Relationships:**
- Many-to-one with User (many tasks belong to one user)

**Validation:**
- Title: 1-200 characters
- Description: max 1000 characters
- user_id must reference existing user

**State Transitions:**
- Pending (completed: false) ↔ Completed (completed: true)

### Conversation
Represents a chat session between user and AI assistant

**Attributes:**
- `id`: integer, Primary Key
- `user_id`: string, Foreign Key → User.id
- `created_at`: timestamp
- `updated_at`: timestamp

**Relationships:**
- Many-to-one with User (many conversations belong to one user)
- One-to-many with Message (conversation has many messages)

**Validation:**
- user_id must reference existing user

### Message
Represents an individual message in a conversation

**Attributes:**
- `id`: integer, Primary Key
- `user_id`: string, Foreign Key → User.id
- `conversation_id`: integer, Foreign Key → Conversation.id
- `role`: enum('user', 'assistant')
- `content`: text
- `created_at`: timestamp

**Relationships:**
- Many-to-one with User (many messages belong to one user)
- Many-to-one with Conversation (many messages belong to one conversation)

**Validation:**
- user_id must reference existing user
- conversation_id must reference existing conversation
- role must be either 'user' or 'assistant'
- content must be 1-5000 characters

## Database Schema

### Tables
```
users (managed by Better Auth)
├── id (string, PK)
├── email (string, unique)
├── name (string)
└── created_at (timestamp)

tasks
├── id (integer, PK)
├── user_id (string, FK → users.id)
├── title (string, not null)
├── description (text, nullable)
├── completed (boolean, default false)
├── created_at (timestamp)
└── updated_at (timestamp)

conversations
├── id (integer, PK)
├── user_id (string, FK → users.id)
├── created_at (timestamp)
└── updated_at (timestamp)

messages
├── id (integer, PK)
├── user_id (string, FK → users.id)
├── conversation_id (integer, FK → conversations.id)
├── role (enum: user/assistant)
├── content (text)
└── created_at (timestamp)
```

### Indexes
- `tasks.user_id` - for filtering tasks by user
- `tasks.completed` - for filtering tasks by status
- `conversations.user_id` - for filtering conversations by user
- `messages.conversation_id` - for retrieving messages in conversation order
- `messages.user_id` - for filtering messages by user

## Business Rules
1. Users can only access their own tasks
2. Users can only access their own conversations
3. Users can only access messages in their own conversations
4. Tasks must be associated with a valid user
5. Messages must be associated with a valid conversation and user