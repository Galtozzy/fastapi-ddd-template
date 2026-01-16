"""Adapters API module.

This module contains the FastAPI routers/adapters that serve
as the entry points for external API requests.

Routers are organized by bounded context (e.g., health, users).
Each router defines endpoints and handles HTTP-specific concerns
(request parsing, response formatting, status codes).

The router should delegate to application use cases and not
contain business logic directly.
"""

__all__ = []
