# API Monitoring Dashboard Using FastAPI

A sample REST API monitoring project built with **FastAPI, Prometheus, Grafana, and Docker Compose**. It demonstrates API availability monitoring, response-time tracking, error detection, alerting, email notifications, and failure simulation.

## Table of Contents

- [Project Overview]
- [Architecture]
- [Technology Stack]
- [Features]
- [Project Structure]
- [Prerequisites]
- [Setup and Installation]
- [Access the Services]
- [API Endpoints]
- [Grafana Dashboard]
- [Alert Rules]
- [Failure Simulation and Testing]
- [Troubleshooting]
- [Security Notes]
- [Limitations and Future Improvements]

## Project Overview

The goal of this project is to monitor a sample FastAPI service and demonstrate how common API problems can be detected and reported.

FastAPI exposes application endpoints and Prometheus metrics. Prometheus scrapes those metrics, while Grafana displays the results and evaluates alert rules. Grafana is configured to send email notifications when configured alert conditions are met.

## Architecture

```text
Client / Test Requests
        |
        v
   FastAPI Service ------------------> /metrics
        |                                  |
        |                                  v
        |                             Prometheus
        |                                  |
        |                                  v
        +----------------------------> Grafana
                                           |
                                  Dashboard and Alert Rules
                                           |
                                           v
                                    Email Notifications
```

- **FastAPI** serves API requests and the metrics endpoint.
- **Prometheus FastAPI Instrumentator** collects request metrics.
- **Prometheus** scrapes the API metrics endpoint.
- **Grafana** queries Prometheus, displays dashboard panels, and evaluates alerts.
- **Docker Compose** runs Prometheus and Grafana.
- **Gmail SMTP** is used as the configured email notification channel.

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Prometheus
- `prometheus-fastapi-instrumentator`
- Grafana
- Docker Compose
- Python Requests for endpoint testing
- Gmail SMTP for email notifications

## Features

- API availability monitoring through Prometheus target status.
- Request-count and response-time metrics.
- Monitoring of HTTP client errors (4xx) and server errors (5xx).
- Grafana dashboard for service and request metrics.
- Alert rules for downtime, slow responses, HTTP 500 errors, increased failure rate, authentication simulation, and rate-limit simulation.
- Email notifications through a Grafana contact point.
- Endpoints for simulating failures and delayed responses.

## Project Structure

The repository should contain the following files (some folders may need to be created or exported):

```text
FastAPI-New-Age/
├── main.py
├── requirements.txt
├── compose.yaml
├── prometheus.yml
├── README.md
├── .gitignore
├── New Age FastAPI Monitoring -Grafana.json
```

The `grafana/dashboard.json`, `docs/`, and `screenshots/` entries are recommended repository artifacts. Add them if you have exported or captured them. Do not include screenshots or files that you have not actually created.

## Prerequisites

Install the following on your computer:

- Python (the project was developed with Python 3.13 in the current environment)
- Visual Studio Code or another code editor
- Docker Desktop with Docker Compose
- Git, if you want to push the project from the terminal

## Setup and Installation

### 1. Clone the repository

After uploading this project to GitHub, clone it with:

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_FOLDER>
```

Or open the existing project folder in VS Code.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, follow your local organization's policy or activate the environment using a supported terminal.

### 3. Install Python dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` is not present, create one from the working environment with `pip freeze > requirements.txt`, then review it before committing.

### 4. Configure Prometheus

The `prometheus.yml` configuration should point to the FastAPI metrics endpoint. The current local Docker setup uses a configuration similar to:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["prometheus:9090"]

  - job_name: "fastapi_app_new_age"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["host.docker.internal:8000"]
```

`host.docker.internal` lets a Docker container reach a service running on the Windows host. If your environment is different, update the target accordingly.

### 5. Start Prometheus and Grafana

Make sure Docker Desktop is running. From the directory containing `compose.yaml`, run:

```powershell
docker compose up -d
```

Check that the containers are running:

```powershell
docker ps
```

To stop the monitoring containers later:

```powershell
docker compose down
```

### 6. Start the FastAPI application

Open a separate terminal in the project folder, activate the virtual environment, and run:

```powershell
python -m uvicorn main:app --reload
```

Keep this terminal open while testing. The `--reload` option is useful for development; it is not intended as a production deployment setting.

### 7. Verify the application

Open these addresses in a browser:

- `http://localhost:8000/health`
- `http://localhost:8000/docs`
- `http://localhost:8000/metrics`

The health endpoint should return a healthy status when the application is running. The metrics endpoint should expose Prometheus-formatted metrics.

## Access the Services

| Service | Local address | Purpose |
|---|---|---|
| FastAPI | `http://localhost:8000` | API service |
| FastAPI Swagger UI | `http://localhost:8000/docs` | Explore and test endpoints |
| Prometheus | `http://localhost:9090` | Query metrics and inspect targets |
| Prometheus Targets | `http://localhost:9090/targets` | Check scrape status |
| Grafana | `http://localhost:3000` | Dashboard and alert management |

Grafana credentials depend on the values in your local Compose configuration. Do not publish passwords or SMTP credentials in this repository.

## API Endpoints

The project includes endpoints for normal requests and controlled failure simulations. Verify the exact route names in `main.py` before using them, because the route names below reflect the routes tested during development.

| Endpoint | Expected behavior |
|---|---|
| `/health` | Returns the API health status |
| `/users` | Returns sample user data |
| `/products` | Returns sample product data |
| `/simulate_error` | Simulates an HTTP 500 server error |
| `/simulate_timeout` | Waits about 5 seconds before responding |
| `/simulate_rate_limit` | Simulates an HTTP 429 rate-limit response |
| `/simulate_authentication_error` | Simulates an authentication failure (4xx) |
| `/simulate_timeout_scenario_2` | Waits 30 seconds to test a client-side timeout |
| `/metrics` | Exposes metrics for Prometheus |

Some route names may use hyphens or underscores depending on the current `main.py`. The actual registered route in the application is authoritative.

### Test endpoints from PowerShell

Check a rate-limit response:

```powershell
python -c "import requests; r = requests.get('http://localhost:8000/simulate_rate_limit'); print('Status code:', r.status_code); print('Response:', r.text)"
```

Test the delayed endpoint with a five-second client timeout:

```powershell
python -c "import requests; r = requests.get('http://localhost:8000/simulate_timeout_scenario_2', timeout=5); print(r.status_code)"
```

The second command is expected to raise `requests.exceptions.ReadTimeout` if the endpoint waits 30 seconds. That demonstrates a **client-side timeout**; it does not, by itself, prove that Grafana has a dedicated timeout alert.

## Grafana Dashboard

The dashboard developed for this project includes panels for:

1. **Total API Requests** — total requests recorded by the instrumentator.
2. **API Service Status** — the Prometheus `up` metric for the FastAPI target (`1` means Prometheus can scrape it; `0` means it cannot).
3. **Average Response Time** — average request duration over a recent time window.
4. **Failed Request Rate** — percentage of requests recorded as 4xx or 5xx.
5. **API Error Trends** — recorded client- and server-error trends over time.

To share the dashboard, export it from Grafana as JSON and save the file under `grafana/dashboard.json`. Dashboard JSON does not necessarily include alert rules, data-source credentials, or contact-point secrets; configure those separately in the receiving Grafana instance.

## Alert Rules

The following alert rules were configured during testing:

| Alert rule | Condition/purpose |
|---|---|
| `New Age FastAPI API Downtime` | Prometheus `up` metric is below `1` |
| `Delay Response Time` | Average response time for the monitored slow endpoint is above 3 seconds |
| `New Age FastAPI HTTP 500 Error` | New 5xx requests are detected |
| `New Age FastAPI High Failure Rate` | 4xx/5xx failure rate exceeds the configured 5% threshold |
| `FastAPI Authentication Failure` | Authentication simulation produces a 4xx response |
| `FastAPI Rate Limit Exceeded` | Rate-limit simulation produces a 4xx response |

The rules use a configured Grafana Gmail contact point. Rule names and conditions should be checked against the current Grafana configuration before submission.

### Email setup

Configure SMTP in the local Grafana Compose configuration using environment variables. Keep actual credentials in a local `.env` file or another secret-management method, and do not commit that file. If using Gmail, use an App Password where applicable and never publish it.

## Failure Simulation and Testing

The following outcomes were observed during development. Repeat the tests and include your own screenshots when preparing a final submission.

| Scenario | Verification | Observed outcome |
|---|---|---|
| API downtime | Stop Uvicorn while Docker services remain running; inspect Prometheus Targets and Grafana alert state | Prometheus target showed DOWN during testing; a Grafana downtime email was received in an earlier test |
| Slow response | Call the endpoint that waits about 5 seconds and inspect its response-time query | Query showed approximately 5 seconds and the response-time alert entered Firing |
| HTTP 500 | Call the server-error simulation endpoint | HTTP 500 alert fired and an email was received |
| Authentication failure | Call the authentication simulation endpoint | A 4xx metric was recorded and an alert email was reported received |
| Rate limit | Call the rate-limit simulation endpoint | The response status was verified as 429 and the dedicated alert email was received |
| Client-side timeout | Call the 30-second endpoint with a 5-second Requests timeout | Python raised `ReadTimeout` |

**Important:** The exact HTTP 401 response for the authentication simulation should be verified separately if it is required as evidence. Instrumentator metrics in this setup aggregate response codes into classes such as `4xx` and `5xx`. The Prometheus `up` metric checks scrape availability, not the body of the `/health` endpoint. A separate probe or application-specific metric is needed for direct health-response monitoring or dedicated client-timeout detection.

### API downtime test steps

1. Confirm FastAPI is running and `/health` responds successfully.
2. Keep Docker, Prometheus, and Grafana running.
3. Stop the Uvicorn process with `Ctrl + C`.
4. Open `http://localhost:9090/targets` and wait for the FastAPI target to show DOWN.
5. In Grafana, open **Alerting → Alert rules** and inspect `New Age FastAPI API Downtime`.
6. Capture screenshots of the Prometheus target and Grafana alert state. Capture the email notification if one arrives.
7. Restart FastAPI and confirm that `/health` responds again.
8. Wait for the alert to return to Normal and capture that recovery state if useful.

## Troubleshooting

| Issue | Checks |
|---|---|
| `docker compose up -d` fails | Confirm Docker Desktop is running and the command is executed in the folder containing `compose.yaml`. |
| FastAPI does not start | Activate `.venv`, install requirements, and inspect the terminal error. |
| Prometheus target is DOWN | Confirm Uvicorn is running on port 8000 and the target is `host.docker.internal:8000` in this local Docker setup. |
| Prometheus has no metrics | Open `/metrics` in the browser and inspect the Prometheus Targets page. |
| Grafana shows no data | Check the Prometheus data source URL (for this Compose network, typically `http://prometheus:9090`) and the query labels. |
| Alert remains Normal | Preview the query, verify the threshold and condition, check the evaluation interval and pending period, and inspect the alert's state history. |
| Email is not received | Test the Grafana contact point, check SMTP settings and logs, and look in spam/junk. Never share SMTP secrets. |
| Timeout command raises `ReadTimeout` | This is expected for the 30-second endpoint when the client timeout is 5 seconds. The server may continue processing after the client stops waiting. |

## Security Notes

- Never commit `.env`, Gmail App Passwords, API keys, passwords, or other secrets.
- Add `.env` and `.venv/` to `.gitignore`.
- Use placeholder values in `.env.example`.
- Change any default Grafana password before exposing the service beyond a local development environment.
- Do not expose Prometheus or Grafana publicly without appropriate access controls.
- The failure endpoints are for testing only. Do not deploy them to a public production service without access restrictions.

## Limitations and Future Improvements

- The application uses simulated endpoints rather than a production API.
- The `up` metric checks whether Prometheus can scrape the API, not whether `/health` returns the expected content.
- HTTP response metrics are grouped by class (`4xx`, `5xx`), so exact status-code reporting may require logs or custom metrics.
- A client-side timeout test does not automatically create a server-side timeout metric or a dedicated Grafana timeout alert.
- Additional improvements could include a dedicated health probe, custom metrics for exact error types, automated tests, dashboard provisioning, alert-rule provisioning, Slack notifications, and production-ready authentication and deployment settings.

## Evidence and Deliverables

For a complete submission, include:

- FastAPI source code (`main.py`)
- `requirements.txt`
- `compose.yaml` and `prometheus.yml`
- Exported Grafana dashboard JSON
- Screenshots of the dashboard, alert states, and email notifications
- Failure-testing results
- This README and any additional technical documentation

Only claim evidence that is actually captured and included in the repository.
