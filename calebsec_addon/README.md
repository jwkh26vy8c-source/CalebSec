# CalebSec Add-On: RBAC/Auth, Live Log Ingestion, Sigma Rule Support

This zip adds a runnable Python/FastAPI security backend scaffold for **CalebSec**.

## Features included

- **RBAC / authentication**
  - SQLite user store
  - HMAC-signed bearer tokens
  - Roles: `admin`, `analyst`, `viewer`
  - Route-level permission checks

- **Live log ingestion**
  - REST endpoint for pushing logs
  - Optional file tailer for live ingestion from a log file
  - In-memory event stream
  - Simple alert creation when Sigma rules match

- **Sigma rule support**
  - Loads Sigma-style YAML rules from `rules/`
  - Supports common simple detections:
    - `selection` maps
    - field equality
    - field contains via `field|contains`
    - `keywords`
    - basic `condition: selection`
    - basic `condition: selection1 or selection2`
    - basic `condition: selection1 and selection2`

## Quick start

```bash
cd calebsec_addon
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python -m calebsec.main --init-db
python -m calebsec.main --serve
```

On Windows PowerShell:

```powershell
cd calebsec_addon
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py -m calebsec.main --init-db
py -m calebsec.main --serve
```

## Default login

After `--init-db`, a default admin user is created:

- Username: `admin`
- Password: `ChangeMe123!`

Change this immediately in a real deployment.

## API demo

Start the server, then open:

- <http://127.0.0.1:8000/docs>

Login:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"ChangeMe123!"}'
```

Copy the returned `access_token`, then ingest a log:

```bash
TOKEN="paste-token-here"

curl -X POST http://127.0.0.1:8000/ingest \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"source":"windows","event_id":4625,"message":"Failed password for admin from 10.0.0.8","user":"admin","src_ip":"10.0.0.8"}'
```

Check alerts:

```bash
curl http://127.0.0.1:8000/alerts \
  -H "Authorization: Bearer $TOKEN"
```

## Live file ingestion demo

In one terminal:

```bash
python -m calebsec.main --serve --tail sample_logs/auth.log
```

In another terminal:

```bash
echo '{"source":"linux-auth","message":"Failed password for root from 10.0.0.5","user":"root","src_ip":"10.0.0.5"}' >> sample_logs/auth.log
```

Then check `/alerts`.

## Integrating into an existing CalebSec project

You can either run this as its own service, or copy these folders into your existing project:

```text
calebsec/auth
calebsec/ingestion
calebsec/sigma
calebsec/api
calebsec/core
```

Mount the FastAPI router from `calebsec.api.routes` into your existing FastAPI app, or adapt the modules to your framework.

## Security notes

This is a development-ready scaffold, not a production hardening pass. Before production use:

- Move `CALEBSEC_SECRET` to a secure secret manager.
- Replace the default admin password.
- Put the API behind TLS.
- Add rate limiting to `/auth/login`.
- Persist events/alerts to a database instead of using only memory.
- Expand Sigma support if you need full Sigma backend compatibility.
