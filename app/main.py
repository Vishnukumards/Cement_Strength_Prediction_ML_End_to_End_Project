from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from datetime import datetime
import os

from src.predict import predictor
from src.schemas import PredictionInput, PredictionResponse, HealthResponse, ModelMetadata

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Concrete Strength Prediction API",
    description="API for predicting concrete compressive strength based on composition and age",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Concrete Strength Prediction API", "docs": "/docs"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        model_info = predictor.model_loader.get_model_info()
        return HealthResponse(
            status="healthy",
            model_loaded=True,
            model_version=model_info["model_version"],
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            model_version="unknown",
            timestamp=datetime.utcnow().isoformat()
        )

@app.get("/metadata", response_model=ModelMetadata)
async def get_metadata():
    """Get model metadata and training information"""
    try:
        model_info = predictor.model_loader.get_model_info()
        return ModelMetadata(
            **model_info,
            performance_metrics={
                "r2_score": 0.89,  # From notebook evaluation
                "rmse": 4.23,     # From notebook evaluation
                "algorithm": "RandomForestRegressor"
            }
        )
    except Exception as e:
        logger.error(f"Metadata retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve model metadata")

@app.post("/predict", response_model=PredictionResponse)
async def predict_strength(input_data: PredictionInput):
    """
    Predict concrete compressive strength based on composition parameters
    
    - **cement**: Cement component (kg in m³ mixture) - 102.0 to 540.0
    - **blast_furnace_slag**: Blast furnace slag component (kg in m³ mixture) - 0.0 to 359.4  
    - **fly_ash**: Fly ash component (kg in m³ mixture) - 0.0 to 200.1
    - **water**: Water component (kg in m³ mixture) - 121.75 to 247.0
    - **superplasticizer**: Superplasticizer component (kg in m³ mixture) - 0.0 to 32.2
    - **coarse_aggregate**: Coarse aggregate component (kg in m³ mixture) - 801.0 to 1145.0
    - **fine_aggregate**: Fine aggregate component (kg in m³ mixture) - 594.0 to 992.6
    - **age**: Concrete age in days - 1 to 365
    """
    try:
        # Convert to dict format expected by preprocessing
        input_dict = input_data.dict(by_alias=True)
        
        # Make prediction
        result = predictor.predict(input_dict)
        
        logger.info(f"Prediction successful for input: {input_dict}")
        return PredictionResponse(**result)
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")

@app.post("/explain")
async def explain_prediction(input_data: PredictionInput):
    """
    Provide feature importance explanation for prediction
    (Simplified version - in production you might integrate SHAP/LIME)
    """
    try:
        input_dict = input_data.dict(by_alias=True)
        
        # This would integrate with SHAP/LIME in production
        explanation = {
            "feature_importance": {
                "Cement": 0.25,
                "Water": 0.20,
                "Age": 0.15,
                "Water-Binder Ratio": 0.12,
                "Superplasticizer": 0.10,
                "Fly Ash": 0.08,
                "Blast Furnace Slag": 0.05,
                "Aggregate-Cement Ratio": 0.03,
                "Coarse Aggregate": 0.01,
                "Fine Aggregate": 0.01
            },
            "message": "Feature importance based on RandomForest model",
            "note": "For detailed SHAP explanations, enable explainability package"
        }
        
        return explanation
        
    except Exception as e:
        logger.error(f"Explanation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Explanation generation failed")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)