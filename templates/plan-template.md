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
**Performance Goals**: [Default: development-friendly, or specify if performance requirements mentioned, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Security Requirements**: [Default: basic development security, or specify if security/privacy mentioned, e.g., GDPR, encryption, audit trails or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

### Tech Stack & Infrastructure
**Backend Framework**: [e.g., FastAPI, Express.js, Spring Boot, .NET Core or NEEDS CLARIFICATION]  
**Frontend Framework**: [e.g., React, Vue.js, Angular, Svelte, or N/A for non-web projects or NEEDS CLARIFICATION]  
**Mobile Framework**: [e.g., React Native, Flutter, Native iOS/Android, or N/A or NEEDS CLARIFICATION]  
**API Style**: [REST, GraphQL, gRPC, WebSocket, or NEEDS CLARIFICATION]  
**Authentication**: [JWT, OAuth2, Session-based, Firebase Auth, or NEEDS CLARIFICATION]  
**Deployment**: [Default: local development setup, or specify if production/cloud requirements or NEEDS CLARIFICATION]

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

### State Management & Object Lifecycle
**State Machines**: [entities requiring state management, e.g., Order, User, Payment or NEEDS CLARIFICATION]  
**State Persistence**: [how state is stored and retrieved, database fields, event sourcing or NEEDS CLARIFICATION]  
**State Transitions**: [what triggers state changes, validation rules, business logic or NEEDS CLARIFICATION]  
**Concurrency Control**: [optimistic/pessimistic locking, versioning, conflict resolution or NEEDS CLARIFICATION]  
**Object Lifecycle**: [creation, initialization, active states, cleanup, destruction or NEEDS CLARIFICATION]  
**Event Handling**: [domain events, state change notifications, event sourcing patterns or NEEDS CLARIFICATION]  
**Temporal Concerns**: [time-based state changes, scheduling, expiration, timeouts or NEEDS CLARIFICATION]

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

### MANDATORY Documentation Structure (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── architecture.md      # Phase 1: MANDATORY - Services, structure, integration (/plan command)
├── data-design.md       # Phase 1: MANDATORY - Models, state, persistence, lifecycle (/plan command)
├── deployment.md        # Phase 1: MANDATORY - Deployment, security*, performance* (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
│   ├── api-spec.yaml   # OpenAPI/GraphQL schemas
│   └── database-schema.sql # Database DDL and constraints
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

**CRITICAL**: You MUST create files with these EXACT names. Do NOT use old names like:
- ❌ data-model.md (OLD - DO NOT USE)
- ❌ system-design.md (OLD - DO NOT USE)  
- ❌ services-architecture.md (OLD - DO NOT USE)
- ✅ architecture.md (CORRECT)
- ✅ data-design.md (CORRECT)
- ✅ deployment.md (CORRECT)

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

6. **State Management & Lifecycle Research**:
   - Identify entities requiring state machines from functional requirements
   - Research state machine patterns for identified entities
   - Evaluate object lifecycle management strategies
   - Investigate concurrency control and locking mechanisms
   - Research event-driven architecture patterns if applicable
   - Plan temporal state management (timeouts, scheduling, expiration)

7. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]
   - Implementation considerations: [key technical details]

**Output**: research.md with all NEEDS CLARIFICATION resolved and technical foundation established

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **MANDATORY: System Architecture** → `architecture.md` (EXACT FILENAME):
   - **Service Design**: Core services, boundaries, communication patterns
   - **Project Structure**: Directory organization, module separation
   - **Integration Patterns**: How services/components connect
   - **Technology Integration**: Framework usage, dependency patterns

2. **MANDATORY: Data & State Design** → `data-design.md` (EXACT FILENAME):
   - **Database Schema**: Tables, indexes, constraints, relationships
   - **Entity Modeling**: Core domain objects and their properties
   - **State Machines**: Which entities have state, valid transitions, business rules
   - **Object Lifecycle**: Creation, initialization, state changes, cleanup, destruction
   - **Concurrency & Locking**: Version control, optimistic/pessimistic locking
   - **Event Patterns**: State change events, domain events, event sourcing
   - **Temporal Concerns**: Time-based state changes, expiration, scheduling
   - **Class Design**: Interfaces, inheritance, composition for data/state management
   - **Persistence Patterns**: How objects are saved, loaded, cached

3. **MANDATORY: Deployment & Operations** → `deployment.md` (EXACT FILENAME):
   - **Default Strategy**: Simple local development setup
     * Local database (SQLite, local PostgreSQL, etc.)
     * Direct application execution (no containers by default)
     * File-based configuration
     * Development-friendly defaults
   - **Conditional Sections** (only if explicitly mentioned in requirements):
     * **Security & Privacy** (if security/privacy requirements specified):
       - Authentication and authorization strategies
       - Data encryption and protection
       - Privacy compliance (GDPR, CCPA, etc.)
       - Security headers and protections
       - Audit logging and monitoring
     * **Performance & Scaling** (if performance requirements specified):
       - Load balancing and scaling strategies
       - Caching layers and optimization
       - Database performance tuning
       - Monitoring and alerting
       - Performance testing approaches
     * **Production Deployment** (if production requirements specified):
       - Container/cloud deployment strategies
       - Infrastructure as code
       - CI/CD pipeline design
       - Environment management
       - Backup and disaster recovery

4. **API Contracts Design** → `/contracts/`:
   - For each user action → endpoint specification
   - Define request/response schemas with validation rules
   - **State-Related APIs**:
     * Design state query endpoints (current state, history)
     * Define state transition endpoints with validation
     * Plan bulk state operation APIs if needed
     * Design state event subscription APIs
   - Plan API versioning strategy and backward compatibility
   - Design authentication and authorization per endpoint
   - Output OpenAPI/GraphQL schema files

5. **Generate contract tests** from contracts:
   - One test file per endpoint/service interface
   - Assert request/response schemas and business rules
   - Tests must fail (no implementation yet)
   - Include database integration test scaffolding

6. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps
   - Include service interaction tests

7. **Update agent file incrementally** (O(1) operation):
   - Run `/scripts/update-agent-context.sh [claude|gemini|copilot]` for your AI assistant
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**REQUIRED Output**: 
- architecture.md (NOT services-architecture.md)
- data-design.md (NOT data-model.md) 
- deployment.md (NEW FILE)
- /contracts/*, failing tests, quickstart.md, agent-specific file

**IMPORTANT**: You MUST create these exact filenames. Do not use old naming like data-model.md or system-design.md.

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