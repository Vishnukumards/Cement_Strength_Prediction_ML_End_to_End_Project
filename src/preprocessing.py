import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CementDataPreprocessor:
    """Faithfully replicates the preprocessing logic from the Jupyter notebook"""
    
    def __init__(self):
        self.feature_names = [
            'Cement (component 1)(kg in a m^3 mixture)',
            'Blast Furnace Slag (component 2)(kg in a m^3 mixture)',
            'Fly Ash (component 3)(kg in a m^3 mixture)',
            'Water  (component 4)(kg in a m^3 mixture)',
            'Superplasticizer (component 5)(kg in a m^3 mixture)',
            'Coarse Aggregate  (component 6)(kg in a m^3 mixture)',
            'Fine Aggregate (component 7)(kg in a m^3 mixture)',
            'Age (day)',
            'total_binder',
            'water_binder_ratio',
            'aggregate_cement_ratio'
        ]
    
    def preprocess(self, input_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Replicates exact preprocessing from notebook:
        1. Create DataFrame from input
        2. Feature engineering: total_binder, water_binder_ratio, aggregate_cement_ratio
        3. Handle any missing values (though notebook shows none)
        """
        try:
            # Create DataFrame (mirroring notebook's data structure)
            df = pd.DataFrame([input_data])
            
            # Feature engineering - EXACTLY as in notebook
            df['total_binder'] = (
                df['Cement (component 1)(kg in a m^3 mixture)'] +
                df['Blast Furnace Slag (component 2)(kg in a m^3 mixture)'] +
                df['Fly Ash (component 3)(kg in a m^3 mixture)']
            )
            
            df['water_binder_ratio'] = (
                df['Water  (component 4)(kg in a m^3 mixture)'] / df['total_binder']
            )
            
            df['aggregate_cement_ratio'] = (
                (df['Coarse Aggregate  (component 6)(kg in a m^3 mixture)'] +
                 df['Fine Aggregate (component 7)(kg in a m^3 mixture)']) /
                df['Cement (component 1)(kg in a m^3 mixture)']
            )
            
            # Handle infinite values from division (not in notebook but needed for production)
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            
            # Drop NaN values (mirroring notebook's data.dropna())
            df = df.dropna()
            
            # Ensure correct column order for model
            processed_data = df[self.feature_names]
            
            logger.info("Successfully preprocessed input data")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error in preprocessing: {str(e)}")
            raise ValueError(f"Data preprocessing failed: {str(e)}")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data types and ranges based on notebook EDA"""
        required_fields = [
            'Cement (component 1)(kg in a m^3 mixture)',
            'Blast Furnace Slag (component 2)(kg in a m^3 mixture)',
            'Fly Ash (component 3)(kg in a m^3 mixture)',
            'Water  (component 4)(kg in a m^3 mixture)',
            'Superplasticizer (component 5)(kg in a m^3 mixture)',
            'Coarse Aggregate  (component 6)(kg in a m^3 mixture)',
            'Fine Aggregate (component 7)(kg in a m^3 mixture)',
            'Age (day)'
        ]
        
        # Check all required fields are present
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"Missing required field: {field}")
            
            # Basic type validation
            if not isinstance(input_data[field], (int, float)):
                raise ValueError(f"Field {field} must be numeric")
        
        return True 