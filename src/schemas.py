from pydantic import BaseModel, Field, validator
from typing import Optional
import numpy as np

class PredictionInput(BaseModel):
    """Pydantic model for prediction input validation"""
    cement: float = Field(..., alias="Cement (component 1)(kg in a m^3 mixture)", ge=102.0, le=540.0)
    blast_furnace_slag: float = Field(..., alias="Blast Furnace Slag (component 2)(kg in a m^3 mixture)", ge=0.0, le=359.4)
    fly_ash: float = Field(..., alias="Fly Ash (component 3)(kg in a m^3 mixture)", ge=0.0, le=200.1)
    water: float = Field(..., alias="Water  (component 4)(kg in a m^3 mixture)", ge=121.75, le=247.0)
    superplasticizer: float = Field(..., alias="Superplasticizer (component 5)(kg in a m^3 mixture)", ge=0.0, le=32.2)
    coarse_aggregate: float = Field(..., alias="Coarse Aggregate  (component 6)(kg in a m^3 mixture)", ge=801.0, le=1145.0)
    fine_aggregate: float = Field(..., alias="Fine Aggregate (component 7)(kg in a m^3 mixture)", ge=594.0, le=992.6)
    age: int = Field(..., alias="Age (day)", ge=1, le=365)

    class Config:
        allow_population_by_field_name = True

    @validator('water', pre=True)
    def validate_water_binder_ratio(cls, v, values):
        """Validate that water-binder ratio is reasonable"""
        if 'cement' in values and 'blast_furnace_slag' in values and 'fly_ash' in values:
            total_binder = values['cement'] + values['blast_furnace_slag'] + values['fly_ash']
            if total_binder > 0:
                ratio = v / total_binder
                if ratio > 1.0:  # Based on notebook analysis
                    raise ValueError('Water-to-binder ratio seems unusually high')
        return v

class PredictionResponse(BaseModel):
    """Pydantic model for prediction response"""
    predicted_strength: float
    units: str
    model_version: str
    features_used: list[str]
    status: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_version: str
    timestamp: str

class ModelMetadata(BaseModel):
    """Model metadata response"""
    model_type: str
    model_version: str
    training_date: str
    features_used: int
    target: str
    performance_metrics: Optional[dict] = None