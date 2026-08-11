# Project Structure
This document defines the standard structure used throughout the project. Every new feature should follow these conventions to ensure the codebase remains consistent, maintainable, and easy for new developers to understand.

The structure is designed around:
- Scalability
- Maintainability
- SOLID principles
- Separation of concerns
- Testability
- Team collaboration

Following a consistent structure reduces onboarding time for new contributors and makes future refactoring significantly easier.

This document is a living reference and should evolve alongside the project.




## Current Project Structure
The project structure below reflects the current state of the codebase. As the application grows, new directories and components will be introduced when they provide clear value.

```text
project-root/
├── apps/
├── config/
├── docker/
├── docs/
├── requirements/
├── docker-compose.yml
├── manage.py
└── README.md
```


### Directory Responsibilities
- **apps/** contains all business features of the application.
- **config/** contains Django configuration, settings, URLs, and ASGI/WSGI entry points.
- **docker/** contains Dockerfiles and container configuration.
- **docs/** contains architecture, ADRs, diagrams, and technical documentation.
- **requirements/** separates Python dependencies by environment if needed.
