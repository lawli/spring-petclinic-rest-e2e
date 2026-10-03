# Request values outside the declared schema are not answered with 400, except body bean-validation failures

- Status: reproduced on 2026-10-04 against the `local` profile for all 25 operations.
- Service: `petclinic`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The contract declares path ids as integers with `minimum: 0`, paging parameters with their own bounds, and date fields with `format: date`; each operation documents `400 Bad request` with a `ProblemDetail`. A request value outside those declarations must therefore be answered with 400.

The exception handler produces 400 for one exception type only, `MethodArgumentNotValidException`, which is raised when a request body fails bean validation. Every other exception reaches the catch-all handler, which answers 500. That covers a violated parameter constraint, a non-numeric value for an integer parameter, and a body value that cannot be parsed (a date that is not an ISO date).

The checkout alone did not settle which status an out-of-range parameter gets, because the API interfaces that carry the parameter constraints are generated at build time. The run settled it: the constraints are enforced, the violation reaches the catch-all handler, and the answer is 500 (see "Observed").

Body values that violate a schema constraint (required, length, pattern, minimum, the pet age rule) are not part of this conflict: they raise `MethodArgumentNotValidException` and are answered with 400.

## Shared implementation evidence

- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:117 — "@ExceptionHandler(MethodArgumentNotValidException.class)"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:120 — "HttpStatus status = HttpStatus.BAD_REQUEST;"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:80 — "@ExceptionHandler(Exception.class)"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:84 — "HttpStatus status = HttpStatus.INTERNAL_SERVER_ERROR;"

## Affected endpoints

### GET /api/owners/{ownerId}

- contract: src/main/resources/openapi.yml:219 — "type: integer"
- contract: src/main/resources/openapi.yml:221 — "minimum: 0"
- contract: src/main/resources/openapi.yml:242 — "400:"
- rows: `petclinic|GET|/api/owners/{ownerId}|validation|negative-id`, `petclinic|GET|/api/owners/{ownerId}|validation|non-numeric-id`
- cases: `tests/petclinic/owners/case_get-owner-negative-id--nc420e.yaml`, `tests/petclinic/owners/case_get-owner-non-numeric-id--chcs2l.yaml`

### PUT /api/owners/{ownerId}

- contract: src/main/resources/openapi.yml:274 — "minimum: 0"
- contract: src/main/resources/openapi.yml:290 — "400:"
- row: `petclinic|PUT|/api/owners/{ownerId}|validation|negative-id`
- case: `tests/petclinic/owners/case_update-owner-negative-id--40xmj0.yaml`

### DELETE /api/owners/{ownerId}

- contract: src/main/resources/openapi.yml:323 — "minimum: 0"
- contract: src/main/resources/openapi.yml:344 — "400:"
- row: `petclinic|DELETE|/api/owners/{ownerId}|validation|negative-id`
- case: `tests/petclinic/owners/case_delete-owner-negative-id--vkjw4s.yaml`

### POST /api/owners/{ownerId}/pets

- contract: src/main/resources/openapi.yml:377 — "minimum: 0"
- contract: src/main/resources/openapi.yml:2169 — "format: date"
- contract: src/main/resources/openapi.yml:393 — "400:"
- rows: `petclinic|POST|/api/owners/{ownerId}/pets|validation|negative-owner-id`, `petclinic|POST|/api/owners/{ownerId}/pets|validation|birth-date-invalid-format`
- cases: `tests/petclinic/owner-pets/case_add-pet-negative-owner-id--v0fyv9.yaml`, `tests/petclinic/owner-pets/case_add-pet-birth-date-invalid-format--uyrlmh.yaml`

### GET /api/owners/{ownerId}/pets/{petId}

- contract: src/main/resources/openapi.yml:426 — "minimum: 0"
- contract: src/main/resources/openapi.yml:433 — "type: integer"
- contract: src/main/resources/openapi.yml:435 — "minimum: 0"
- contract: src/main/resources/openapi.yml:456 — "400:"
- rows: `petclinic|GET|/api/owners/{ownerId}/pets/{petId}|validation|negative-owner-id`, `petclinic|GET|/api/owners/{ownerId}/pets/{petId}|validation|negative-pet-id`, `petclinic|GET|/api/owners/{ownerId}/pets/{petId}|validation|non-numeric-pet-id`
- cases: `tests/petclinic/owner-pets/case_get-owners-pet-negative-owner-id--ccvxy5.yaml`, `tests/petclinic/owner-pets/case_get-owners-pet-negative-pet-id--az7izn.yaml`, `tests/petclinic/owner-pets/case_get-owners-pet-non-numeric-pet-id--8ijr4c.yaml`

### PUT /api/owners/{ownerId}/pets/{petId}

- contract: src/main/resources/openapi.yml:498 — "minimum: 0"
- contract: src/main/resources/openapi.yml:2169 — "format: date"
- contract: src/main/resources/openapi.yml:510 — "400:"
- rows: `petclinic|PUT|/api/owners/{ownerId}/pets/{petId}|validation|negative-pet-id`, `petclinic|PUT|/api/owners/{ownerId}/pets/{petId}|validation|birth-date-invalid-format`
- cases: `tests/petclinic/owner-pets/case_update-owners-pet-negative-pet-id--il0k1f.yaml`, `tests/petclinic/owner-pets/case_update-owners-pet-birth-date-invalid-format--nnuh52.yaml`

### POST /api/owners/{ownerId}/pets/{petId}/visits

- contract: src/main/resources/openapi.yml:552 — "minimum: 0"
- contract: src/main/resources/openapi.yml:2272 — "format: date"
- contract: src/main/resources/openapi.yml:568 — "400:"
- rows: `petclinic|POST|/api/owners/{ownerId}/pets/{petId}/visits|validation|negative-pet-id`, `petclinic|POST|/api/owners/{ownerId}/pets/{petId}/visits|validation|date-invalid-format`
- cases: `tests/petclinic/owner-visits/case_add-visit-negative-pet-id--cxyx5y.yaml`, `tests/petclinic/owner-visits/case_add-visit-date-invalid-format--0i0ked.yaml`

### GET /api/pets/{petId}

- contract: src/main/resources/openapi.yml:939 — "type: integer"
- contract: src/main/resources/openapi.yml:941 — "minimum: 0"
- contract: src/main/resources/openapi.yml:962 — "400:"
- rows: `petclinic|GET|/api/pets/{petId}|validation|negative-id`, `petclinic|GET|/api/pets/{petId}|validation|non-numeric-id`
- cases: `tests/petclinic/pets/case_get-pet-negative-id--9ap99f.yaml`, `tests/petclinic/pets/case_get-pet-non-numeric-id--es0dv0.yaml`

### PUT /api/pets/{petId}

- contract: src/main/resources/openapi.yml:994 — "minimum: 0"
- contract: src/main/resources/openapi.yml:2169 — "format: date"
- contract: src/main/resources/openapi.yml:1022 — "400:"
- rows: `petclinic|PUT|/api/pets/{petId}|validation|negative-id`, `petclinic|PUT|/api/pets/{petId}|validation|birth-date-invalid-format`
- cases: `tests/petclinic/pets/case_update-pet-negative-id--qx54ud.yaml`, `tests/petclinic/pets/case_update-pet-birth-date-invalid-format--jzlp82.yaml`

### DELETE /api/pets/{petId}

- contract: src/main/resources/openapi.yml:1054 — "minimum: 0"
- contract: src/main/resources/openapi.yml:1075 — "400:"
- row: `petclinic|DELETE|/api/pets/{petId}|validation|negative-id`
- case: `tests/petclinic/pets/case_delete-pet-negative-id--t8e6h7.yaml`

### POST /api/visits

- contract: src/main/resources/openapi.yml:2272 — "format: date"
- contract: src/main/resources/openapi.yml:1159 — "400:"
- row: `petclinic|POST|/api/visits|validation|date-invalid-format`
- case: `tests/petclinic/visits/case_create-visit-date-invalid-format--a8twwy.yaml`

### GET /api/visits/{visitId}

- contract: src/main/resources/openapi.yml:1190 — "type: integer"
- contract: src/main/resources/openapi.yml:1192 — "minimum: 0"
- contract: src/main/resources/openapi.yml:1213 — "400:"
- rows: `petclinic|GET|/api/visits/{visitId}|validation|negative-id`, `petclinic|GET|/api/visits/{visitId}|validation|non-numeric-id`
- cases: `tests/petclinic/visits/case_get-visit-negative-id--qx2vja.yaml`, `tests/petclinic/visits/case_get-visit-non-numeric-id--29dath.yaml`

### PUT /api/visits/{visitId}

- contract: src/main/resources/openapi.yml:1245 — "minimum: 0"
- contract: src/main/resources/openapi.yml:2272 — "format: date"
- contract: src/main/resources/openapi.yml:1273 — "400:"
- rows: `petclinic|PUT|/api/visits/{visitId}|validation|negative-id`, `petclinic|PUT|/api/visits/{visitId}|validation|date-invalid-format`
- cases: `tests/petclinic/visits/case_update-visit-negative-id--eb2344.yaml`, `tests/petclinic/visits/case_update-visit-date-invalid-format--mty5d5.yaml`

### DELETE /api/visits/{visitId}

- contract: src/main/resources/openapi.yml:1305 — "minimum: 0"
- contract: src/main/resources/openapi.yml:1326 — "400:"
- row: `petclinic|DELETE|/api/visits/{visitId}|validation|negative-id`
- case: `tests/petclinic/visits/case_delete-visit-negative-id--y8axc6.yaml`

### GET /api/v2/owners

- contract: src/main/resources/openapi.yml:159 — "type: integer"
- contract: src/main/resources/openapi.yml:161 — "minimum: 0"
- contract: src/main/resources/openapi.yml:171 — "minimum: 1"
- contract: src/main/resources/openapi.yml:172 — "maximum: 100"
- contract: src/main/resources/openapi.yml:194 — "400:"
- rows: `petclinic|GET|/api/v2/owners|validation|size-zero`, `petclinic|GET|/api/v2/owners|validation|size-over-max`, `petclinic|GET|/api/v2/owners|validation|page-negative`, `petclinic|GET|/api/v2/owners|validation|page-non-numeric`
- cases: `tests/petclinic/owners-v2/case_owners-page-size-zero--fcy9on.yaml`, `tests/petclinic/owners-v2/case_owners-page-size-over-max--rmqcg7.yaml`, `tests/petclinic/owners-v2/case_owners-page-negative-page--r8rrkf.yaml`, `tests/petclinic/owners-v2/case_owners-page-non-numeric-page--6n526i.yaml`

### GET /api/v2/pets

- contract: src/main/resources/openapi.yml:885 — "type: integer"
- contract: src/main/resources/openapi.yml:887 — "minimum: 0"
- contract: src/main/resources/openapi.yml:897 — "minimum: 1"
- contract: src/main/resources/openapi.yml:898 — "maximum: 100"
- contract: src/main/resources/openapi.yml:913 — "400:"
- rows: `petclinic|GET|/api/v2/pets|validation|size-zero`, `petclinic|GET|/api/v2/pets|validation|size-over-max`, `petclinic|GET|/api/v2/pets|validation|page-negative`, `petclinic|GET|/api/v2/pets|validation|page-non-numeric`
- cases: `tests/petclinic/pets-v2/case_pets-page-size-zero--o1mr4s.yaml`, `tests/petclinic/pets-v2/case_pets-page-size-over-max--ae9om3.yaml`, `tests/petclinic/pets-v2/case_pets-page-negative-page--kp5a3z.yaml`, `tests/petclinic/pets-v2/case_pets-page-non-numeric-page--8plgxn.yaml`

### GET, PUT, DELETE /api/pettypes/{petTypeId}

- contract: src/main/resources/openapi.yml:683 — "type: integer"
- contract: src/main/resources/openapi.yml:685 — "minimum: 0"
- contract: src/main/resources/openapi.yml:706 — "400:"
- contract: src/main/resources/openapi.yml:738 — "minimum: 0"
- contract: src/main/resources/openapi.yml:766 — "400:"
- contract: src/main/resources/openapi.yml:798 — "minimum: 0"
- contract: src/main/resources/openapi.yml:819 — "400:"
- rows: `petclinic|GET|/api/pettypes/{petTypeId}|validation|negative-id`, `petclinic|GET|/api/pettypes/{petTypeId}|validation|non-numeric-id`, `petclinic|PUT|/api/pettypes/{petTypeId}|validation|negative-id`, `petclinic|DELETE|/api/pettypes/{petTypeId}|validation|negative-id`
- cases: `tests/petclinic/pettypes/case_get-pet-type-negative-id--9g57hk.yaml`, `tests/petclinic/pettypes/case_get-pet-type-non-numeric-id--lpcmuc.yaml`, `tests/petclinic/pettypes/case_update-pet-type-negative-id--0gwexu.yaml`, `tests/petclinic/pettypes/case_delete-pet-type-negative-id--h7a01s.yaml`

### GET, PUT, DELETE /api/specialties/{specialtyId}

- contract: src/main/resources/openapi.yml:1441 — "type: integer"
- contract: src/main/resources/openapi.yml:1443 — "minimum: 0"
- contract: src/main/resources/openapi.yml:1464 — "400:"
- contract: src/main/resources/openapi.yml:1496 — "minimum: 0"
- contract: src/main/resources/openapi.yml:1524 — "400:"
- contract: src/main/resources/openapi.yml:1556 — "minimum: 0"
- contract: src/main/resources/openapi.yml:1577 — "400:"
- rows: `petclinic|GET|/api/specialties/{specialtyId}|validation|negative-id`, `petclinic|GET|/api/specialties/{specialtyId}|validation|non-numeric-id`, `petclinic|PUT|/api/specialties/{specialtyId}|validation|negative-id`, `petclinic|DELETE|/api/specialties/{specialtyId}|validation|negative-id`
- cases: `tests/petclinic/specialties/case_get-specialty-negative-id--zhty9u.yaml`, `tests/petclinic/specialties/case_get-specialty-non-numeric-id--wxhldh.yaml`, `tests/petclinic/specialties/case_update-specialty-negative-id--xiso8i.yaml`, `tests/petclinic/specialties/case_delete-specialty-negative-id--zt23lh.yaml`

### GET, PUT, DELETE /api/vets/{vetId}

- contract: src/main/resources/openapi.yml:1693 — "type: integer"
- contract: src/main/resources/openapi.yml:1695 — "minimum: 0"
- contract: src/main/resources/openapi.yml:1716 — "400:"
- contract: src/main/resources/openapi.yml:1748 — "minimum: 0"
- contract: src/main/resources/openapi.yml:1776 — "400:"
- contract: src/main/resources/openapi.yml:1808 — "minimum: 0"
- contract: src/main/resources/openapi.yml:1829 — "400:"
- rows: `petclinic|GET|/api/vets/{vetId}|validation|negative-id`, `petclinic|GET|/api/vets/{vetId}|validation|non-numeric-id`, `petclinic|PUT|/api/vets/{vetId}|validation|negative-id`, `petclinic|DELETE|/api/vets/{vetId}|validation|negative-id`
- cases: `tests/petclinic/vets/case_get-vet-negative-id--of42ds.yaml`, `tests/petclinic/vets/case_get-vet-non-numeric-id--7tsdmh.yaml`, `tests/petclinic/vets/case_update-vet-negative-id--i9ipcl.yaml`, `tests/petclinic/vets/case_delete-vet-negative-id--4wl4bs.yaml`

## Observed

Unmarked runs of 2026-10-04 (batch 1, then batch 2), `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`. All 44 cases got 500 with a ProblemDetail whose `detail` is "An unexpected error occurred while processing your request"; the `title` names the exception:

| Request | Expected (contract) | Actual |
|---|---|---|
| `GET /api/owners/-1` | 400 | 500, title `ConstraintViolationException` |
| `GET /api/owners/abc` | 400 | 500, title `MethodArgumentTypeMismatchException` |
| `GET /api/v2/owners?size=101` | 400 | 500, title `ConstraintViolationException` |
| `GET /api/v2/owners?page=abc` | 400 | 500, title `MethodArgumentTypeMismatchException` |
| `POST /api/owners/12/pets` with `"birthDate": "15/01/2020"` | 400 | 500, title `HttpMessageNotReadableException` |
| `DELETE /api/pettypes/-328` (pet type 328 created by the case) | 400 | 500, title `ConstraintViolationException` |
| `GET /api/vets/abc` | 400 | 500, title `MethodArgumentTypeMismatchException` |

The write cases stop at the failing step, so their follow-up checks (the owned record is unchanged) did not run. After the run the environment held only its seed data.

## Markers

The 44 cases above carry a `known_defects` marker with `ref: defects/invalid-request-values-not-answered-with-400.md`, the failing step and `at: status`; the contract assertions are unchanged, and the cases report XFAIL. When the handler maps these errors to 400 the cases report XPASS and the markers must be removed.
