# FastAPI Development

Apply these rules only to FastAPI applications.

## Structure

- Put application construction in `create_app()`.
- Keep routers thin; move persistence and business behavior into services or CRUD helpers.
- Keep request, update, and response schemas separate.
- Keep database sessions and authentication in dependencies.

## Async I/O

- Use `async def` for endpoints that perform I/O.
- Use async database and HTTP clients from async endpoints.
- Do not call `requests`, synchronous SQLAlchemy sessions, or blocking file or network operations from async routes.
- Do not create `SessionLocal()` or long-lived clients inside route handlers.

## Schemas And Security

- Use `response_model` for endpoints that return application data.
- Prefer Pydantic field constraints over handwritten validation when they express the rule.
- Never expose passwords, password hashes, access tokens, refresh tokens, or internal authentication state in response models.
- Keep CORS origins environment-specific; do not combine wildcard origins with credentials.
- Validate JWT expiry, issuer, audience, and algorithm.
- Rate-limit authentication and write-heavy endpoints.
- Redact credentials, cookies, authorization headers, and tokens from logs.

## Testing

- Override the exact dependency used by `Depends`.
- Clear `app.dependency_overrides` after each test.
- Prefer async test clients for async applications.
