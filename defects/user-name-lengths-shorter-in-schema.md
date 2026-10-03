# User and role names up to 80 characters are allowed by the contract but the tables hold 20

- Status: suspected, not reproduced. Derived from reading the source at the pinned commit. The affected row is blocked, so no case exists and no request has been sent.
- Service: `petclinic`
- Endpoint: `POST /api/users`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The contract allows a `username` of up to 80 characters and a role `name` of up to 80 characters. The tables that store them declare both columns as `VARCHAR(20)`. A username or role name of 21 to 80 characters passes request validation and then does not fit its column; the insert fails, and the data-integrity handler answers such failures with 404.

## Evidence

- contract: src/main/resources/openapi.yml:2347 — "maxLength: 80"
- contract: src/main/resources/openapi.yml:2379 — "maxLength: 80"
- implementation: src/main/resources/db/h2/schema.sql:63 — "username VARCHAR(20) NOT NULL PRIMARY KEY,"
- implementation: src/main/resources/db/h2/schema.sql:71 — "role VARCHAR(20) NOT NULL,"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:97 — "@ExceptionHandler(DataIntegrityViolationException.class)"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:105 — "HttpStatus status = HttpStatus.NOT_FOUND;"

## Coverage rows and cases

- row: `petclinic|POST|/api/users|boundary|username-max-length-80` (blocked)
- case: none. By contract the request creates a user, and the API has no operation to delete one, so a case asserting the contract cannot declare executable cleanup.

## Next step

Unblock the row by providing a way to remove test users. Then a case can post a user with an 80-character username, assert the documented success and remove the user in teardown.
