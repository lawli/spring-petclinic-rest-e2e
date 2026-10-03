# A successful update is answered with 204 and no body instead of 200 with the resource

- Status: reproduced on 2026-10-04 against the `local` profile for all six operations.
- Service: `petclinic`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The contract documents a successful update as `200` with the updated resource in the body, and lists no `204` response for these operations. The controllers build the response with `HttpStatus.NO_CONTENT`, so the answer is 204 without a body.

The business repository's own tests expect 204 (`src/test/java/org/springframework/samples/petclinic/rest/controller/OwnerRestControllerV1Tests.java:269`), so this needs a decision on which side is wrong: the contract or the controllers.

## Affected endpoints

### PUT /api/owners/{ownerId}

- contract: src/main/resources/openapi.yml:284 — "200:"
- contract: src/main/resources/openapi.yml:289 — "$ref: '#/components/schemas/Owner'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:124 — "return new ResponseEntity<>(ownerMapper.toOwnerDto(currentOwner), HttpStatus.NO_CONTENT);"
- row: `petclinic|PUT|/api/owners/{ownerId}|happy|update-owner`
- case: `tests/petclinic/owners/case_update-owner--d8gi8t.yaml`

### PUT /api/pets/{petId}

- contract: src/main/resources/openapi.yml:1004 — "200:"
- contract: src/main/resources/openapi.yml:1014 — "$ref: '#/components/schemas/Pet'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetRestControllerV1.java:84 — "return new ResponseEntity<>(petMapper.toPetDto(currentPet), HttpStatus.NO_CONTENT);"
- row: `petclinic|PUT|/api/pets/{petId}|happy|update-pet`
- case: `tests/petclinic/pets/case_update-pet--adznpv.yaml`

### PUT /api/visits/{visitId}

- contract: src/main/resources/openapi.yml:1255 — "200:"
- contract: src/main/resources/openapi.yml:1265 — "$ref: '#/components/schemas/Visit'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:96 — "return new ResponseEntity<>(visitMapper.toVisitDto(currentVisit), HttpStatus.NO_CONTENT);"
- row: `petclinic|PUT|/api/visits/{visitId}|happy|update-visit`
- case: `tests/petclinic/visits/case_update-visit--q7i0k2.yaml`

### PUT /api/pettypes/{petTypeId}

- contract: src/main/resources/openapi.yml:748 — "200:"
- contract: src/main/resources/openapi.yml:758 — "$ref: '#/components/schemas/PetType'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetTypeRestControllerV1.java:90 — "return new ResponseEntity<>(petTypeMapper.toPetTypeDto(currentPetType), HttpStatus.NO_CONTENT);"
- row: `petclinic|PUT|/api/pettypes/{petTypeId}|happy|update-pet-type`
- case: `tests/petclinic/pettypes/case_update-pet-type--qfq70g.yaml`

### PUT /api/specialties/{specialtyId}

- contract: src/main/resources/openapi.yml:1506 — "200:"
- contract: src/main/resources/openapi.yml:1516 — "$ref: '#/components/schemas/Specialty'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/SpecialtyRestControllerV1.java:93 — "return new ResponseEntity<>(specialtyMapper.toSpecialtyDto(currentSpecialty), HttpStatus.NO_CONTENT);"
- row: `petclinic|PUT|/api/specialties/{specialtyId}|happy|update-specialty`
- case: `tests/petclinic/specialties/case_update-specialty--blddou.yaml`

### PUT /api/vets/{vetId}

- contract: src/main/resources/openapi.yml:1758 — "200:"
- contract: src/main/resources/openapi.yml:1768 — "$ref: '#/components/schemas/Vet'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VetRestControllerV1.java:108 — "return new ResponseEntity<>(vetMapper.toVetDto(currentVet), HttpStatus.NO_CONTENT);"
- row: `petclinic|PUT|/api/vets/{vetId}|happy|update-vet`
- case: `tests/petclinic/vets/case_update-vet--wynvle.yaml`

## Not affected

`PUT /api/owners/{ownerId}/pets/{petId}` documents 204 (`src/main/resources/openapi.yml:508`) and the controller returns 204, so contract and implementation agree there.

## Observed

Unmarked runs of 2026-10-04 (batch 1, then batch 2), `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`:

| Request | Expected (contract) | Actual |
|---|---|---|
| `PUT /api/owners/60` with a valid OwnerFields body | 200 with the updated Owner | 204, empty body |
| `PUT /api/pets/47` with a valid Pet body | 200 with the updated Pet | 204, empty body |
| `PUT /api/visits/22` with `{"date": "2024-04-20", "description": "apitest-4033de894839 follow-up"}` | 200 with the updated Visit | 204, empty body |
| `PUT /api/pettypes/334` with `{"id": 334, "name": "apitest-renamed-1a7d9259c2ec"}` | 200 with the updated PetType | 204, empty body |
| `PUT /api/specialties/13` with `{"name": "apitest-renamed-99a521b668b5"}` | 200 with the updated Specialty | 204, empty body |
| `PUT /api/vets/18` with a valid Vet body | 200 with the updated Vet | 204, empty body |

The updates themselves are applied: the six `state|update-persists` cases pass.

## Markers

The six cases above carry a `known_defects` marker with `ref: defects/update-answers-204-instead-of-200.md`, the update step and `at: status`; the contract assertions are unchanged, and the cases report XFAIL. When the contract or the controllers are corrected the cases report XPASS and the markers must be removed.
