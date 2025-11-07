import logging
from typing import Dict, Any, Tuple
import pandas as pd

from .preprocessing import CementDataPreprocessor
from .model_loader import ModelLoader

logger = logging.getLogger(__name__)

class CementStrengthPredictor:
    """Main prediction class that orchestrates preprocessing and prediction"""
    
    def __init__(self, model_path: str = "models/best_model.pkl"):
        self.preprocessor = CementDataPreprocessor()
        self.model_loader = ModelLoader(model_path)
    
    def predict(self, input_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        Complete prediction pipeline:
        1. Validate input
        2. Preprocess (exactly like notebook)
        3. Predict
        4. Return results with metadata
        """
        try:
            # Validate input
            self.preprocessor.validate_input(input_data)
            
            # Preprocess (faithfully replicates notebook)
            processed_features = self.preprocessor.preprocess(input_data)
            
            # Make prediction
            prediction = self.model_loader.predict(processed_features)
            
            # Prepare response
            result = {
                "predicted_strength": float(prediction[0]),
                "units": "MPa",
                "model_version": self.model_loader.model_version,
                "features_used": list(processed_features.columns),
                "status": "success"
            }
            
            logger.info(f"Prediction successful: {result['predicted_strength']} MPa")
            return result
            
        except Exception as e:
            logger.error(f"Prediction pipeline failed: {str(e)}")
            raise

# Singleton instance
predictor = CementStrengthPredictor()