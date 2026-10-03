# A visit without a date is rejected although the contract makes the date optional

- Status: reproduced on 2026-10-04 against the `local` profile for all three operations.
- Service: `petclinic`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The contract's `VisitFields` requires only `description`; `date` is optional. A visit created or updated without a date is therefore valid and must be accepted. The service copies the missing date into the stored visit as null, and the `visit_date` column does not accept null. The write fails on that constraint, and the data-integrity handler answers such failures with 404.

Before the run this note covered the update only, because the update handler sets the date in plain source. For the two create operations the copy happens in a mapper that is generated at build time, so the implementation side could not be cited until the run showed the same data-constraint answer.

## Shared evidence

- contract: src/main/resources/openapi.yml:2281 — "required:"
- contract: src/main/resources/openapi.yml:2282 — "- description"
- implementation: src/main/resources/db/h2/schema.sql:57 — "visit_date DATE NOT NULL,"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:97 — "@ExceptionHandler(DataIntegrityViolationException.class)"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:105 — "HttpStatus status = HttpStatus.NOT_FOUND;"

## Affected endpoints

### PUT /api/visits/{visitId}

- contract: src/main/resources/openapi.yml:1252 — "$ref: '#/components/schemas/VisitFields'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:93 — "currentVisit.setDate(visitDto.getDate());"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:95 — "this.clinicService.saveVisit(currentVisit);"
- row: `petclinic|PUT|/api/visits/{visitId}|boundary|date-omitted`
- case: `tests/petclinic/visits/case_update-visit-date-omitted--cf1dhw.yaml`

### POST /api/owners/{ownerId}/pets/{petId}/visits

- contract: src/main/resources/openapi.yml:559 — "$ref: '#/components/schemas/VisitFields'"
- contract: src/main/resources/openapi.yml:562 — "201:"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:179 — "Visit visit = visitMapper.toVisit(visitFieldsDto);"
- implementation: src/main/java/org/springframework/samples/petclinic/mapper/VisitMapper.java:21 — "Visit toVisit(VisitFieldsDto visitFieldsDto);"
- row: `petclinic|POST|/api/owners/{ownerId}/pets/{petId}/visits|boundary|date-omitted`
- case: `tests/petclinic/owner-visits/case_add-visit-date-omitted--hd5f5c.yaml`

### POST /api/visits

- contract: src/main/resources/openapi.yml:1138 — "$ref: '#/components/schemas/Visit'"
- contract: src/main/resources/openapi.yml:1141 — "200:"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:79 — "Visit visit = visitMapper.toVisit(visitDto);"
- implementation: src/main/java/org/springframework/samples/petclinic/mapper/VisitMapper.java:17 — "Visit toVisit(VisitDto visitDto);"
- row: `petclinic|POST|/api/visits|boundary|date-omitted`
- case: `tests/petclinic/visits/case_create-visit-date-omitted--u954tv.yaml`

## Observed

First run of batch 1, 2026-10-04, `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`. All three requests got the same ProblemDetail: status 404, title `DataIntegrityViolationException`, detail "The requested resource could not be processed due to a data constraint violation".

| Request | Expected (contract) | Actual |
|---|---|---|
| `PUT /api/visits/25` with `{"description": "apitest-cdaad7845608 follow-up"}`, then `GET /api/visits/25` | the visit has the new description | PUT answers 404; GET still shows `"description":"apitest-cdaad7845608 checkup"` |
| `POST /api/owners/36/pets/28/visits` with `{"description": "apitest-a744bc4ed221 checkup"}` | 201 with the stored Visit | 404; no visit stored |
| `POST /api/visits` with `{"description": "apitest-0ec78b198511 checkup", "petId": 60}` | the stored Visit in the body | 404; no visit stored |

## Markers

The three cases carry a `known_defects` marker with `ref: defects/visit-without-date-rejected.md`:

- update: step "the visit has the new description", `at: json.description`
- nested create: step "add a visit with a description only", `at: status`
- `POST /api/visits`: step "create a visit with a description and pet id only", `at: json.description`. This case does not assert the status, because the status of a successful create on this operation is disputed separately (`defects/create-answers-201-instead-of-200.md`).

The contract assertions are unchanged, and the cases report XFAIL. When the service accepts a visit without a date the cases report XPASS and the markers must be removed.
