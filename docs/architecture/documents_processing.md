# Documents Processing App

## Purpose

The Documents Processing app transforms uploaded PDF documents into
searchable knowledge.

It is intentionally separated from the Documents app. The Documents
app manages document ownership, access, and metadata, while this app
handles the computationally expensive processing required to make
documents usable by the future AI assistant.

The processing pipeline is asynchronous and is triggered through
RabbitMQ events rather than directly from the document upload request.

---

## Responsibilities

The Documents Processing app is responsible for:

* Consuming document upload events from RabbitMQ
* Extracting text from PDF documents
* Creating processed document records
* Splitting extracted text into smaller chunks
* Generating embeddings for document chunks
* Storing embeddings using pgvector
* Tracking the processing lifecycle

The app is not responsible for:

* Document ownership
* Workspace authorization
* Uploading documents
* Conversational AI
* Semantic search
* Retrieval orchestration

---

## Processing Pipeline

The complete processing pipeline is:

```text
Document uploaded
        │
        ▼
RabbitMQ
        │
        ▼
Document Processing Worker
        │
        ▼
ProcessDocumentService
        │
        ├── Mark document as PROCESSING
        │
        ├── Extract PDF text
        │
        ├── Create ProcessedDocument
        │
        ├── Split text into DocumentChunks
        │
        ├── Generate embeddings
        │
        ├── Store DocumentEmbeddings
        │
        └── Mark document as COMPLETED


    If processing fails:
        PROCESSING
            │
            ▼
        FAILED


The processing worker acknowledges the RabbitMQ message after the
processing attempt so that a permanently failing document does not
remain in an endless redelivery loop.

⸻

Asynchronous Architecture

The Documents app publishes a document.uploaded event after a
document is created.

RabbitMQ acts as the broker between the Documents app and the
Documents Processing worker.



Asynchronous Architecture

The Documents app publishes a document.uploaded event after a
document is created.

RabbitMQ acts as the broker between the Documents app and the
Documents Processing worker.



Documents App
     │
     │ document.uploaded
     ▼
 RabbitMQ
     │
     ▼
Documents Processing Worker
     │
     ▼
ProcessDocumentService

The event contains the UUID of the document:

{
    "document_uuid": "..."
}


The processing app does not need to know how the Documents app
implements uploading.

It only needs the document UUID defined by the event contract.

⸻

RabbitMQ Integration

The processing worker consumes events from RabbitMQ.

Current messaging configuration:

* Exchange: documents
* Exchange type: topic
* Queue: documents_processing
* Routing key: document.uploaded

The queue is durable so that messages are not lost when the worker is
temporarily unavailable.

The worker acknowledges messages after processing has completed or
failed and the document status has been updated.

⸻

Worker

The processing pipeline runs in a dedicated Docker service:
customer-support-document-worker

The worker executes the Django management command:
python manage.py consume_document_uploaded



The worker:

1. Connects to RabbitMQ.
2. Declares the documents exchange.
3. Declares the processing queue.
4. Binds the queue to the document.uploaded routing key.
5. Waits for uploaded-document events.
6. Executes ProcessDocumentService.
7. Marks processing failures as FAILED.
8. Acknowledges the RabbitMQ message.

The worker is intentionally separate from the Django web process.

This prevents long-running document processing from blocking API
requests.


Service Architecture

The application follows the project’s layered architecture.

RabbitMQ Consumer
       │
       ▼
ProcessDocumentService
       │
       ├── PdfTextExtractionService
       │
       ├── ChunkDocumentService
       │
       └── GetEmbeddingsService
                │
                ▼
       GenerateEmbeddingsProvider
                │
                ▼
            AI Service


The orchestration logic lives in ProcessDocumentService.

Individual processing responsibilities are delegated to specialized
services.

This keeps the main pipeline readable and follows the Single
Responsibility Principle.


PDF Text Extraction

PDF extraction is handled by:
PdfTextExtractionService


Its responsibility is limited to converting the PDF file into plain
text.

The extracted text is stored in ProcessedDocument.

The Documents Processing app therefore preserves the extracted text
rather than requiring the PDF to be parsed again for every future
operation.


Text Chunking

Extracted text is divided into smaller pieces by:
ChunkDocumentService

The underlying splitter is:
RecursiveTextSplitter


The splitter recursively attempts increasingly smaller separators to
produce chunks that respect the configured chunk size.

Chunking exists because embedding an entire document as one vector
would make later semantic retrieval ineffective.

Each chunk stores:

* Its UUID
* The processed document
* Its content
* Its position within the document
* Its creation timestamp

Chunks are ordered by chunk_index.

A database constraint guarantees that a document cannot contain two
chunks with the same index.

⸻

Embedding Generation

Embedding generation is deliberately separated behind a provider
abstraction.

The Documents Processing app uses:
GenerateEmbeddingsProvider

The provider communicates with the separate AI service through HTTP.
Documents Processing
        │
        │ HTTP
        ▼
    AI Service
        │
        ▼
   Embedding Model


The current AI service uses the BGE-M3 embedding model and returns
1024-dimensional vectors.

The Documents Processing app does not directly load or manage the
embedding model.

This keeps model execution isolated from the Django application.

⸻

AI Service Boundary

The AI service is a separate FastAPI application.

Its responsibility is to expose AI-related capabilities through an
HTTP API.

The current embedding endpoint is:
POST /v1/embeddings

The request contains:
{
    "text": "document text"
}


The response contains an embedding vector.

The Documents Processing app communicates with the AI service through
the provider abstraction rather than depending directly on the model
implementation.

This allows the embedding implementation to change without requiring
changes to the processing pipeline.

⸻

Provider Abstraction

Embedding generation uses a provider abstraction so that the
processing pipeline does not depend directly on HTTP or a specific AI
implementation.

Conceptually:
GetEmbeddingsService
        │
        ▼
Embedding Provider
        │
        ▼
AI Service


The provider is responsible for:

* Calling the AI service
* Sending the document chunk text
* Validating the response
* Validating embedding dimensions
* Translating external failures into application exceptions

The provider exposes metadata such as:

* Provider name
* Model name

This metadata is stored alongside each embedding.

⸻

Embedding Storage

Embeddings are stored in PostgreSQL using pgvector.

The project uses: VectorField(dimensions=1024)
Each DocumentEmbedding belongs to a document chunk.

Each DocumentEmbedding belongs to a document chunk.

An embedding records:

* UUID
* Chunk
* Provider
* Model name
* Vector
* Creation timestamp

A database constraint prevents duplicate embeddings for the same:
chunk + provider + model
This allows the system to support multiple embedding providers or
models in the future without changing the chunk model.


Data Model

The processing domain contains three main models.
Document
   │
   │ OneToOne
   ▼
ProcessedDocument
   │
   │ OneToMany
   ▼
DocumentChunk
   │
   │ OneToMany
   ▼
DocumentEmbedding


ProcessedDocument

Represents the processed representation of an uploaded document.

Stores:

* Document relationship
* Extracted text
* Creation timestamp
* Update timestamp

The document itself is the primary key, enforcing the one-to-one
relationship.

DocumentChunk

Represents a section of extracted document text.

Stores:

* UUID
* Processed document
* Content
* Chunk index
* Creation timestamp

DocumentEmbedding

Represents an embedding generated from a document chunk.

Stores:

* UUID
* Chunk
* Provider
* Model name
* 1024-dimensional vector
* Creation timestamp

⸻

Processing Status

Document processing uses four states:
UPLOADED
    │
    ▼
PROCESSING
    │
    ├── COMPLETED
    │
    └── FAILED

    UPLOADED

The document has been successfully stored but processing has not yet
started.

PROCESSING

The worker has started processing the document.

COMPLETED

Text extraction, processed-document creation, chunking, and embedding
generation have all completed successfully.

FAILED

The processing pipeline encountered an unexpected error.

The status is changed to FAILED by the RabbitMQ consumer after the
processing service raises an exception.

⸻

Failure Handling

Failures are handled at the appropriate architectural boundary.

ProcessDocumentService is responsible for performing the pipeline.

It does not silently convert unexpected processing exceptions into
successful results.

The RabbitMQ consumer catches processing failures and updates the
document status to FAILED.

This gives us:
Pipeline succeeds
        │
        ▼
COMPLETED

This prevents documents from remaining permanently in the
PROCESSING state after a worker failure.

⸻

Idempotency and Safety

The processing pipeline is designed to be safe to execute more than
once for the same document.

Database constraints provide protection against duplicate data.

Examples:

* One ProcessedDocument per document
* Unique chunk index per processed document
* Unique embedding per chunk/provider/model

get_or_create() is used when creating the processed document so
reprocessing does not create duplicate processed-document records.

This is important for asynchronous systems because message delivery
can potentially occur more than once.

⸻

Testing Strategy

The Documents Processing app has extensive test coverage across its
layers.

Current tests cover:

* PDF text extraction
* Text splitting
* Chunk creation
* Processing pipeline
* Embedding service
* Embedding provider
* AI service integration behavior
* HTTP failures
* Invalid embedding responses
* Invalid embedding dimensions
* Processing status transitions
* RabbitMQ consumer failure handling

The tests distinguish between:

Unit Tests

Used for individual services, providers, and processing components.

Integration Tests

Used where multiple application components interact, such as the
embedding provider and AI service boundary.

Consumer Tests

Used to verify RabbitMQ event handling and processing failure behavior.

Edge Cases

Tests explicitly cover cases such as:

* Empty text
* Oversized text
* Invalid chunk configuration
* Invalid embedding dimensions
* Missing embedding response data
* AI service failures
* Processing failures
* Reprocessing the same document

The project follows a test-first approach where practical: expected
behavior is defined through tests before implementation is finalized.

⸻

Docker Architecture

The processing system runs as separate Docker services.

┌───────────────────────┐
│       Django Web      │
│    Documents API      │
└───────────┬───────────┘
            │
            │ document.uploaded
            ▼
┌───────────────────────┐
│       RabbitMQ        │
│     Message Broker    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Document Worker     │
│ Django Management Cmd │
└───────────┬───────────┘
            │
            ├──────────────► PostgreSQL + pgvector
            │
            ▼
┌───────────────────────┐
│      AI Service       │
│        FastAPI        │
└───────────────────────┘



The worker and web application share the Django codebase but run as
separate Docker containers with different responsibilities.

The AI service is independently deployed as a FastAPI container.

⸻

Architectural Decisions

Asynchronous Processing

Document processing is asynchronous because PDF extraction, chunking,
and embedding generation can be expensive operations.

This prevents API requests from being blocked by long-running
processing.

Separate AI Service

Embedding generation is isolated behind a FastAPI service.

This keeps machine-learning dependencies and model execution separate
from the Django application.

RabbitMQ

RabbitMQ provides a durable messaging boundary between document
management and document processing.

This allows the processing worker to scale independently from the
Django API.

pgvector

PostgreSQL with pgvector is used to store embeddings alongside the
application’s relational data.

This provides a natural foundation for future semantic retrieval.

Provider Abstraction

Embedding generation is accessed through a provider abstraction so
that models and AI providers can be changed without rewriting the
processing pipeline.

⸻

Future Integration

The Documents Processing app provides the foundation for the future
AI support assistant.

The next major layer will be retrieval.

The expected future flow is:
User Question
      │
      ▼
Query Embedding
      │
      ▼
Vector Similarity Search
      │
      ▼
Relevant Document Chunks
      │
      ▼
AI / LLM Application
      │
      ▼
Grounded Response


The Documents Processing app’s responsibility ends at producing and
storing searchable document representations.

Retrieval and conversational AI will remain separate concerns.

