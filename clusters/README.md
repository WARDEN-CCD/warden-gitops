# clusters/

Each folder is the target of one root Application and contains the Applications for that cluster, plus
small overlays for what differs:

| Setting | `local` (kind) | `azure` (AKS) |
|---------|----------------|---------------|
| Envoy Gateway service | NodePort 30080/30443 → 127.0.0.1:18080/18443 | LoadBalancer |
| `Database` default composition | `database-cnpg` | `database-cnpg` (a `database-azure` composition is not written yet) |
| metrics-server | chart, `--kubelet-insecure-tls` | built into AKS (no chart) |
| Control-plane scrapes | off (kind) | off (managed control plane; Cilium replaces kube-proxy) |
| Profile | `lite` (optionally `full`) | `lite` |
| Hostnames | `<svc>.warden.localhost` via `127.0.0.1:18080` | same hostnames (apps/ is shared), sent as `Host:` to the LB IP |

Platform Applications in `../platform/` are shared; only the values/patches here differ.
