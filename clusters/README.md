# clusters/

Each folder is the target of one root Application and contains the Applications for that cluster, plus
small overlays for what differs:

| Setting | `local` (kind) | `azure` (AKS) |
|---------|----------------|---------------|
| Envoy Gateway service | NodePort 30080/30443 → 127.0.0.1:18080/18443 | LoadBalancer |
| `Database` default composition | `database-cnpg` | `database-azure` |
| Profile | `lite` (optionally `full`) | `lite` |
| Hostnames | `*.warden.localhost:18080` | `*.<lb-ip>.nip.io` |

Platform Applications in `../platform/` are shared; only the values/patches here differ.
