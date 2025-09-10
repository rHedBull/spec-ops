# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, or `GEMINI.md` for Gemini CLI).
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context
**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

### Tech Stack & Infrastructure
**Backend Framework**: [e.g., FastAPI, Express.js, Spring Boot, .NET Core or NEEDS CLARIFICATION]  
**Frontend Framework**: [e.g., React, Vue.js, Angular, Svelte, or N/A for non-web projects or NEEDS CLARIFICATION]  
**Mobile Framework**: [e.g., React Native, Flutter, Native iOS/Android, or N/A or NEEDS CLARIFICATION]  
**API Style**: [REST, GraphQL, gRPC, WebSocket, or NEEDS CLARIFICATION]  
**Authentication**: [JWT, OAuth2, Session-based, Firebase Auth, or NEEDS CLARIFICATION]  
**Deployment**: [Docker, Kubernetes, Serverless, Cloud provider specifics or NEEDS CLARIFICATION]

### Database & Storage
**Primary Database**: [PostgreSQL, MySQL, MongoDB, SQLite, or NEEDS CLARIFICATION]  
**Database Version**: [specific version requirements or NEEDS CLARIFICATION]  
**Connection Pooling**: [built-in, pgbouncer, connection library or NEEDS CLARIFICATION]  
**Caching Layer**: [Redis, Memcached, in-memory, or none or NEEDS CLARIFICATION]  
**File Storage**: [local filesystem, S3, GCS, Azure Blob, or none or NEEDS CLARIFICATION]  
**Search Engine**: [Elasticsearch, PostgreSQL full-text, Algolia, or none or NEEDS CLARIFICATION]

### Testing Strategy
**Unit Testing**: [pytest, Jest, JUnit, XCTest or NEEDS CLARIFICATION]  
**Integration Testing**: [Testcontainers, database fixtures, API testing or NEEDS CLARIFICATION]  
**E2E Testing**: [Playwright, Cypress, Selenium, or none or NEEDS CLARIFICATION]  
**Performance Testing**: [load testing tools, benchmarking approach or NEEDS CLARIFICATION]

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: [#] (max 3 - e.g., api, cli, tests)
- Using framework directly? (no wrapper classes)
- Single data model? (no DTOs unless serialization differs)
- Avoiding patterns? (no Repository/UoW without proven need)

**Architecture**:
- EVERY feature as library? (no direct app code)
- Libraries listed: [name + purpose for each]
- CLI per library: [commands with --help/--version/--format]
- Library docs: llms.txt format planned?

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? (test MUST fail first)
- Git commits show tests before implementation?
- Order: Contract→Integration→E2E→Unit strictly followed?
- Real dependencies used? (actual DBs, not mocks)
- Integration tests for: new libraries, contract changes, shared schemas?
- FORBIDDEN: Implementation before test, skipping RED phase

**Observability**:
- Structured logging included?
- Frontend logs → backend? (unified stream)
- Error context sufficient?

**Versioning**:
- Version number assigned? (MAJOR.MINOR.BUILD)
- BUILD increments on every change?
- Breaking changes handled? (parallel tests, migration plan)

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md                  # This file (/plan command output)
├── research.md              # Phase 0 output (/plan command)
├── services-architecture.md # Phase 1 output (/plan command)
├── data-model.md            # Phase 1 output (/plan command)
├── system-design.md         # Phase 1 output (/plan command)
├── project-structure.md     # Phase 1 output (/plan command)
├── quickstart.md            # Phase 1 output (/plan command)
├── contracts/               # Phase 1 output (/plan command)
│   ├── api-spec.yaml       # OpenAPI/GraphQL schemas
│   ├── service-interfaces/ # Service contract definitions
│   └── database-schema.sql # Database DDL and constraints
└── tasks.md                 # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

**Structure Decision**: [DEFAULT to Option 1 unless Technical Context indicates web/mobile app]

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each technology choice → best practices and integration patterns
   - For database selection → performance, scaling, and migration considerations
   - For service architecture → communication patterns and deployment strategies

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   For service architecture decisions:
     Task: "Research service communication patterns for {use case}"
   For database decisions:
     Task: "Evaluate {database} for {data patterns} and {scale requirements}"
   For interface design:
     Task: "Research design patterns for {specific domain/problem}"
   ```

3. **Service Architecture Research**:
   - Identify service boundaries based on business capabilities
   - Research microservice vs monolith trade-offs for this project
   - Evaluate service communication patterns (sync vs async)
   - Research deployment and orchestration requirements

4. **Database & Storage Research**:
   - Evaluate database options against data patterns and scale
   - Research schema migration strategies for chosen database
   - Investigate caching and performance optimization patterns
   - Plan backup, recovery, and monitoring approaches

5. **Class Design & Patterns Research**:
   - Research applicable design patterns for identified problems
   - Evaluate inheritance vs composition trade-offs
   - Plan dependency injection and testing strategies
   - Research error handling and exception design patterns

6. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]
   - Implementation considerations: [key technical details]

**Output**: research.md with all NEEDS CLARIFICATION resolved and technical foundation established

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Service Architecture Design** → `services-architecture.md`:
   - Identify core services from functional requirements
   - Define service boundaries and responsibilities
   - Map service-to-service communication patterns
   - Define shared vs service-specific data stores
   - Document service deployment and scaling strategies

2. **Database Design** → `data-model.md`:
   - Design database schema with tables, indexes, constraints
   - Define entity relationships (1:1, 1:Many, Many:Many)
   - Plan data migration and seeding strategies
   - Consider read replicas, sharding if needed for scale
   - Document backup and disaster recovery approach

3. **Interface & Class Design** → `system-design.md`:
   - Define core interfaces and abstract classes
   - Plan inheritance hierarchies and composition patterns
   - Design dependency injection containers and patterns
   - Define error handling and exception hierarchies
   - Document design patterns used (Factory, Strategy, Observer, etc.)

4. **API Contracts Design** → `/contracts/`:
   - For each user action → endpoint specification
   - Define request/response schemas with validation rules
   - Plan API versioning strategy and backward compatibility
   - Design authentication and authorization per endpoint
   - Output OpenAPI/GraphQL schema files

5. **Directory Structure Planning** → `project-structure.md`:
   - Define package/module organization
   - Plan separation of concerns (models, services, controllers, utils)
   - Design test directory mirroring source structure
   - Plan configuration and environment file organization
   - Define build and deployment artifact structure

6. **Generate contract tests** from contracts:
   - One test file per endpoint/service interface
   - Assert request/response schemas and business rules
   - Tests must fail (no implementation yet)
   - Include database integration test scaffolding

7. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps
   - Include service interaction tests

8. **Update agent file incrementally** (O(1) operation):
   - Run `/scripts/update-agent-context.sh [claude|gemini|copilot]` for your AI assistant
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: services-architecture.md, data-model.md, system-design.md, project-structure.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-30 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [ ] Phase 0: Research complete (/plan command)
- [ ] Phase 1: Design complete (/plan command)
- [ ] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [ ] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [ ] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*