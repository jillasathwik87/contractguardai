# ContractGuard AI — Reference Design Redesign

This project keeps the supplied ContractGuard AI backend and replaces the frontend with a new responsive design based on the provided reference image and requirements.

## Included pages
- Dashboard
- Contracts / Upload Contract
- My Contracts
- Compliance Rules
- Ask AI
- Settings

## Required behavior
- Dashboard has an Upload Contract entry point.
- Uploading and **Analyze Contract** happen only on the dedicated Contracts page.
- Analysis results, compliance score, checklist and AI summary stay on that same page.
- Ask AI is a separate page and calls `POST /api/ask`.
- Contract analysis calls the existing `POST /api/analyze` endpoint.
- My Contracts uses browser-local analysis history.
- Settings includes Dark Mode, local data controls and API URL configuration.
- Responsive layout follows the supplied desktop dashboard and adapts to mobile.

## Run locally

Backend + frontend together:

```bash
pip install -r requirements.txt
uvicorn api:api --host 0.0.0.0 --port 8000
```

Then open:

```text
http://127.0.0.1:8000
```

The existing Dockerfile can also run the FastAPI service.

## GitHub / public deployment

Push the repository contents to GitHub. The application needs a server that can run the Python/FastAPI backend for `/api/analyze`, `/api/ask` and `/api/health`.

If the frontend and backend are deployed together, no API URL needs to be configured.

If they are deployed separately:
1. Deploy the FastAPI backend.
2. Open Settings in ContractGuard.
3. Enter the backend base URL under **API Base URL**.
4. Save and test the connection.
5. Serve the frontend from the chosen static host.

GitHub Pages by itself can host the static UI, but it does not run this FastAPI backend. For full upload + AI analysis, deploy the backend on a Python/Docker-capable server and point the frontend to it.

## Security note

The supplied project contained local generated vector-store files, logs and a Streamlit secrets file. Those are intentionally excluded from this GitHub-ready redesign package. Put production credentials in the deployment platform's environment/secrets settings instead of committing them to Git.
