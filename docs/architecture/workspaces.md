Workspaces Architecture

Purpose

The workspaces app is responsible for multi-tenancy and authorization.

A workspace represents an isolated environment where users can collaborate and access shared resources. Every resource in the system (documents, chats, AI interactions, etc.) belongs to a workspace.

The app is responsible for:

* Creating workspaces.
* Managing workspace membership.
* Managing workspace roles.
* Enforcing workspace-level permissions.

It is not responsible for storing documents, AI logic, or conversations.

⸻

Domain Model

Workspace

Represents an isolated company or team.

Fields

* id
* name
* slug
* created_at
* updated_at

Business Rules

* Workspace names may be duplicated.
* Slugs are unique and generated automatically.
* The user who creates a workspace automatically becomes its owner.

⸻

WorkspaceMembership

Represents the relationship between a user and a workspace.

A user may belong to multiple workspaces.

A workspace may contain multiple users.

Fields

* workspace
* user
* role
* created_at

Roles

* OWNER
* STAFF

Business Rules

* A user can belong to a workspace only once.
* Each (workspace, user) pair is unique.
* Only owners may add staff members.
* Both owners and staff members may view workspace members.

⸻

Services

Business logic is implemented in services.

CreateWorkspaceService

Responsibilities:

* Create a workspace.
* Generate a unique slug.
* Create the owner’s membership.

⸻

AddWorkspaceMemberService

Responsibilities:

* Verify the actor is an owner.
* Prevent duplicate memberships.
* Add a new staff member.

⸻

ListWorkspaceMembersService

Responsibilities:

* Verify the requesting user belongs to the workspace.
* Return all workspace members.

⸻

Selectors

Selectors contain read-only queries.

get_user_workspaces

Returns all workspaces that the authenticated user belongs to.

⸻

API Endpoints

Create Workspace

POST /api/workspaces/

Creates a new workspace.

⸻

List Workspaces

GET /api/workspaces/

Returns every workspace the authenticated user belongs to.

⸻

Add Workspace Member

POST /api/workspaces/<workspace_id>/members/

Adds a staff member.

Only workspace owners are authorized.

⸻

List Workspace Members

GET /api/workspaces/<workspace_id>/members/

Returns all members of a workspace.

Accessible only to users who belong to that workspace.

⸻

Authorization Rules

Action	                   Owner	Staff	Non-member
Create workspace	        ✅	     ✅	      ✅
View own workspaces	        ✅	     ✅	      ❌
Add staff member	        ✅	     ❌	      ❌
View workspace members	    ✅	     ✅	      ❌

⸻

Testing Strategy

The app follows a service-first approach.

Each feature is implemented in the following order:

1. Service tests
2. Service implementation
3. API tests
4. API implementation

This keeps business logic independent from the REST API and makes it reusable by future interfaces such as Telegram, CLI tools, or background jobs.

⸻

Design Decisions

* Business logic lives in services.
* Database queries are isolated in selectors when appropriate.
* API views remain thin.
* Permissions are enforced inside services.
* Business rule violations are represented using BusinessLogicError.
* Global exception handling converts business exceptions into consistent API responses.

⸻

Future Extensions

Planned features include:

* Remove workspace members.
* Transfer workspace ownership.
* Multiple owner support.
* Workspace settings.
* Invitations.
* Audit logging.
* Workspace deletion and archival.

These are intentionally postponed to keep the MVP focused.