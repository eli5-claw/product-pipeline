---
name: sql-optimizer
description: Optimize SQL queries for performance and efficiency. Use when queries are slow, analyzing query plans, or designing database schemas. Triggers on requests for SQL optimization, slow queries, query performance, or database tuning.
---

# SQL Optimizer

Make databases fast. Query tuning, index optimization, schema design.

## Query Optimization

### EXPLAIN ANALYZE
Always start here:
```sql
EXPLAIN ANALYZE
SELECT * FROM users
WHERE email = 'user@example.com';
```

### Common Bottlenecks

1. **Missing indexes** — Sequential scans on large tables
2. **N+1 queries** — Looping queries in application code
3. **SELECT *** — Fetching unnecessary columns
4. **No pagination** — Loading massive result sets
5. **Unbounded JOINs** — Cartesian products

## Indexing Strategy

### When to Index
- Columns in WHERE clauses
- JOIN conditions
- ORDER BY columns
- Foreign keys

### When NOT to Index
- Small tables (< 1000 rows)
- Frequently updated columns
- Low cardinality columns (boolean, status)

### Index Types
```sql
-- B-tree (default)
CREATE INDEX idx_users_email ON users(email);

-- Partial index
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Composite index
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- GIN for JSON/arrays
CREATE INDEX idx_docs_tags ON documents USING GIN(tags);
```

## Query Patterns

### Efficient Pagination
```sql
-- Cursor-based (fast)
SELECT * FROM users
WHERE id > $cursor
ORDER BY id
LIMIT 100;

-- Offset (slow on large tables)
SELECT * FROM users
ORDER BY id
LIMIT 100 OFFSET 10000;  -- O(n) cost
```

### Efficient COUNT
```sql
-- Approximate (fast)
SELECT reltuples::BIGINT AS estimate
FROM pg_class
WHERE relname = 'users';

-- Exact (slow on large tables)
SELECT COUNT(*) FROM users;
```

## References

- [Query Plan Analysis](references/query-plans.md)
- [Indexing Guide](references/indexing.md)
- [Schema Design](references/schema-design.md)
