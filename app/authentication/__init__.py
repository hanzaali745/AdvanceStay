"""
Authentication module — placeholder for Roadmap Phase 7 (Authentication)
and Phase 8 (User accounts).

Not yet implemented and not wired into app.main. When this phase starts:
  - User model + password hashing (passlib, already in requirements.txt)
  - JWT or session-based auth (python-jose is already in requirements.txt)
  - Route protection dependency for the routers in app/dashboard,
    app/suppliers, app/products, etc.

Building this now, before Phase 2-6 (connectors/agents/deployment) land,
would mean protecting routes and data that don't exist yet — kept as an
explicit integration point instead per the project roadmap.
"""
