import joblib
import os
import logging
from typing import Any

logger = logging.getLogger(__name__)

class ModelLoader:
    """Load and manage the trained model with version handling"""
    
    def __init__(self, model_path: str = "models/best_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.model_version = "1.0.0"  # From notebook training
        self.load_model()
    
    def load_model(self):
        """Load the trained model with error handling"""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found at {self.model_path}")
            
            self.model = joblib.load(self.model_path)
            logger.info(f"Successfully loaded model from {self.model_path}")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def get_model_info(self) -> dict:
        """Get model metadata"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        return {
            "model_type": type(self.model).__name__,
            "model_version": self.model_version,
            "training_date": "2024-01-01",  # Would normally come from metadata
            "features_used": 11,  # 8 original + 3 engineered
            "target": "Concrete compressive strength(MPa, megapascals)"
        }
    
    def predict(self, features):
        """Make prediction using loaded model"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        try:
            prediction = self.model.predict(features)
            return prediction
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise