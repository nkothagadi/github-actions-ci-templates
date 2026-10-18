# github-actions-ci-templates

A reusable GitHub Actions workflow for a secure CI pipeline, plus a tiny sample service to prove it works.

## Pipeline

```
lint (ruff) -> unit tests -> docker build -> Trivy vulnerability scan (fails on CRITICAL)
```

- **Reusable:** `reusable-python-ci.yml` uses `workflow_call`, so other repos can call it in a few lines.
- **Least privilege:** workflows run with `permissions: contents: read`.
- **Supply-chain hygiene:** Dependabot keeps Actions and Docker base images up to date; the container runs as a non-root user.
- **Fast feedback:** concurrency control cancels superseded runs.

## Use it from another repo

```yaml
jobs:
  ci:
    uses: nkothagadi/github-actions-ci-templates/.github/workflows/reusable-python-ci.yml@main
    with:
      python-version: "3.12"
      image-name: my-service
```

## Run locally

```bash
python -m unittest discover -s app -t . -v     # tests
docker build -t demo-app .                      # image
docker run --rm -p 8080:8080 demo-app           # then: curl localhost:8080/healthz
```

## Layout

| Path | Purpose |
| --- | --- |
| `.github/workflows/reusable-python-ci.yml` | The reusable pipeline |
| `.github/workflows/ci.yml` | Calls the reusable workflow on push and PR |
| `app/` | Sample service (`/healthz`) and its tests |
| `Dockerfile` | Non-root container image |

## License

MIT
