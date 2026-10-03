# A visit is created for a pet without checking that the pet belongs to the owner in the path

- Status: reproduced on 2026-10-04 against the `local` profile.
- Service: `petclinic`
- Endpoint: `POST /api/owners/{ownerId}/pets/{petId}/visits`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The contract answers 404 "Pet not found for this owner" when the pet in the path is not a pet of the owner in the path. The handler receives the owner id but never uses it: it builds a pet reference from the pet id alone and stores the visit. A visit for an existing pet is therefore created with 201 whatever the owner id is, including an owner that does not exist or another owner.

## Evidence

- contract: src/main/resources/openapi.yml:574 — "404:"
- contract: src/main/resources/openapi.yml:575 — "description: Pet not found for this owner."
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:177 — "public ResponseEntity<VisitDto> addVisitToOwner(Integer ownerId, Integer petId, VisitFieldsDto visitFieldsDto) {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:181 — "pet.setId(petId);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:183 — "this.clinicService.saveVisit(visit);"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:187 — "return new ResponseEntity<>(visitDto, headers, HttpStatus.CREATED);"

## Coverage rows and cases

- rows: `petclinic|POST|/api/owners/{ownerId}/pets/{petId}/visits|error|pet-of-another-owner`, `petclinic|POST|/api/owners/{ownerId}/pets/{petId}/visits|error|unknown-owner`
- cases: `tests/petclinic/owner-visits/case_add-visit-pet-of-another-owner--fddlmg.yaml`, `tests/petclinic/owner-visits/case_add-visit-unknown-owner--exjljl.yaml`

## Not affected

A pet id that matches no pet is answered with 404 and a `ProblemDetail` through the data-integrity handler, which agrees with the contract (`tests/petclinic/owner-visits/case_add-visit-unknown-pet--pb9d2r.yaml`).

## Observed

First run of batch 1, 2026-10-04, `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`:

| Request | Expected (contract) | Actual |
|---|---|---|
| `POST /api/owners/43/pets/34/visits` with a valid body (pet 34 belongs to owner 42) | 404 "Pet not found for this owner" | 201 with `{"description":"apitest-d611aac4a5ae checkup","id":7,"petId":34,"date":"2024-03-10"}` |
| `POST /api/owners/0/pets/36/visits` with a valid body (no owner 0 exists) | 404 "Pet not found for this owner" | 201 with `{"description":"apitest-6d01d014080c checkup","id":9,"petId":36,"date":"2024-03-10"}` |

Both visits were stored against the contract. Each case deletes its pet in teardown, which removed the visit; nothing was left after the run.

## Markers

Both cases carry a `known_defects` marker with `ref: defects/visit-created-without-checking-owner.md`, the create step and `at: status`; the contract assertions are unchanged, and the cases report XFAIL. When the handler checks the owner the cases report XPASS and the markers must be removed.
