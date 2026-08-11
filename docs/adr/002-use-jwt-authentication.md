# ADR-0002: Use JWT Authentication

## Status
Accepted



## Context
The project exposes a REST API that will later be consumed by a separate frontend.
Session authentication would tightly couple the backend to browser sessions and make future clients more difficult to support.

## Decision
Use Django REST Framework with `djangorestframework-simplejwt`.
The authentication flow consists of:
- Access Token (15 minutes)
- Refresh Token (7 days)
- Refresh token rotation
- Refresh token blacklisting

## Consequences

### Advantages
- Stateless authentication
- Easy integration with React and mobile clients
- Industry-standard approach
- Scalable architecture

### Disadvantages
- Slightly more complex than session authentication
- Requires token refresh and blacklisting