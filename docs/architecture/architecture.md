# Project Architecture
This document explains the architectural decisions made during the development of this project. It focuses on the reasoning behind the project structure, configuration choices, and best practices, so that future contributors—and interviewers—can understand not only *what* was done, but *why* it was done.



## Django Settings Structure

### Why split `settings.py`?
Instead of keeping all configuration in a single `settings.py` file, the project separates settings into multiple modules.

**Benefits:**
- Improves readability by keeping related settings together.
- Makes maintenance easier as the project grows.
- Allows different environments (development, production, testing) to have their own configuration.
- Reduces the chance of accidentally deploying development settings to production.
- Follows a common structure used in larger Django projects.


### Structure
```text
config/
└── settings/
    ├── __init__.py
    ├── base.py
    ├── development.py
    └── production.py
```

### How it works
- `base.py` contains settings shared by every environment.
- `development.py` imports everything from `base.py` and overrides settings needed for local development.
- `production.py` imports everything from `base.py` and overrides settings for production deployments.

This approach follows the **Don't Repeat Yourself (DRY)** principle by placing shared configuration in a single location while allowing each environment to customize only what is necessary.


## Architecture Principles
This project is designed with maintainability, scalability, and collaboration in mind. The following principles guide every architectural decision:

- SOLID principles are applied where they improve flexibility and maintainability.
- Business logic is separated from the presentation layer.
- Each component has a single, well-defined responsibility.
- Code should be easy to extend without modifying existing implementations whenever possible.
- Dependencies should rely on abstractions instead of concrete implementations.
- The project follows a feature-based structure to make collaboration easier.
- Configuration is externalized through environment variables.
- Every feature should be easy to test independently.



## Authentication Architecture

### Authentication Strategy
- Django REST Framework
- JWT authentication using `djangorestframework-simplejwt`
- Custom `User` model extending `AbstractUser`
- API-first architecture (no session authentication)

### Token Strategy
- Access Token: 15 minutes
- Refresh Token: 7 days
- Refresh token rotation enabled
- Refresh token blacklisting enabled

### Design Decisions
- JWT was chosen because the backend is API-first and will support a separate frontend in the future.
- Authentication is implemented through the `accounts` app.
- Business logic belongs in services.
- Read operations belong in selectors.
- Views orchestrate requests and responses only.
- Serializers validate data only.
- Models represent the domain and persistence.

### Benefits
- Easy to integrate with React, mobile apps, or other clients.
- Scalable and maintainable architecture.
- Clear separation of responsibilities.


## Application Architecture

The project follows a layered architecture inside each Django application.

```text
HTTP Request
      │
      ▼
APIView
      │
      ▼
Serializer
      │
      ▼
Service
      │
      ▼
Model
      │
      ▼
Database
```

### Responsibilities

#### Views
Views are responsible for:
- Receiving HTTP requests.
- Validating input through serializers.
- Calling business services.
- Returning HTTP responses.

Views should not contain business rules.

---

#### Serializers
Serializers validate incoming data and serialize outgoing data.

They should not contain business logic or interact directly with external systems.

---

#### Services
Services contain business logic.
Examples:
- Registering a user
- Logging a user out
- Creating a workspace
- Processing AI requests

Business logic remains reusable independently from the API layer.

---

#### Selectors
Selectors provide reusable read operations.
They encapsulate complex database queries and allow multiple parts of the application to retrieve data without duplicating query logic.

Selectors never modify data.

---

#### Models
Models define the application's domain entities and persistence layer.

Models should remain focused on representing data rather than orchestrating business workflows.


## Multi-Tenant Architecture

The platform is designed as a multi-tenant SaaS application, where each company has its own isolated workspace.

A workspace acts as the boundary for all business data, ensuring that companies cannot access each other’s resources.

### Workspace Isolation

Every business entity belongs to a workspace, either directly or indirectly.

Examples include:

* Documents
* Conversations
* Messages
* AI knowledge

All data access is filtered by the authenticated staff member’s workspace membership.

### Staff and Customers

The system distinguishes between two types of users:

* Staff authenticate using JWT and manage workspaces, documents, and AI configuration.
* Customers interact anonymously with the AI assistant and do not require authentication.

This separation keeps authentication focused on administration while providing a frictionless customer experience.

### Workspace Roles

Workspace permissions are intentionally kept simple for the initial version of the project.

Two roles are supported:

* OWNER
* STAFF

Roles are implemented using Django TextChoices rather than a database table to avoid unnecessary complexity. If future requirements introduce customizable permissions, the design can evolve to a dedicated role and permission system.