# spring-petclinic-rest-e2e

API end-to-end tests for
[spring-petclinic-rest](https://github.com/spring-petclinic/spring-petclinic-rest), generated
with [repo2test](https://github.com/lawli/repo2test) 0.2.4 as a demonstration. An agent
following the pinned workspace skill wrote the coverage inventory, the cases and the defect
notes. They are published as generated.

| | |
|---|---|
| Source reference | spring-petclinic-rest at commit `4cd8e1b` |
| Inventory (`coverage/`) | 44 endpoints, 307 behaviors |
| Cases (`tests/`) | 202 |
| Not authored | 82 behaviors blocked, 23 recorded as gaps |
| Last local run | 109 passed, 92 expected failures, 1 failed |

- **Expected failures** reproduce places where the service and its OpenAPI contract disagree.
  `defects/` has one note per conflict: 13 notes, 11 reproduced by a case and 2 based on the
  source only.
- **The one failure** is a pending expectation. The contract does not say whether deleting an
  owner may also remove a pet type, so the case is not marked as a defect.
- **Blocked behaviors** need a target with security enabled and one test identity per role, or
  a way to remove test users.

## Run it

1. Start spring-petclinic-rest at the reference commit with `./mvnw spring-boot:run`. By
   default it listens on `http://localhost:9966/petclinic`.
2. In this repository:

   ```sh
   uv sync --locked
   uv run --locked apitest workspace configure --profile local --service petclinic \
     --url http://localhost:9966/petclinic
   uv run --locked apitest run --service petclinic --profile local --report both
   ```

The cases create and delete their own records. Run them only against a disposable instance.

## Workspace setup

Run `uv sync --locked`, then `uv run --locked apitest --help`.
Configure service URLs with `apitest workspace configure`; environment values stay local.
Install the entry with `python3 tools/install_entry.py --host codex` or `--host claude`.
Use `--update` to deliberately replace an installed entry. For sibling workspace access, start Codex with `--add-dir <workspace> --add-dir "$(uv cache dir)"` (add `-c sandbox_workspace_write.network_access=true` when uv must download packages); start Claude Code with `--add-dir <workspace>`.

Platform setup: require the validate check and up-to-date branches or a merge queue/train; require CODEOWNERS approval by a runner maintainer other than the PR author for wheel/lock changes. Enable the default-branch push check. These platform settings must be configured by a repository administrator; generating YAML does not enforce them.
