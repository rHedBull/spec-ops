# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), research.md, data-design.md, architecture.md, contracts/

## Task Registry
**Last Task ID**: T031 | **Total Tasks**: 31 | **Updated**: [DATE]

### Task Status Summary
- **Not Started**: 31 tasks
- **In Progress**: 0 tasks  
- **Completed**: 0 tasks
- **Blocked**: 0 tasks
- **Detailed**: 0 tasks (use `/detail` command to create detailed specs)

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-design.md: Extract entities and state machines → model tasks
   → architecture.md: Extract services and structure → service tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Analyze feature scope and identify milestones:
   → Count contracts, entities, user stories
   → Group by logical boundaries (user workflows, service boundaries)
   → Determine milestone structure (1-3 milestones typical)
4. Generate milestone-based tasks:
   → Setup: project init, dependencies, linting (once)
   → For each milestone:
     * Tests: contract tests, integration tests for milestone scope
     * Implementation: models, services, endpoints for milestone scope
   → Final polish: cross-milestone cleanup, performance, docs
5. Apply task rules within each milestone:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD) within each milestone
6. Number tasks sequentially across all milestones (T001, T002...)
7. Generate dependency graph showing milestone boundaries
8. Create parallel execution examples per milestone
9. Validate milestone completeness:
   → Each milestone delivers working functionality?
   → All contracts covered across milestones?
   → All entities have models?
   → Clear milestone boundaries?
10. Return: SUCCESS (milestone-based tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Setup Phase (Once)
- [ ] T001 Create project structure per implementation plan
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T002 Initialize [language] project with [framework] dependencies  
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T003 [P] Configure linting and formatting tools
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned

## Milestone 1: Core User Management ⚠️
**Scope**: Basic user operations (create, read, authenticate)
**Deliverable**: Working user management system

### Milestone 1 Tests (TDD) ⚠️ MUST COMPLETE BEFORE IMPLEMENTATION
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T004 [P] Contract test POST /api/users in tests/contract/test_users_post.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T005 [P] Contract test GET /api/users/{id} in tests/contract/test_users_get.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T006 [P] Integration test user registration in tests/integration/test_registration.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T007 [P] Integration test auth flow in tests/integration/test_auth.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned

### Milestone 1 Implementation (ONLY after tests are failing)
- [ ] T008 [P] User model in src/models/user.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T009 [P] UserService CRUD in src/services/user_service.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T010 POST /api/users endpoint in src/api/users.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T011 GET /api/users/{id} endpoint in src/api/users.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T012 Connect UserService to database
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T013 Basic auth middleware in src/middleware/auth.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T014 Input validation and error handling
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned

## Milestone 2: Advanced Features ⚠️
**Scope**: User profiles, permissions, advanced operations
**Deliverable**: Complete user management with profiles and permissions
**Prerequisites**: Milestone 1 complete and tested

### Milestone 2 Tests (TDD) ⚠️ MUST COMPLETE BEFORE IMPLEMENTATION
- [ ] T015 [P] Contract test PUT /api/users/{id} in tests/contract/test_users_put.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T016 [P] Contract test GET /api/users/{id}/profile in tests/contract/test_profiles_get.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T017 [P] Integration test profile management in tests/integration/test_profiles.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T018 [P] Integration test permissions in tests/integration/test_permissions.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned

### Milestone 2 Implementation (ONLY after tests are failing)
- [ ] T019 [P] UserProfile model in src/models/user_profile.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T020 [P] PermissionService in src/services/permission_service.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T021 PUT /api/users/{id} endpoint in src/api/users.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T022 GET /api/users/{id}/profile endpoint in src/api/profiles.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T023 Profile management service integration
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T024 Permission-based middleware enhancement
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned

## Final Polish Phase
**Prerequisites**: All milestones complete
- [ ] T025 [P] Unit tests for validation in tests/unit/test_validation.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T026 [P] Unit tests for services in tests/unit/test_services.py
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T027 Performance tests (<200ms response) in tests/performance/
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T028 [P] Update docs/api.md with all endpoints
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T029 Cross-milestone integration validation
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T030 Remove code duplication across milestones
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned
- [ ] T031 Run complete manual-testing.md scenarios
  - **Status**: Not Started | **Detailed**: No | **Assignee**: Unassigned

## Dependencies

### Milestone-Level Dependencies
- **Setup** → **Milestone 1** → **Milestone 2** → **Final Polish**
- Each milestone must be fully complete (tests passing) before next milestone begins
- Within each milestone: Tests before implementation (TDD)

### Task-Level Dependencies
- **Milestone 1**: T004-T007 (tests) before T008-T014 (implementation)
- **Milestone 2**: T015-T018 (tests) before T019-T024 (implementation)
- **Final Polish**: T025-T031 after all milestones complete
- Models (T008, T019) before services (T009, T020) 
- Services before endpoints and middleware

## Parallel Execution Examples

### Milestone 1 Tests (Launch together):
```
Task: "Contract test POST /api/users in tests/contract/test_users_post.py"
Task: "Contract test GET /api/users/{id} in tests/contract/test_users_get.py"
Task: "Integration test registration in tests/integration/test_registration.py"
Task: "Integration test auth in tests/integration/test_auth.py"
```

### Milestone 1 Implementation (After tests fail):
```
Task: "User model in src/models/user.py"
Task: "UserService CRUD in src/services/user_service.py"
```

### Milestone 2 Tests (After Milestone 1 complete):
```
Task: "Contract test PUT /api/users/{id} in tests/contract/test_users_put.py"
Task: "Contract test GET /api/users/{id}/profile in tests/contract/test_profiles_get.py"
Task: "Integration test profile management in tests/integration/test_profiles.py"
Task: "Integration test permissions in tests/integration/test_permissions.py"
```

## Task Status Management

### Status Values
- **Not Started**: Task not yet begun
- **In Progress**: Implementation underway
- **Testing**: Implementation complete, verification in progress
- **Completed**: All acceptance criteria met
- **Blocked**: Cannot proceed (specify reason in task comments)

### Detailed Values  
- **No**: Task uses only high-level description from tasks.md
- **Yes**: Task has detailed specification in `tasks/T###-task-name.md`

### Updating Task Status
To update task status, modify the status line directly in tasks.md:
```
- [x] T005 [P] Contract test GET /api/users/{id} in tests/contract/test_users_get.py
  - **Status**: Completed | **Detailed**: Yes | **Assignee**: @developer
```

### Auto-Update Task Registry
When tasks are updated, remember to update the Task Registry section:
- Update **Last Task ID** if new tasks are added
- Update **Total Tasks** count
- Update status summary counts

### Helper Script (Optional)
Use the provided script to update task status automatically:
```bash
# Update single task status
./scripts/update-task-status.sh specs/001-user-auth T005 "In Progress" @developer

# Mark task as completed
./scripts/update-task-status.sh specs/001-user-auth T007 Completed

# Mark task as blocked
./scripts/update-task-status.sh specs/001-user-auth T010 Blocked @team-lead
```

The script automatically:
- Updates task status and assignee
- Marks/unmarks completion checkboxes
- Updates Task Registry summary counts
- Updates timestamp

## Next Steps: Task Detailing (Optional)

Use the `/detail` command to create detailed specifications for complex tasks:

### Usage Examples
```
/detail T005                    # Detail single task
/detail T004-T007              # Detail range of tasks  
/detail "Milestone 1"          # Detail all Milestone 1 tasks
/detail "Milestone 1 Tests"    # Detail just the test tasks in Milestone 1
/detail all                    # Detail every task (not recommended)
```

### When to Use Detailed Specs
- **Complex implementation tasks**: Multi-step or unclear requirements
- **Integration tasks**: Multiple systems or services involved  
- **Test tasks**: Complex test scenarios or setup requirements
- **New team members**: Provide detailed guidance for unfamiliar tasks

### Detailed Task Files
- Creates `tasks/T###-task-name.md` for each selected task
- Includes implementation details, acceptance criteria, file paths
- References design documents and dependencies
- Provides step-by-step development guidance

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts
- Use `/detail` command for implementation guidance

## Milestone-Based Task Generation Rules
*Applied during main() execution*

1. **Milestone Identification**:
   - Group contracts by logical feature boundaries
   - Group entities by related functionality
   - Identify user workflows that span multiple contracts
   - Create 1-3 milestones based on complexity

2. **From Contracts (per milestone)**:
   - Each contract in milestone → contract test task [P]
   - Each endpoint in milestone → implementation task
   
3. **From Data Design (per milestone)**:
   - Each entity in milestone → model creation task [P]
   - Related entities → service layer tasks in same milestone
   
4. **From User Stories (per milestone)**:
   - Each story in milestone scope → integration test [P]
   - Quickstart scenarios → milestone validation tasks

5. **Milestone Ordering**:
   - Setup once → Milestone 1 (tests → implementation) → Milestone 2 (tests → implementation) → Final Polish
   - Within milestone: Tests before implementation (TDD)
   - Dependencies block parallel execution within milestone

6. **Cross-Milestone Rules**:
   - Foundation services in Milestone 1
   - Advanced features in later milestones
   - Each milestone delivers working, testable functionality

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts distributed across milestones
- [ ] All entities have model tasks in appropriate milestones
- [ ] All milestone tests come before milestone implementation
- [ ] Each milestone delivers complete functionality
- [ ] Parallel tasks within milestone truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task within milestone
- [ ] Clear milestone boundaries and dependencies
- [ ] Milestone progression makes logical sense