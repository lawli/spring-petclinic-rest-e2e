# A successful delete is answered with 204 and no body instead of 200 with the resource

- Status: reproduced on 2026-10-04 against the `local` profile for all six operations.
- Service: `petclinic`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The contract documents a successful delete as `200` with the deleted resource in the body, and lists no `204` response for these operations. The controllers return `new ResponseEntity<>(HttpStatus.NO_CONTENT)`, so the answer is 204 without a body.

The business repository's own tests expect 204 (`src/test/java/org/springframework/samples/petclinic/rest/controller/OwnerRestControllerV1Tests.java:330`), so this needs a decision on which side is wrong: the contract or the controllers.

## Affected endpoints

### DELETE /api/owners/{ownerId}

- contract: src/main/resources/openapi.yml:326 — "200:"
- contract: src/main/resources/openapi.yml:336 — "$ref: '#/components/schemas/Owner'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:136 — "return new ResponseEntity<>(HttpStatus.NO_CONTENT);"
- row: `petclinic|DELETE|/api/owners/{ownerId}|happy|delete-owner`
- case: `tests/petclinic/owners/case_delete-owner--3vq8a3.yaml`

### DELETE /api/pets/{petId}

- contract: src/main/resources/openapi.yml:1057 — "200:"
- contract: src/main/resources/openapi.yml:1067 — "$ref: '#/components/schemas/Pet'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetRestControllerV1.java:95 — "return new ResponseEntity<>(HttpStatus.NO_CONTENT);"
- row: `petclinic|DELETE|/api/pets/{petId}|happy|delete-pet`
- case: `tests/petclinic/pets/case_delete-pet--7kn7q7.yaml`

### DELETE /api/visits/{visitId}

- contract: src/main/resources/openapi.yml:1308 — "200:"
- contract: src/main/resources/openapi.yml:1318 — "$ref: '#/components/schemas/Visit'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:108 — "return new ResponseEntity<>(HttpStatus.NO_CONTENT);"
- row: `petclinic|DELETE|/api/visits/{visitId}|happy|delete-visit`
- case: `tests/petclinic/visits/case_delete-visit--ca5nsu.yaml`

### DELETE /api/pettypes/{petTypeId}

- contract: src/main/resources/openapi.yml:801 — "200:"
- contract: src/main/resources/openapi.yml:811 — "$ref: '#/components/schemas/PetType'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetTypeRestControllerV1.java:102 — "return new ResponseEntity<>(HttpStatus.NO_CONTENT);"
- row: `petclinic|DELETE|/api/pettypes/{petTypeId}|happy|delete-pet-type`
- case: `tests/petclinic/pettypes/case_delete-pet-type--faflq3.yaml`

### DELETE /api/specialties/{specialtyId}

- contract: src/main/resources/openapi.yml:1559 — "200:"
- contract: src/main/resources/openapi.yml:1569 — "$ref: '#/components/schemas/Specialty'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/SpecialtyRestControllerV1.java:105 — "return new ResponseEntity<>(HttpStatus.NO_CONTENT);"
- row: `petclinic|DELETE|/api/specialties/{specialtyId}|happy|delete-specialty`
- case: `tests/petclinic/specialties/case_delete-specialty--ccznu7.yaml`

### DELETE /api/vets/{vetId}

- contract: src/main/resources/openapi.yml:1811 — "200:"
- contract: src/main/resources/openapi.yml:1821 — "$ref: '#/components/schemas/Vet'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VetRestControllerV1.java:120 — "return new ResponseEntity<>(HttpStatus.NO_CONTENT);"
- row: `petclinic|DELETE|/api/vets/{vetId}|happy|delete-vet`
- case: `tests/petclinic/vets/case_delete-vet--dy4qrx.yaml`

## Observed

Unmarked runs of 2026-10-04 (batch 1, then batch 2), `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`:

| Request | Expected (contract) | Actual |
|---|---|---|
| `DELETE /api/owners/50` (owner created by the case) | 200 with the deleted Owner | 204, empty body |
| `DELETE /api/pets/40` (pet created by the case) | 200 with the deleted Pet | 204, empty body |
| `DELETE /api/visits/16` (visit created by the case) | 200 with the deleted Visit | 204, empty body |
| `DELETE /api/pettypes/327` (pet type created by the case) | 200 with the deleted PetType | 204, empty body |
| `DELETE /api/specialties/6` (specialty created by the case) | 200 with the deleted Specialty | 204, empty body |
| `DELETE /api/vets/12` (vet created by the case) | 200 with the deleted Vet | 204, empty body |

The records are removed: the six `state|get-after-delete` cases pass.

## Markers

The six cases above carry a `known_defects` marker with `ref: defects/delete-answers-204-instead-of-200.md`, the delete step and `at: status`; the contract assertions are unchanged, and the cases report XFAIL. When the contract or the controllers are corrected the cases report XPASS and the markers must be removed.
