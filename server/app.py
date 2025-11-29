import time
import logging
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app

try:
    from model.iris_model import predict
except ImportError:
    logging.warning("Could not import 'model.iris_model'. Using mock prediction for testing.")
    def predict(features):
        return int(features[0]) % 3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

REQUESTS_TOTAL = Counter(
    'inference_requests_total',
    'Total inference requests',
    ['method', 'endpoint', 'status']
)

DURATION_SECONDS = Histogram(
    'inference_duration_seconds',
    'Inference duration',
    ['method', 'endpoint'],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

PREDICTION_OUTPUT = Counter(
    'prediction_output_total',
    'Prediction class distribution',
    ['class'] # e.g., "0", "1", "2"
)

MODEL_LOADED = Gauge('model_loaded', 'Model load status')
MODEL_LOADED.set(1)

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    method = request.method
    path = request.url.path

    if path == "/metrics":
        return await call_next(request)

    start_time = time.time()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception as e:
        logger.error(f"Internal Server Error: {e}")
        raise e
    finally:
        process_time = time.time() - start_time
        REQUESTS_TOTAL.labels(
            method=method,
            endpoint=path,
            status=status_code
        ).inc()
        DURATION_SECONDS.labels(
            method=method,
            endpoint=path
        ).observe(process_time)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class FeaturesInput(BaseModel):
    features: list[float] # sepal_length, sepal_width, petal_length, petal_width

@app.post("/predict")
def inference(input: FeaturesInput):
    prediction = predict(input.features)
    PREDICTION_OUTPUT.labels(str(int(prediction))).inc()
    return {"prediction": int(prediction)}
