# A user without roles is rejected although the contract requires only a username

- Status: suspected, not reproduced. Derived from reading the source at the pinned commit. The affected row is blocked, so no case exists and no request has been sent.
- Service: `petclinic`
- Endpoint: `POST /api/users`
- Source commit: `4cd8e1b0cd42578e882247d8801f6be5d402f118`

## Conflict

The contract's `User` requires only `username`; `roles` is an optional list. A user posted without roles is therefore valid and must be created. The service refuses such a user with an `IllegalArgumentException` before saving it. That exception is not a request-body validation error, so it reaches the catch-all handler, which answers 500.

## Evidence

- contract: src/main/resources/openapi.yml:2362 — "roles:"
- contract: src/main/resources/openapi.yml:2368 — "required:"
- contract: src/main/resources/openapi.yml:2369 — "- username"
- contract: src/main/resources/openapi.yml:1862 — "200:"
- implementation: src/main/java/org/springframework/samples/petclinic/service/UserServiceImpl.java:20 — "if(user.getRoles() == null || user.getRoles().isEmpty()) {"
- implementation: src/main/java/org/springframework/samples/petclinic/service/UserServiceImpl.java:21 — "throw new IllegalArgumentException("User must have at least a role set!");"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:80 — "@ExceptionHandler(Exception.class)"
- implementation: src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java:84 — "HttpStatus status = HttpStatus.INTERNAL_SERVER_ERROR;"

## Coverage rows and cases

- row: `petclinic|POST|/api/users|boundary|create-user-without-roles` (blocked)
- case: none. By contract the request creates a user, and the API has no operation to delete one, so a case asserting the contract cannot declare executable cleanup.

## Next step

Unblock the row by providing a way to remove test users. Then a case can post a user without roles, assert the documented success and remove the user in teardown.
