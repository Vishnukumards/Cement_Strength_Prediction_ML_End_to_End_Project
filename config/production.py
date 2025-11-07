class ProductionConfig:
    MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/best_model.pkl")
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    DEBUG = False
    
    # Simple CORS for development/testing
    CORS_ORIGINS = ["*"]  # Allow all origins for project phase
    
    # Or if you want to be slightly more secure:
    # CORS_ORIGINS = [
    #     "http://localhost:8501",
    #     "http://127.0.0.1:8501"
    # ]