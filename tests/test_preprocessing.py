import sys
import os
import pandas as pd

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing import CementDataPreprocessor

def test_preprocessing():
    preprocessor = CementDataPreprocessor()
    
    # Test input matching notebook structure
    test_input = {
        "Cement (component 1)(kg in a m^3 mixture)": 540.0,
        "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": 0.0,
        "Fly Ash (component 3)(kg in a m^3 mixture)": 0.0,
        "Water  (component 4)(kg in a m^3 mixture)": 162.0,
        "Superplasticizer (component 5)(kg in a m^3 mixture)": 2.5,
        "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": 1040.0,
        "Fine Aggregate (component 7)(kg in a m^3 mixture)": 676.0,
        "Age (day)": 28
    }
    
    result = preprocessor.preprocess(test_input)
    
    # Check that engineered features are created
    assert 'total_binder' in result.columns
    assert 'water_binder_ratio' in result.columns
    assert 'aggregate_cement_ratio' in result.columns
    
    # Check calculations match notebook logic
    assert result['total_binder'].iloc[0] == 540.0  # cement + slag + fly_ash
    assert result['water_binder_ratio'].iloc[0] == 162.0 / 540.0