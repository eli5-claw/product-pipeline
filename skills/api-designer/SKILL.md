---
name: api-designer
description: Design RESTful and GraphQL APIs following industry best practices. Use when creating API specifications, designing endpoints, or reviewing API architecture. Triggers on requests for API design, OpenAPI specs, REST API, GraphQL, or endpoint design.
---

# API Designer

Design APIs that developers love. RESTful, GraphQL, or gRPC — done right.

## Design Principles

### RESTful APIs
- **Resource-oriented** — Nouns, not verbs (`/users` not `/getUsers`)
- **HTTP methods** — GET, POST, PUT, PATCH, DELETE correctly
- **Status codes** — 200, 201, 204, 400, 401, 403, 404, 409, 422, 500
- **Versioning** — URL (`/v1/`) or header-based
- **Pagination** — Cursor-based for scale, offset for simplicity

### GraphQL APIs
- **Schema-first** — Design before implementing
- **Type safety** — Strict schemas, nullability considered
- **N+1 protection** — DataLoader pattern
- **Query complexity** — Depth limiting, cost analysis
- **Introspection** — Disable in production

## API Specification (OpenAPI)

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        200:
          description: List of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

## Endpoint Design Checklist

- [ ] Clear, consistent naming
- [ ] Proper HTTP methods
- [ ] Appropriate status codes
- [ ] Request/response schemas
- [ ] Error response format
- [ ] Rate limiting headers
- [ ] Pagination (if list)
- [ ] Filtering/sorting (if list)
- [ ] Authentication documented
- [ ] Idempotency keys (if needed)

## Error Response Format

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Email is required",
    "field": "email",
    "requestId": "req_abc123"
  }
}
```

## References

- [REST Best Practices](references/rest-practices.md)
- [GraphQL Patterns](references/graphql-patterns.md)
- [OpenAPI Guide](references/openapi-guide.md)
