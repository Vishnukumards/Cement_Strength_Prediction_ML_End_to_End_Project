# monitoring/logger.py
import structlog
from datetime import datetime

logger = structlog.get_logger()

def log_prediction(input_data, prediction, latency):
    logger.info(
        "prediction_made",
        timestamp=datetime.utcnow().isoformat(),
        input_data=input_data,
        prediction=prediction,
        latency_ms=latency,
        model_version="1.0.0"
    )