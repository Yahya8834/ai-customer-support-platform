Documents App

Purpose

The Documents app manages all PDF documents that belong to a workspace. It provides the foundation for the AI support assistant by storing uploaded documentation that will later be processed into searchable knowledge.

The app is intentionally responsible only for document management. AI processing, embeddings, retrieval, and conversations are handled by separate applications.

⸻

Responsibilities

The Documents app is responsible for:

* Uploading PDF documents
* Listing workspace documents
* Retrieving document details
* Deleting documents
* Restricting access to workspace members
* Restricting document deletion to workspace owners

The app is not responsible for:

* Parsing PDFs
* Chunking text
* Generating embeddings
* Semantic search
* AI conversations

⸻

API Endpoints

Method	Endpoint	Description
GET	/api/v1/workspaces/{workspace_uuid}/documents/	List workspace documents
POST	/api/v1/workspaces/{workspace_uuid}/documents/	Upload a PDF document
GET	/api/v1/workspaces/{workspace_uuid}/documents/{document_uuid}/	Retrieve a document
DELETE	/api/v1/workspaces/{workspace_uuid}/documents/{document_uuid}/	Delete a document

⸻

Authorization

Workspace members may:

* List documents
* Retrieve document details
* Upload PDF documents

Workspace owners may additionally:

* Delete documents

Non-members cannot access any document within the workspace.

⸻

Validation

Current validation rules:

* Only PDF files are accepted.
* The uploader must belong to the workspace.
* The workspace must exist.
* The document must belong to the requested workspace.

⸻

Architecture

The app follows the same layered architecture used throughout the project.

APIView
    │
    ▼
Service / Selector
    │
    ▼
Models

Services

Services perform operations that modify data.

Current services:

* UploadDocumentService
* DeleteDocumentService

Selectors

Selectors perform read-only operations.

Current selectors:

* list_workspace_documents()
* get_document()

Keeping reads and writes separate makes business logic easier to maintain and test.

⸻

Public Identifiers

The API exposes UUIDs exclusively.

Internal database implementation details are hidden from API consumers.

Examples:

* workspace_uuid
* document_uuid
* user_uuid

Serializers return UUID values instead of numeric identifiers.

⸻

Testing Strategy

The Documents app contains tests for:

* Services
* Selectors
* API endpoints

This separation allows business logic to be tested independently from HTTP behavior.

The API tests verify:

* Authentication
* Authorization
* Validation
* Correct HTTP status codes
* Response payloads

Services verify business rules without involving the API layer.

Selectors verify read operations independently.

⸻

Future Responsibilities

The Documents app will later integrate with the AI pipeline.

Uploading a document will eventually trigger:

1. PDF text extraction
2. Text chunking
3. Embedding generation using pgvector
4. Storage of searchable vectors

These responsibilities will remain outside the Documents app itself in order to keep document management independent from AI processing.


⸻

Asynchronous Processing Integration

The Documents app does not process uploaded documents directly.

After a document is successfully uploaded, the app publishes a
`document.uploaded` event to RabbitMQ.

The event contains the UUID of the uploaded document:

```json
{
    "document_uuid": "..."
}


RabbitMQ acts as the message broker between the Documents app and
the Documents Processing app.

The flow is:

Document API
│
▼
UploadDocumentService
│
├── Create Document
│
└── Publish document.uploaded
│
▼
RabbitMQ
│
▼
Documents Processing Worker
│
▼
ProcessDocumentService

This keeps document uploading independent from potentially expensive
PDF extraction, chunking, and embedding operations.

The API can therefore return immediately after the document is stored
and the processing work can happen asynchronously in a separate
worker.

RabbitMQ Responsibilities

RabbitMQ is responsible for:

* Receiving document processing events
* Persisting messages until they are consumed
* Routing events using exchanges and routing keys
* Delivering events to the Documents Processing worker

RabbitMQ is not responsible for:

* Processing documents
* Extracting PDF text
* Generating embeddings
* Storing document data

Event Contract

The Documents app publishes:

* Exchange: documents
* Event: document.uploaded
* Routing key: document.uploaded

The event payload contains the document UUID.

This creates a small and stable contract between the Documents app
and the Documents Processing app without coupling their internal
service implementations.

Failure Isolation

Document uploading and document processing are intentionally
decoupled.

If the processing worker is unavailable:

* The document can still be uploaded successfully.
* The document.uploaded event remains in RabbitMQ.
* The processing worker can consume the event when it becomes
    available.

This prevents document uploads from depending on the availability of
the AI processing pipeline.

The document processing status is tracked separately:

UPLOADED
│
▼
PROCESSING
│
├── COMPLETED
│
└── FAILED


