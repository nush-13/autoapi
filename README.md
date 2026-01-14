# AutoAPI — Intelligent API Generator from Query Logs

AutoAPI is a backend engineering tool that analyzes database query logs and identifies frequently used data access patterns.

## Phase 1 — Query Log Analysis
- Reads realistic SQL query logs
- Extracts query type, table usage, and filter patterns
- Produces structured insights from raw database behavior

Further phases will focus on:
- API recommendation generation
- Automatic REST API creation
- Scalability and optimization

### Phase 4 — FastAPI Integration

- Added REST endpoint `/recommended-apis`
- Exposed Swagger documentation at `/docs`
- Reads SQL query logs, analyzes patterns, returns recommended APIs
- Stack used: FastAPI, Pandas, Docker (optional)

 project is being developed incrementally.

