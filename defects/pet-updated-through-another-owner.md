# A pet can be updated through an owner it does not belong to

- Status: reproduced on 2026-10-04 against the `local` profile.
- Service: `petclinic`
- Endpoint: `PUT /api/owners/{ownerId}/pets/{petId}`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The contract answers 404 "Pet not found for this owner" when the pet in the path is not a pet of the owner in the path. The handler checks only that the owner exists and then loads the pet by its id alone, so a pet of another owner is updated and answered with 204.

The read operation on the same path does look the pet up among the owner's pets (`owner.getPet(petId)`, line 196 of the same controller), so the two operations disagree with each other.

## Evidence

- contract: src/main/resources/openapi.yml:516 — "404:"
- contract: src/main/resources/openapi.yml:517 — "description: Pet not found for this owner."
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:161 — "Owner currentOwner = this.clinicService.findOwnerById(ownerId);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:163 — "Pet currentPet = this.clinicService.findPetById(petId);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:168 — "this.clinicService.savePet(currentPet);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:169 — "return new ResponseEntity<>(HttpStatus.NO_CONTENT);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:196 — "Pet pet = owner.getPet(petId);"

## Coverage rows and cases

- row: `petclinic|PUT|/api/owners/{ownerId}/pets/{petId}|error|pet-of-another-owner`
- case: `tests/petclinic/owner-pets/case_update-pet-of-another-owner--xk8md3.yaml`

## Observed

First run of batch 1, 2026-10-04, `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`:

| Request | Expected (contract) | Actual |
|---|---|---|
| `PUT /api/owners/34/pets/26` with `{"name": "moved-f7457cf08a1d", "birthDate": "2021-06-30", "type": {...}}` (pet 26 belongs to owner 33) | 404 "Pet not found for this owner" | 204, empty body |

The case stops at that step, so its second step (the pet kept its values) did not run; the 204 means the update was accepted.

## Markers

`tests/petclinic/owner-pets/case_update-pet-of-another-owner--xk8md3.yaml` carries a `known_defects` marker with `ref: defects/pet-updated-through-another-owner.md`, the update step and `at: status`; the contract assertions are unchanged, and the case reports XFAIL. When the handler checks the owner the case reports XPASS and the marker must be removed.
