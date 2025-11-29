# IRIS Monitoring System

This project demonstrates how to monitor a Machine Learning service (Iris Classification) using **Prometheus** and **Grafana**.

## 🏗 Architecture

- **ML Service (FastAPI)**: Serves the Iris classification model and exposes metrics at `/metrics`.
- **Prometheus**: Scrapes metrics from the ML Service.
- **Grafana**: Visualizes the metrics through dashboards.

## 🚀 Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation & Running

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Start the services**:
    ```bash
    docker-compose up -d
    ```
    This command will build the images and start the containers for the ML service, Prometheus, and Grafana.

3.  **Access the services**:
    -   **ML API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
    -   **Prometheus UI**: [http://localhost:9090](http://localhost:9090)
    -   **Grafana UI**: [http://localhost:3000](http://localhost:3000)
        -   **Username**: `admin`
        -   **Password**: `admin` (You will be prompted to change it on first login)

## 🧪 Load Testing & Simulation

To see the monitoring in action, you need to generate some traffic. We have provided a script to simulate various scenarios (Normal traffic, High Load, Data Drift, Errors).

1.  **Run the load test script**:
    ```bash
    python scripts/load_test.py
    ```

2.  **Observe the logs**: The script will print the current scenario and the prediction results.

## 📊 Grafana Dashboard Setup

1.  **Login to Grafana** at [http://localhost:3000](http://localhost:3000).
2.  **Add Data Source**:
    -   Go to **Connections** -> **Data Sources**.
    -   Click **Add new data source**.
    -   Select **Prometheus**.
    -   Set the URL to `http://prometheus:9090`.
    -   Click **Save & Test**.
    *(Note: This might be pre-configured via `monitoring/grafana-datasources.yml`)*
3.  **Create Dashboard**:
    -   Go to **Dashboards** -> **New dashboard**.
    -   **Add visualization**.
    -   Select the **Prometheus** data source.
    -   Use the following PromQL queries to create panels:

    | Metric | PromQL Query |
    | :--- | :--- |
    | **Request Throughput (RPS)** | `sum(rate(inference_requests_total[1m])) by (status)` |
    | **Latency (P95)** | `histogram_quantile(0.95, sum(rate(inference_duration_seconds_bucket[5m])) by (le))` |
    | **Latency (Avg)** | `sum(rate(inference_duration_seconds_sum[5m])) / sum(rate(inference_duration_seconds_count[5m]))` |
    | **Error Rate (%)** | `sum(rate(inference_requests_total{status=~"5.."}[5m])) / sum(rate(inference_requests_total[5m])) * 100` |
    | **Prediction Distribution** | `sum(rate(prediction_output_total[1h])) by (class)` |

## 📂 Project Structure

```
.
├── docker-compose.yml      # Service orchestration
├── model
│   └── iris_model.py       # Model training script
├── monitoring
│   ├── grafana-datasources.yml # Grafana provisioning
│   └── prometheus.yml      # Prometheus config
├── server
│   ├── app.py              # FastAPI app with instrumentation
│   └── Dockerfile          # Server Dockerfile
└── scripts
    └── load_test.py        # Traffic simulator
```
