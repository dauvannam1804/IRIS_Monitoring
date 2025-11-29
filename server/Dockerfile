FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install fastapi uvicorn scikit-learn==1.5.2 joblib prometheus_client
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
