# The owner entity accepts only 10-digit telephones while the contract allows 1 to 20 digits

- Status: reproduced on 2026-10-04 against the `local` profile for both operations.
- Service: `petclinic`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The contract's `OwnerFields.telephone` is a string of 1 to 20 digits. The `Owner` entity declares that the telephone must match exactly 10 digits. A telephone of any other length that the contract allows (for example 20 digits) passes request validation and then meets the entity constraint when the owner is stored.

That failure is not a request-body validation error, so it is not mapped to 400; it reaches the catch-all handler, which answers 500. The run confirmed that the entity constraint is enforced when the owner is stored (see "Observed").

## Shared evidence

- contract: src/main/resources/openapi.yml:2030 — "minLength: 1"
- contract: src/main/resources/openapi.yml:2031 — "maxLength: 20"
- contract: src/main/resources/openapi.yml:2032 — "pattern: '^[0-9]*$'"
- implementation: src/main/java/org/springframework/samples/petclinic/model/Owner.java:48 — "@Digits(fraction = 0, integer = 10)"
- implementation: src/main/java/org/springframework/samples/petclinic/model/Owner.java:49 — "@Pattern(regexp = "^[0-9]{10}$", message = "Phone number must be exactly 10 digits")"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:80 — "@ExceptionHandler(Exception.class)"

## Affected endpoints

### POST /api/owners

- contract: src/main/resources/openapi.yml:77 — "$ref: '#/components/schemas/OwnerFields'"
- contract: src/main/resources/openapi.yml:80 — "201:"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:104 — "this.clinicService.saveOwner(owner);"
- row: `petclinic|POST|/api/owners|boundary|telephone-max-length-20`
- case: `tests/petclinic/owners/case_create-owner-telephone-max-length--ntsvzo.yaml`

### PUT /api/owners/{ownerId}

- contract: src/main/resources/openapi.yml:281 — "$ref: '#/components/schemas/OwnerFields'"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:122 — "currentOwner.setTelephone(ownerFieldsDto.getTelephone());"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java:123 — "this.clinicService.saveOwner(currentOwner);"
- row: `petclinic|PUT|/api/owners/{ownerId}|boundary|telephone-max-length-20`
- case: `tests/petclinic/owners/case_update-owner-telephone-max-length--uxmqm7.yaml`

## Observed

First run of batch 1, 2026-10-04, `local` profile, reference commit `4cd8e1b0cd42578e882247d8801f6be5d402f118`:

| Request | Expected (contract) | Actual |
|---|---|---|
| `POST /api/owners` with `"telephone": "12345678901234567890"` | 201 with the stored Owner | 500, title `ConstraintViolationException`; no owner stored |
| `PUT /api/owners/65` with `"telephone": "12345678901234567890"`, then `GET /api/owners/65` | telephone is the 20-digit number | PUT answers 500, title `TransactionSystemException`; GET still shows `"telephone":"6085550100"` |

## Markers

Both cases carry a `known_defects` marker with `ref: defects/owner-telephone-stricter-than-contract.md`: the create case at its create step, `at: status`; the update case at its read-back step, `at: json.telephone`. The contract assertions are unchanged, and the cases report XFAIL. The fix is a decision between the two declarations: narrow the contract to 10 digits or relax the entity. After it, the cases report XPASS and the markers must be removed.

The create case cleans up through `tests/petclinic/owners/_helpers/cleanup.py`, because a rejected create returns no id for a declarative teardown step to use.
