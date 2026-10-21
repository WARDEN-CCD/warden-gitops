# apps/

One directory per service, created by `warden new` (see `warden-platform/templates/spring-service/README.md`).
An ApplicationSet with a Git directory generator turns each `apps/<svc>/` into an Argo CD Application in
namespace `svc-<svc>`, sync wave `10`.

Only the promotion bot changes image digests, one line per PR, guarded by `.github/scripts/digest_only.py`.
