# A successful create is answered with 201 instead of the documented 200

- Status: reproduced on 2026-10-04 against the `local` profile for four operations. `POST /api/users` has not been executed: its row is blocked.
- Service: `petclinic`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

For the operations below the contract documents success as `200` ("created successfully") and lists no `201` response. The controllers build the response with `HttpStatus.CREATED`, so the answer is 201.

Three other create operations document 201 and return 201 (see "Not affected"), so the contract is inconsistent with itself; this needs a decision on whether these five operations should document 201 or the controllers should return 200.

## Affected endpoints

### POST /api/visits

- contract: src/main/resources/openapi.yml:1141 — "200:"
- contract: src/main/resources/openapi.yml:1142 — "description: visit created successfully."
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:83 — "return new ResponseEntity<>(visitDto, headers, HttpStatus.CREATED);"
- row: `petclinic|POST|/api/visits|happy|create-visit`
- case: `tests/petclinic/visits/case_create-visit--isxqib.yaml`

### POST /api/pettypes

- contract: src/main/resources/openapi.yml:634 — "200:"
- contract: src/main/resources/openapi.yml:635 — "description: Pet type created successfully."
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetTypeRestControllerV1.java:78 — "return new ResponseEntity<>(petTypeMapper.toPetTypeDto(type), headers, HttpStatus.CREATED);"
- row: `petclinic|POST|/api/pettypes|happy|create-pet-type`
- case: `tests/petclinic/pettypes/case_create-pet-type--q17hhj.yaml`

### POST /api/specialties

- contract: src/main/resources/openapi.yml:1392 — "200:"
- contract: src/main/resources/openapi.yml:1393 — "description: Specialty created successfully."
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/SpecialtyRestControllerV1.java:81 — "return new ResponseEntity<>(specialtyMapper.toSpecialtyDto(specialty), headers, HttpStatus.CREATED);"
- row: `petclinic|POST|/api/specialties|happy|create-specialty`
- case: `tests/petclinic/specialties/case_create-specialty--ud88cp.yaml`

### POST /api/vets

- contract: src/main/resources/openapi.yml:1644 — "200:"
- contract: src/main/resources/openapi.yml:1645 — "description: Vet created successfully."
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VetRestControllerV1.java:87 — "return new ResponseEntity<>(vetMapper.toVetDto(vet), headers, HttpStatus.CREATED);"
- row: `petclinic|POST|/api/vets|happy|create-vet-without-specialties`
- case: `tests/petclinic/vets/case_create-vet--839o3n.yaml`

### POST /api/users (row blocked: no cleanup path for created users)

- contract: src/main/resources/openapi.yml:1862 — "200:"
- contract: src/main/resources/openapi.yml:1863 — "description: User created successfully."
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/UserRestControllerV1.java:52 — "return new ResponseEntity<>(userMapper.toUserDto(user), headers, HttpStatus.CREATED);"
- row: `petclinic|POST|/api/users|happy|create-user`

## Not affected

`POST /api/owners` (`src/main/resources/openapi.yml:80`), `POST /api/owners/{ownerId}/pets` (`:387`) and `POST /api/owners/{ownerId}/pets/{petId}/visits` (`:562`) document 201, and their handlers return 201.

## Observed

Unmarked runs of 2026-10-04 (batch 1, then batch 2), `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`:

| Request | Expected (contract) | Actual |
|---|---|---|
| `POST /api/visits` with `{"date": "2024-03-10", "description": "apitest-9d3d991b1573 checkup", "petId": 58}` | 200 with the stored Visit | 201 with `{"description":"apitest-9d3d991b1573 checkup","id":13,"petId":58,"date":"2024-03-10"}` |
| `POST /api/pettypes` with `{"name": "apitest-type-9e5dc75f7582"}` | 200 with the stored PetType | 201 with `{"name":"apitest-type-9e5dc75f7582","id":325}` |
| `POST /api/specialties` with `{"name": "apitest-specialty-499e5eb993ec"}` | 200 with the stored Specialty | 201 with `{"id":4,"name":"apitest-specialty-499e5eb993ec"}` |
| `POST /api/vets` with `{"firstName": "Apitest", "lastName": "Vetcbjpbibhhgpo", "specialties": []}` | 200 with the stored Vet | 201 with `{"firstName":"Apitest","lastName":"Vetcbjpbibhhgpo","specialties":[],"id":8}` |

The bodies match the contract; only the status differs.

## Markers

The four cases above carry a `known_defects` marker with `ref: defects/create-answers-201-instead-of-200.md`, the create step and `at: status`; the contract assertions are unchanged, and the cases report XFAIL. When the contract or the controllers are corrected the cases report XPASS and the markers must be removed.
