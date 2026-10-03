# A list with no entries is answered with 404 instead of 200 and an empty array

- Status: reproduced on 2026-10-04 against the `local` profile for `GET /api/owners`. The five lists recorded as gaps have not been executed in the empty state.
- Service: `petclinic`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The list operations return an array and document only the responses 200, 304 and 500. No 404 is documented, so a result with no entries is a 200 with an empty array. Each controller checks `isEmpty()` and answers 404 with an empty body instead.

The business repository's own tests expect that 404 (`src/test/java/org/springframework/samples/petclinic/rest/controller/OwnerRestControllerV1Tests.java:197`), so this needs a decision on which side is wrong: the contract (missing 404) or the controllers.

Only `GET /api/owners` can reach the empty result without touching other data, through its `lastName` filter. For the other lists an empty collection cannot be arranged in a shared environment; those rows are recorded as gaps.

## Affected endpoints

### GET /api/owners

- contract: src/main/resources/openapi.yml:113 — "200:"
- contract: src/main/resources/openapi.yml:123 — "type: array"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:83 — "if (owners.isEmpty()) {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:84 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- rows: `petclinic|GET|/api/owners|error|filter-no-match` (authored), `petclinic|GET|/api/owners|state|empty-collection` (gap)
- case: `tests/petclinic/owners/case_list-owners-filter-no-match--j6rcno.yaml`

### GET /api/pets (gap row, no case)

- contract: src/main/resources/openapi.yml:846 — "200:"
- contract: src/main/resources/openapi.yml:856 — "type: array"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetRestControllerV1.java:66 — "if (pets.isEmpty()) {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetRestControllerV1.java:67 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|GET|/api/pets|state|empty-collection`

### GET /api/visits (gap row, no case)

- contract: src/main/resources/openapi.yml:1101 — "200:"
- contract: src/main/resources/openapi.yml:1111 — "type: array"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:59 — "if (visits.isEmpty()) {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:60 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|GET|/api/visits|state|empty-collection`

### GET /api/pettypes (gap row, no case)

- contract: src/main/resources/openapi.yml:594 — "200:"
- contract: src/main/resources/openapi.yml:604 — "type: array"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetTypeRestControllerV1.java:55 — "if (petTypes.isEmpty()) {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetTypeRestControllerV1.java:56 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|GET|/api/pettypes|state|empty-collection`

### GET /api/specialties (gap row, no case)

- contract: src/main/resources/openapi.yml:1352 — "200:"
- contract: src/main/resources/openapi.yml:1362 — "type: array"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/SpecialtyRestControllerV1.java:58 — "if (specialties.isEmpty()) {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/SpecialtyRestControllerV1.java:59 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|GET|/api/specialties|state|empty-collection`

### GET /api/vets (gap row, no case)

- contract: src/main/resources/openapi.yml:1603 — "200:"
- contract: src/main/resources/openapi.yml:1613 — "type: array"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VetRestControllerV1.java:60 — "if (vets.isEmpty()) {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VetRestControllerV1.java:61 — "return new ResponseEntity<>(HttpStatus.NOT_FOUND);"
- row: `petclinic|GET|/api/vets|state|empty-collection`

## Not affected

The paged operations `GET /api/v2/owners` and `GET /api/v2/pets` always answer 200 with a page object, also when the page is empty.

## Observed

First run of batch 1, 2026-10-04, `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`:

| Request | Expected (contract) | Actual |
|---|---|---|
| `GET /api/owners?lastName=<run-unique last name that no owner has>` | 200 with `[]` | 404, empty body |

## Markers

`tests/petclinic/owners/case_list-owners-filter-no-match--j6rcno.yaml` carries a `known_defects` marker with `ref: defects/list-answers-404-for-empty-result.md`, the list step and `at: status`; the contract assertion is unchanged, and the case reports XFAIL. When the contract or the controller is corrected the case reports XPASS and the marker must be removed.
