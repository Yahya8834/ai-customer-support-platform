# Application Boundaries

## Purpose

The project is divided into independent Django apps.

Each app owns a single business domain and exposes a small public API through
services and selectors. Other apps should avoid depending directly on internal
implementation details.

The goals are:

- Separation of concerns
- Low coupling
- High cohesion
- Easier testing
- Easier onboarding
- Parallel development

---

# Dependency Rules

Dependencies should flow in one direction only.

```
accounts
    ↓
workspaces
    ↓
documents
    ↓
chat
    ↓
ai
```

The `common` app is shared and may be imported by every app.

Apps should never create circular dependencies.

---

# Public API

Every app should expose only:

- services/
- selectors/
- constants/
- events/ (future)

Other apps should avoid importing:

- models
- serializers
- views
- internal utilities

Good:

```python
from apps.documents.services.create_document import CreateDocumentService
```

Good:

```python
from apps.chat.selectors.get_chat import get_chat
```

Avoid:

```python
from apps.chat.models import Chat
```

unless there is a very strong reason.

---

# App Responsibilities

## accounts

Responsible for:

- Authentication
- User registration
- JWT
- User profile

Owns:

- User model

Does NOT know about:

- AI
- Documents
- Chats

---

## workspaces

Responsible for:

- Workspace creation
- Workspace membership
- Roles
- Permissions

Owns:

- Workspace
- Membership

May use:

- accounts.User

Does NOT know about:

- AI implementation

---

## documents

Responsible for:

- Uploaded documents
- File storage
- Metadata
- Parsing status

Owns:

- Document

Uses:

- Workspace

Does NOT know:

- Chat logic

---

## chat

Responsible for:

- Conversations
- Messages
- Conversation history

Owns:

- Chat
- Message

Uses:

- Workspace
- Documents (read-only)

Does NOT know:

- LLM implementation

---

## ai

Responsible for:

- LLM providers
- Prompt building
- Embeddings
- Retrieval
- Response generation

Owns:

- AI orchestration

Uses:

- Chat
- Documents

Never owns business entities.

---

## common

Responsible for:

- Exceptions
- Utilities
- Shared base classes
- Shared API helpers

Should contain no business logic.

---

# Communication Between Apps

Business logic should be accessed through services.

Example:

```
Chat API
    ↓
CreateMessageService
    ↓
AIService
    ↓
DocumentSelector
```

Each layer communicates through well-defined interfaces.

---

# Development Guidelines

A developer should be able to work on one app without modifying another.

Changes inside an app should not break unrelated apps if public interfaces
remain unchanged.

When introducing new features:

1. Decide which app owns the feature.
2. Keep business rules inside that app.
3. Expose only the minimum public interface required by other apps.