# 404 is returned without the documented ProblemDetail body

- Status: reproduced on 2026-10-04 against the `local` profile for all 21 operations.
- Service: `petclinic`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

Every documented 404 response carries an `application/json` `ProblemDetail`, whose six fields (`type`, `title`, `status`, `detail`, `timestamp`, `schemaValidationErrors`) are all required. When a controller does not find the resource it returns a bare `ResponseEntity` with status 404, so the answer has no body.

The cases assert the status first and the body fields after it, so a reproduction fails at `json.status` while the 404 status itself still passes.

## Shared contract evidence

- contract: src/main/resources/openapi.yml:1900 — "ProblemDetail:"
- contract: src/main/resources/openapi.yml:1947 — "required:"

## Affected endpoints

### GET /api/owners/{ownerId}

- contract: src/main/resources/openapi.yml:248 — "404:"
- contract: src/main/resources/openapi.yml:253 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:94 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|GET|/api/owners/{ownerId}|boundary|id-zero-not-found`
- case: `tests/petclinic/owners/case_get-owner-id-zero--x51mtd.yaml`

### PUT /api/owners/{ownerId}

- contract: src/main/resources/openapi.yml:296 — "404:"
- contract: src/main/resources/openapi.yml:301 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:116 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|PUT|/api/owners/{ownerId}|state|update-after-delete`
- case: `tests/petclinic/owners/case_update-owner-after-delete--skg14x.yaml`

### DELETE /api/owners/{ownerId}

- contract: src/main/resources/openapi.yml:350 — "404:"
- contract: src/main/resources/openapi.yml:355 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:133 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|DELETE|/api/owners/{ownerId}|idempotency|delete-twice`
- case: `tests/petclinic/owners/case_delete-owner-twice--z7bsw3.yaml`

### POST /api/owners/{ownerId}/pets

- contract: src/main/resources/openapi.yml:399 — "404:"
- contract: src/main/resources/openapi.yml:404 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:144 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|POST|/api/owners/{ownerId}/pets|error|unknown-owner`
- case: `tests/petclinic/owner-pets/case_add-pet-unknown-owner--1awtlk.yaml`

### GET /api/owners/{ownerId}/pets/{petId}

- contract: src/main/resources/openapi.yml:462 — "404:"
- contract: src/main/resources/openapi.yml:467 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:201 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- rows: `petclinic|GET|/api/owners/{ownerId}/pets/{petId}|error|pet-of-another-owner`, `petclinic|GET|/api/owners/{ownerId}/pets/{petId}|boundary|pet-id-zero-not-found`
- cases: `tests/petclinic/owner-pets/case_get-pet-of-another-owner--fwkekk.yaml`, `tests/petclinic/owner-pets/case_get-owners-pet-id-zero--hagy7x.yaml`

### PUT /api/owners/{ownerId}/pets/{petId}

- contract: src/main/resources/openapi.yml:516 — "404:"
- contract: src/main/resources/openapi.yml:521 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:172 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|PUT|/api/owners/{ownerId}/pets/{petId}|state|update-after-pet-delete`
- case: `tests/petclinic/owner-pets/case_update-owners-pet-after-delete--g49iv5.yaml`

### GET /api/pets/{petId}

- contract: src/main/resources/openapi.yml:968 — "404:"
- contract: src/main/resources/openapi.yml:973 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetRestControllerV1.java:57 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|GET|/api/pets/{petId}|boundary|id-zero-not-found`
- case: `tests/petclinic/pets/case_get-pet-id-zero--6rsp1o.yaml`

### PUT /api/pets/{petId}

- contract: src/main/resources/openapi.yml:1028 — "404:"
- contract: src/main/resources/openapi.yml:1033 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetRestControllerV1.java:78 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|PUT|/api/pets/{petId}|state|update-after-delete`
- case: `tests/petclinic/pets/case_update-pet-after-delete--co4ic1.yaml`

### DELETE /api/pets/{petId}

- contract: src/main/resources/openapi.yml:1081 — "404:"
- contract: src/main/resources/openapi.yml:1086 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetRestControllerV1.java:92 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|DELETE|/api/pets/{petId}|idempotency|delete-twice`
- case: `tests/petclinic/pets/case_delete-pet-twice--jcecf1.yaml`

### GET /api/visits/{visitId}

- contract: src/main/resources/openapi.yml:1219 — "404:"
- contract: src/main/resources/openapi.yml:1224 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:70 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|GET|/api/visits/{visitId}|boundary|id-zero-not-found`
- case: `tests/petclinic/visits/case_get-visit-id-zero--fotlgp.yaml`

### PUT /api/visits/{visitId}

- contract: src/main/resources/openapi.yml:1279 — "404:"
- contract: src/main/resources/openapi.yml:1284 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:91 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|PUT|/api/visits/{visitId}|state|update-after-delete`
- case: `tests/petclinic/visits/case_update-visit-after-delete--hmk8xk.yaml`

### DELETE /api/visits/{visitId}

- contract: src/main/resources/openapi.yml:1332 — "404:"
- contract: src/main/resources/openapi.yml:1337 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:105 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|DELETE|/api/visits/{visitId}|idempotency|delete-twice`
- case: `tests/petclinic/visits/case_delete-visit-twice--o2ijr2.yaml`

### GET, PUT, DELETE /api/pettypes/{petTypeId}

- contract: src/main/resources/openapi.yml:712 — "404:"
- contract: src/main/resources/openapi.yml:772 — "404:"
- contract: src/main/resources/openapi.yml:825 — "404:"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetTypeRestControllerV1.java:66 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetTypeRestControllerV1.java:86 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetTypeRestControllerV1.java:99 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- rows: `petclinic|GET|/api/pettypes/{petTypeId}|boundary|id-zero-not-found`, `petclinic|PUT|/api/pettypes/{petTypeId}|state|update-after-delete`, `petclinic|DELETE|/api/pettypes/{petTypeId}|idempotency|delete-twice`
- cases: `tests/petclinic/pettypes/case_get-pet-type-id-zero--pfw7pb.yaml`, `tests/petclinic/pettypes/case_update-pet-type-after-delete--lrwj07.yaml`, `tests/petclinic/pettypes/case_delete-pet-type-twice--13n83o.yaml`

### GET, PUT, DELETE /api/specialties/{specialtyId}

- contract: src/main/resources/openapi.yml:1470 — "404:"
- contract: src/main/resources/openapi.yml:1530 — "404:"
- contract: src/main/resources/openapi.yml:1583 — "404:"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/SpecialtyRestControllerV1.java:69 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/SpecialtyRestControllerV1.java:89 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/SpecialtyRestControllerV1.java:102 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- rows: `petclinic|GET|/api/specialties/{specialtyId}|boundary|id-zero-not-found`, `petclinic|PUT|/api/specialties/{specialtyId}|state|update-after-delete`, `petclinic|DELETE|/api/specialties/{specialtyId}|idempotency|delete-twice`
- cases: `tests/petclinic/specialties/case_get-specialty-id-zero--6j0wnw.yaml`, `tests/petclinic/specialties/case_update-specialty-after-delete--fk9av3.yaml`, `tests/petclinic/specialties/case_delete-specialty-twice--pm7fl6.yaml`

### GET, PUT, DELETE /api/vets/{vetId}

- contract: src/main/resources/openapi.yml:1722 — "404:"
- contract: src/main/resources/openapi.yml:1782 — "404:"
- contract: src/main/resources/openapi.yml:1835 — "404:"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VetRestControllerV1.java:71 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VetRestControllerV1.java:95 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VetRestControllerV1.java:117 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- rows: `petclinic|GET|/api/vets/{vetId}|boundary|id-zero-not-found`, `petclinic|PUT|/api/vets/{vetId}|state|update-after-delete`, `petclinic|DELETE|/api/vets/{vetId}|idempotency|delete-twice`
- cases: `tests/petclinic/vets/case_get-vet-id-zero--nq63qt.yaml`, `tests/petclinic/vets/case_update-vet-after-delete--os9l4z.yaml`, `tests/petclinic/vets/case_delete-vet-twice--flm14l.yaml`

## Not affected

A 404 produced by the data-integrity handler does carry a `ProblemDetail` (`src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:105`), for example a visit posted for a pet that does not exist.

## Observed

Unmarked runs of 2026-10-04 (batch 1, then batch 2), `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`. All 22 cases got status 404 as documented and then failed on the first body field:

| Request | Expected (contract) | Actual |
|---|---|---|
| `GET /api/owners/0` | 404 with a ProblemDetail | 404, empty body |
| `GET /api/owners/25/pets/18` (pet 18 belongs to owner 24) | 404 with a ProblemDetail | 404, empty body |
| `DELETE /api/pets/43` (second delete of the same pet) | 404 with a ProblemDetail | 404, empty body |
| `GET /api/pettypes/0` | 404 with a ProblemDetail | 404, empty body |
| `PUT /api/specialties/14` with a valid body (specialty 14 deleted before) | 404 with a ProblemDetail | 404, empty body |
| `DELETE /api/vets/14` (second delete of the same vet) | 404 with a ProblemDetail | 404, empty body |

## Markers

The 22 cases above carry a `known_defects` marker with `ref: defects/not-found-without-problem-detail.md`, the failing step and `at: json.status`; the contract assertions are unchanged, and the cases report XFAIL. The status assertion stays live: a status other than 404 is a plain failure, not an expected one. When the controllers return the documented body the cases report XPASS and the markers must be removed.
