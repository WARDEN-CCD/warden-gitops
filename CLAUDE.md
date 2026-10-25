# CLAUDE.md — warden-gitops

This repo **is** the cluster's desired state; Argo CD applies it. Workspace rules: `../CLAUDE.md` (hub).

- Never add instructions that require `kubectl apply` by hand beyond `bootstrap/root-*.yaml`.
- Helm chart versions must match the hub's `versions.yaml` `charts` section. Upgrade there first.
- Images under `apps/` are always `name@sha256:<64 hex>` (verify.py enforces). Rollouts embed `template`;
  no `workloadRef`, no Deployments for services.
- Gateway API `HTTPRoute` for traffic. No `Ingress`.
- Policies are not defined here; Applications in `platform/kyverno/` point at the `warden-policy` repo.
- The `digest-only` workflow uses `pull_request_target` on purpose and must never check out or run PR code.
  Keep the script stdlib-only.
- Every Application: `automated: {prune: true, selfHeal: true}` and a sync-wave annotation.
- Every Application names a project from `platform/projects/` (one per source repo, hub ADR-029), never
  `default`, which is locked. A new kind, name or namespace for a source means editing its project in the same PR.
- Cluster differences live in `clusters/<name>/` overlays only; `platform/` stays cluster-agnostic.
