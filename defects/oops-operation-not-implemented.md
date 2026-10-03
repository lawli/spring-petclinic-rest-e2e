# The contract's "oops" operation has no handler

- Status: reproduced on 2026-10-04 against the `local` profile.
- Service: `petclinic`
- Endpoint: `GET /api/oops`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The contract defines `GET /oops` as an operation that always fails and produces a sample error response: its 200 response is documented as "Never returned", and the error it documents is `400 Bad request` with a `ProblemDetail`.

The API interfaces are generated from the contract, one per tag, and a controller has to implement each of them. No class under `src/main/java` implements the interface for the `oops` tag, and no source file mentions `failingRequest` or `OopsApi`. The request therefore has no handler; an unmapped request raises an exception that reaches the catch-all handler, which answers 500.

## Evidence

- contract: src/main/resources/openapi.yml:33 — "/oops:"
- contract: src/main/resources/openapi.yml:37 — "operationId: failingRequest"
- contract: src/main/resources/openapi.yml:38 — "summary: Always fails"
- contract: src/main/resources/openapi.yml:42 — "description: Never returned."
- contract: src/main/resources/openapi.yml:59 — "400:"
- contract: src/main/resources/openapi.yml:64 — "$ref: '#/components/schemas/ProblemDetail'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:54 — "public class OwnerRestControllerV1 implements OwnersApi {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetRestControllerV1.java:41 — "public class PetRestControllerV1 implements PetsApi {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/PetTypeRestControllerV1.java:40 — "public class PetTypeRestControllerV1 implements PettypesApi {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/SpecialtyRestControllerV1.java:42 — "public class SpecialtyRestControllerV1 implements SpecialtiesApi {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/UserRestControllerV1.java:35 — "public class UserRestControllerV1 implements UsersApi {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VetRestControllerV1.java:44 — "public class VetRestControllerV1 implements VetsApi {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/VisitRestControllerV1.java:43 — "public class VisitRestControllerV1 implements VisitsApi {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v2/OwnerRestControllerV2.java:21 — "public class OwnerRestControllerV2 implements OwnerV2Api {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v2/PetRestControllerV2.java:21 — "public class PetRestControllerV2 implements PetV2Api {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/RootRestControllerV1.java:36 — "public class RootRestControllerV1 {"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:80 — "@ExceptionHandler(Exception.class)"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:84 — "HttpStatus status = HttpStatus.INTERNAL_SERVER_ERROR;"

## Coverage rows and cases

- row: `petclinic|GET|/api/oops|error|always-fails-with-problem-detail`
- case: `tests/petclinic/platform/case_oops-always-fails--u4klq6.yaml`

## Observed

Unmarked run of batch 2, 2026-10-04, `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`:

| Request | Expected (contract) | Actual |
|---|---|---|
| `GET /api/oops` | 400 with a ProblemDetail | 500 with a ProblemDetail: title `NoResourceFoundException`, detail "An unexpected error occurred while processing your request" |

## Markers

`tests/petclinic/platform/case_oops-always-fails--u4klq6.yaml` carries a `known_defects` marker with `ref: defects/oops-operation-not-implemented.md`, the call step and `at: status`; the contract assertion is unchanged, and the case reports XFAIL. When the operation is implemented or removed from the contract the case reports XPASS and the marker must be removed.
