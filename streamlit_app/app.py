import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuration - UPDATED FOR PRODUCTION
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Cement Strength Predictor",
    page_icon="🏗️",
    layout="wide"
)

def initialize_session_state():
    """Initialize all session state variables"""
    default_values = {
        'cement': 300.0,
        'blast_slag': 0.0,
        'fly_ash': 0.0,
        'water': 180.0,
        'superplasticizer': 2.5,
        'coarse_agg': 1050.0,
        'fine_agg': 750.0,
        'age': 28,
        'last_prediction': None,
        'prediction_history': []
    }
    
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def validate_inputs(cement, water, age):
    """Validate user inputs and provide professional guidance"""
    warnings = []
    info = []
    
    # Water-cement ratio validation
    water_cement_ratio = water / cement if cement > 0 else 0
    if water_cement_ratio > 0.7:
        warnings.append("⚠️ High water-cement ratio may significantly reduce strength and durability")
    elif water_cement_ratio > 0.6:
        warnings.append("⚠️ Moderate water-cement ratio - consider reducing for higher strength")
    elif water_cement_ratio < 0.3:
        warnings.append("⚠️ Very low water-cement ratio may affect workability")
    else:
        info.append("✅ Optimal water-cement ratio range")
    
    # Age validation
    if age < 3:
        info.append("💡 Very early age testing - strength will develop significantly over time")
    elif age < 7:
        info.append("💡 Early age concrete typically reaches ~65% of 28-day strength")
    elif age < 28:
        info.append("💡 Concrete typically reaches ~90% of 28-day strength at 14 days")
    
    # Cement content validation
    if cement < 250:
        warnings.append("⚠️ Low cement content may result in lower strength and durability")
    elif cement > 500:
        info.append("💡 High cement content - consider supplementary cementitious materials")
    
    # Display all warnings and info
    for warning in warnings:
        st.warning(warning)
    for information in info:
        st.info(information)
    
    return len(warnings) == 0

def calculate_mix_ratios(cement, water, blast_slag, fly_ash, coarse_agg, fine_agg):
    """Calculate and return key mix design ratios"""
    water_cement_ratio = water / cement if cement > 0 else 0
    total_binder = cement + blast_slag + fly_ash
    total_aggregate = coarse_agg + fine_agg
    aggregate_binder_ratio = total_aggregate / total_binder if total_binder > 0 else 0
    fine_agg_ratio = fine_agg / total_aggregate if total_aggregate > 0 else 0
    
    return {
        'water_cement_ratio': water_cement_ratio,
        'total_binder': total_binder,
        'total_aggregate': total_aggregate,
        'aggregate_binder_ratio': aggregate_binder_ratio,
        'fine_agg_ratio': fine_agg_ratio
    }

def check_api_health():
    try:
        # UPDATED: Increased timeout for production
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            st.error(f"API Health Check Failed: Status {response.status_code}")
            return False, None
    except requests.exceptions.RequestException as e:
        st.error(f"API Connection Error: {str(e)}")
        st.info(f"Trying to connect to: {API_BASE_URL}")
        return False, None
    except Exception as e:
        st.error(f"Unexpected error during health check: {str(e)}")
        return False, None

def get_metadata():
    try:
        # UPDATED: Increased timeout for production
        response = requests.get(f"{API_BASE_URL}/metadata", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"Could not fetch metadata: Status {response.status_code}")
            return None
    except Exception as e:
        st.warning(f"Could not fetch metadata: {str(e)}")
        return None

def make_prediction(input_data):
    try:
        # UPDATED: Increased timeout for production
        response = requests.post(
            f"{API_BASE_URL}/predict", 
            json=input_data, 
            timeout=30,  # Increased timeout for Render
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = response.text
            st.error(f"Prediction failed with status {response.status_code}: {error_detail}")
            return None
    except requests.exceptions.Timeout:
        st.error("""
        ⏰ Prediction request timed out. 
        
        This can happen on free tier deployments when the service is waking up.
        Please try again in 30 seconds.
        """)
        return None
    except requests.exceptions.ConnectionError:
        st.error(f"""
        🔌 Cannot connect to the prediction server. 
        
        Please ensure the API is running at: {API_BASE_URL}
        
        If deploying on Render:
        - Check that both services are deployed
        - Verify the API_URL environment variable is set correctly
        - Wait for services to fully start (can take 1-2 minutes on free tier)
        """)
        return None
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")
        return None

def create_input_data_from_session():
    """Create input data dictionary from session state"""
    return {
        "Cement (component 1)(kg in a m^3 mixture)": st.session_state.cement,
        "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": st.session_state.blast_slag,
        "Fly Ash (component 3)(kg in a m^3 mixture)": st.session_state.fly_ash,
        "Water  (component 4)(kg in a m^3 mixture)": st.session_state.water,
        "Superplasticizer (component 5)(kg in a m^3 mixture)": st.session_state.superplasticizer,
        "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": st.session_state.coarse_agg,
        "Fine Aggregate (component 7)(kg in a m^3 mixture)": st.session_state.fine_agg,
        "Age (day)": st.session_state.age
    }

def load_scenario(scenario_data):
    """Load a test scenario into session state"""
    for key, value in scenario_data.items():
        if key in st.session_state:
            st.session_state[key] = value

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("🏗️ Cement Strength Predictor")
    st.markdown("Predict concrete compressive strength using machine learning")
    
    # Check API health with better loading state
    with st.spinner("🔍 Checking API connection..."):
        api_healthy, health_data = check_api_health()
    
    if not api_healthy:
        st.error("""
        ## 🚨 FastAPI Server Not Reachable!
        
        **If running locally:**
        ```bash
        uvicorn app.main:app --reload --port 8000
        ```
        
        **If deployed on Render:**
        - Check that both services are deployed
        - Verify API service is running
        - Wait 1-2 minutes for services to start
        - Check Render dashboard for deployment status
        
        **Current API URL:** `{}`
        """.format(API_BASE_URL))
        
        # Show current configuration
        with st.expander("🔧 Debug Information"):
            st.write(f"**API Base URL:** {API_BASE_URL}")
            st.write(f"**Environment:** {'Production' if API_BASE_URL != 'http://localhost:8000' else 'Local'}")
            st.write("**Troubleshooting Steps:**")
            st.write("1. Check if API service is running")
            st.write("2. Verify network connectivity")
            st.write("3. Check API service logs")
            st.write("4. Ensure CORS is properly configured")
        
        return
    
    # Show connection status
    if api_healthy:
        model_version = health_data.get('model_version', 'Unknown')
        st.success(f"✅ API Connected - Model Version: {model_version}")
        
        # Show deployment info
        if API_BASE_URL != "http://localhost:8000":
            st.info(f"🌐 **Production Deployment** - Connected to: {API_BASE_URL}")
    
    # Main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Concrete Mix Parameters")
        
        # Input form with clear organization
        with st.form("prediction_form"):
            st.subheader("Binder Materials")
            cement = st.number_input(
                "Cement (kg/m³)", 
                min_value=100.0, 
                max_value=600.0, 
                value=st.session_state.cement,
                key="cement_input"
            )
            blast_slag = st.number_input(
                "Blast Furnace Slag (kg/m³)", 
                min_value=0.0, 
                max_value=400.0, 
                value=st.session_state.blast_slag,
                key="blast_slag_input"
            )
            fly_ash = st.number_input(
                "Fly Ash (kg/m³)", 
                min_value=0.0, 
                max_value=200.0, 
                value=st.session_state.fly_ash,
                key="fly_ash_input"
            )
            
            st.subheader("Water & Additives")
            water = st.number_input(
                "Water (kg/m³)", 
                min_value=120.0, 
                max_value=250.0, 
                value=st.session_state.water,
                key="water_input"
            )
            superplasticizer = st.number_input(
                "Superplasticizer (kg/m³)", 
                min_value=0.0, 
                max_value=40.0, 
                value=st.session_state.superplasticizer,
                step=0.1,
                key="superplasticizer_input"
            )
            
            st.subheader("Aggregates & Age")
            coarse_agg = st.number_input(
                "Coarse Aggregate (kg/m³)", 
                min_value=800.0, 
                max_value=1300.0, 
                value=st.session_state.coarse_agg,
                key="coarse_agg_input"
            )
            fine_agg = st.number_input(
                "Fine Aggregate (kg/m³)", 
                min_value=600.0, 
                max_value=1000.0, 
                value=st.session_state.fine_agg,
                key="fine_agg_input"
            )
            age = st.number_input(
                "Age (days)", 
                min_value=1, 
                max_value=365, 
                value=st.session_state.age,
                key="age_input"
            )
            
            submitted = st.form_submit_button("Predict Compressive Strength", type="primary")
            
            # Update session state when form is submitted
            if submitted:
                st.session_state.cement = cement
                st.session_state.blast_slag = blast_slag
                st.session_state.fly_ash = fly_ash
                st.session_state.water = water
                st.session_state.superplasticizer = superplasticizer
                st.session_state.coarse_agg = coarse_agg
                st.session_state.fine_agg = fine_agg
                st.session_state.age = age
    
    with col2:
        st.header("Prediction Results")
        
        if submitted:
            # Input validation
            st.subheader("🔍 Input Validation")
            is_valid = validate_inputs(cement, water, age)
            
            with st.spinner("🤖 Making prediction... (This may take 30 seconds on first request)"):
                input_data = create_input_data_from_session()
                
                prediction_result = make_prediction(input_data)
                
                if prediction_result:
                    strength = prediction_result.get('predicted_strength', 0)
                    
                    # Store the prediction
                    st.session_state.last_prediction = {
                        'strength': strength,
                        'inputs': input_data,
                        'timestamp': pd.Timestamp.now()
                    }
                    
                    # Display result
                    st.subheader("📊 Strength Prediction")
                    st.metric(
                        label="Compressive Strength",
                        value=f"{strength:.1f} MPa"
                    )
                    
                    # Strength classification
                    st.subheader("🏷️ Classification")
                    if strength < 20:
                        st.error("**Very Low Strength Concrete** (C12/15)")
                        st.info("Suitable for non-structural applications")
                    elif strength < 25:
                        st.warning("**Low Strength Concrete** (C16/20)")
                        st.info("Suitable for foundations and mass concrete")
                    elif strength < 30:
                        st.info("**Moderate Strength Concrete** (C25/30)")
                        st.info("General purpose construction")
                    elif strength < 40:
                        st.success("**Standard Strength Concrete** (C30/37)")
                        st.info("Reinforced concrete structures")
                    elif strength < 50:
                        st.success("**High Strength Concrete** (C40/50)")
                        st.info("Pre-stressed concrete, high-rise buildings")
                    elif strength < 60:
                        st.success("**Very High Strength Concrete** (C50/60)")
                        st.info("Special structures, bridges")
                    else:
                        st.success("**Ultra High Strength Concrete** (C60/75+)")
                        st.info("Special applications, high-performance structures")
                    
                    # Mix ratio calculations
                    st.subheader("📐 Mix Design Ratios")
                    ratios = calculate_mix_ratios(cement, water, blast_slag, fly_ash, coarse_agg, fine_agg)
                    
                    col_ratio1, col_ratio2, col_ratio3 = st.columns(3)
                    
                    with col_ratio1:
                        wc_ratio = ratios['water_cement_ratio']
                        st.metric(
                            "Water-Cement Ratio", 
                            f"{wc_ratio:.2f}",
                            help="Lower ratios typically yield higher strength"
                        )
                        
                    with col_ratio2:
                        total_agg = ratios['total_aggregate']
                        st.metric(
                            "Total Aggregate", 
                            f"{total_agg:.0f} kg/m³",
                            help="Combined coarse and fine aggregate content"
                        )
                        
                    with col_ratio3:
                        binder_content = ratios['total_binder']
                        st.metric(
                            "Total Binder", 
                            f"{binder_content:.0f} kg/m³",
                            help="Cement + Slag + Fly Ash"
                        )
                    
                    # Additional ratios
                    col_ratio4, col_ratio5 = st.columns(2)
                    
                    with col_ratio4:
                        agg_binder_ratio = ratios['aggregate_binder_ratio']
                        st.metric(
                            "Aggregate-Binder Ratio",
                            f"{agg_binder_ratio:.1f}",
                            help="Total aggregate / total binder"
                        )
                    
                    with col_ratio5:
                        fine_agg_ratio = ratios['fine_agg_ratio']
                        st.metric(
                            "Fine Aggregate Ratio",
                            f"{fine_agg_ratio:.2f}",
                            help="Fine aggregate / total aggregate"
                        )
    
    # Test scenarios
    st.markdown("---")
    st.header("🚀 Quick Test Scenarios")
    
    scenarios = {
        "High-Strength": {
            "cement": 450.0, 
            "blast_slag": 100.0, 
            "fly_ash": 50.0, 
            "water": 150.0,
            "superplasticizer": 3.0, 
            "coarse_agg": 1000.0, 
            "fine_agg": 700.0, 
            "age": 28
        },
        "Standard": {
            "cement": 300.0, 
            "blast_slag": 50.0, 
            "fly_ash": 30.0, 
            "water": 180.0,
            "superplasticizer": 1.0, 
            "coarse_agg": 1100.0, 
            "fine_agg": 750.0, 
            "age": 28
        },
        "Early Strength": {
            "cement": 400.0, 
            "blast_slag": 0.0, 
            "fly_ash": 0.0, 
            "water": 170.0,
            "superplasticizer": 2.0, 
            "coarse_agg": 1050.0, 
            "fine_agg": 680.0, 
            "age": 7
        }
    }
    
    cols = st.columns(3)
    for idx, (name, data) in enumerate(scenarios.items()):
        with cols[idx]:
            if st.button(f"Load {name} Scenario", use_container_width=True, key=f"scenario_{idx}"):
                load_scenario(data)
                st.success(f"{name} scenario loaded!")
                st.rerun()

    # Sidebar with enhanced information
    with st.sidebar:
        st.header("🏭 Model Information")
        metadata = get_metadata()
        if metadata:
            st.write(f"**Model Type:** {metadata.get('model_type', 'XGBRegressor')}")
            st.write(f"**Version:** {metadata.get('model_version', '1.0.0')}")
            st.write(f"**Features:** {metadata.get('features_used', 8)}")
            
            if 'performance_metrics' in metadata:
                st.subheader("📈 Performance Metrics")
                metrics = metadata['performance_metrics']
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("R² Score", f"{metrics.get('r2_score', 0.89):.3f}")
                with col_metric2:
                    st.metric("RMSE", f"{metrics.get('rmse', 4.23):.2f} MPa")
        
        # Deployment information
        st.header("🌐 Deployment Info")
        st.write(f"**API URL:** {API_BASE_URL}")
        st.write(f"**Environment:** {'Production' if API_BASE_URL != 'http://localhost:8000' else 'Local'}")
        
        # Professional guidance
        st.header("💡 Professional Guidance")
        with st.expander("Water-Cement Ratio"):
            st.write("""
            **Recommended ranges:**
            - **0.35-0.40**: High strength concrete
            - **0.40-0.50**: Standard concrete
            - **0.50-0.60**: Mass concrete
            - **>0.60**: Low strength applications
            """)
        
        with st.expander("Strength Classes"):
            st.write("""
            **Concrete strength classes (MPa):**
            - **C12/15**: 12-15 MPa (Non-structural)
            - **C25/30**: 25-30 MPa (General purpose)
            - **C30/37**: 30-37 MPa (Reinforced structures)
            - **C40/50**: 40-50 MPa (High-rise buildings)
            - **C50/60+**: 50+ MPa (Special structures)
            """)
        
        # Debug section
        st.header("🔧 Debug Information")
        if st.checkbox("Show Session State"):
            st.write(st.session_state)
        
        if st.checkbox("Show Input Data"):
            input_data = create_input_data_from_session()
            st.json(input_data)
        
        if st.checkbox("Show API Configuration"):
            st.write(f"**API Base URL:** {API_BASE_URL}")
            st.write(f"**Environment Variable API_URL:** {os.getenv('API_URL', 'Not set')}")

if __name__ == "__main__":
    main()
    
## Local -- 


# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# # Configuration
# API_BASE_URL = "http://localhost:8000"

# # Page configuration
# st.set_page_config(
#     page_title="Cement Strength Predictor",
#     page_icon="🏗️",
#     layout="wide"
# )

# def initialize_session_state():
#     """Initialize all session state variables"""
#     default_values = {
#         'cement': 300.0,
#         'blast_slag': 0.0,
#         'fly_ash': 0.0,
#         'water': 180.0,
#         'superplasticizer': 2.5,
#         'coarse_agg': 1050.0,
#         'fine_agg': 750.0,
#         'age': 28,
#         'last_prediction': None,
#         'prediction_history': []
#     }
    
#     for key, value in default_values.items():
#         if key not in st.session_state:
#             st.session_state[key] = value

# def validate_inputs(cement, water, age):
#     """Validate user inputs and provide professional guidance"""
#     warnings = []
#     info = []
    
#     # Water-cement ratio validation
#     water_cement_ratio = water / cement if cement > 0 else 0
#     if water_cement_ratio > 0.7:
#         warnings.append("⚠️ High water-cement ratio may significantly reduce strength and durability")
#     elif water_cement_ratio > 0.6:
#         warnings.append("⚠️ Moderate water-cement ratio - consider reducing for higher strength")
#     elif water_cement_ratio < 0.3:
#         warnings.append("⚠️ Very low water-cement ratio may affect workability")
#     else:
#         info.append("✅ Optimal water-cement ratio range")
    
#     # Age validation
#     if age < 3:
#         info.append("💡 Very early age testing - strength will develop significantly over time")
#     elif age < 7:
#         info.append("💡 Early age concrete typically reaches ~65% of 28-day strength")
#     elif age < 28:
#         info.append("💡 Concrete typically reaches ~90% of 28-day strength at 14 days")
    
#     # Cement content validation
#     if cement < 250:
#         warnings.append("⚠️ Low cement content may result in lower strength and durability")
#     elif cement > 500:
#         info.append("💡 High cement content - consider supplementary cementitious materials")
    
#     # Display all warnings and info
#     for warning in warnings:
#         st.warning(warning)
#     for information in info:
#         st.info(information)
    
#     return len(warnings) == 0

# def calculate_mix_ratios(cement, water, blast_slag, fly_ash, coarse_agg, fine_agg):
#     """Calculate and return key mix design ratios"""
#     water_cement_ratio = water / cement if cement > 0 else 0
#     total_binder = cement + blast_slag + fly_ash
#     total_aggregate = coarse_agg + fine_agg
#     aggregate_binder_ratio = total_aggregate / total_binder if total_binder > 0 else 0
#     fine_agg_ratio = fine_agg / total_aggregate if total_aggregate > 0 else 0
    
#     return {
#         'water_cement_ratio': water_cement_ratio,
#         'total_binder': total_binder,
#         'total_aggregate': total_aggregate,
#         'aggregate_binder_ratio': aggregate_binder_ratio,
#         'fine_agg_ratio': fine_agg_ratio
#     }

# def check_api_health():
#     try:
#         response = requests.get(f"{API_BASE_URL}/health", timeout=5)
#         if response.status_code == 200:
#             return True, response.json()
#         else:
#             st.error(f"API Health Check Failed: Status {response.status_code}")
#             return False, None
#     except requests.exceptions.RequestException as e:
#         st.error(f"API Connection Error: {str(e)}")
#         return False, None
#     except Exception as e:
#         st.error(f"Unexpected error during health check: {str(e)}")
#         return False, None

# def get_metadata():
#     try:
#         response = requests.get(f"{API_BASE_URL}/metadata", timeout=5)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             st.warning(f"Could not fetch metadata: Status {response.status_code}")
#             return None
#     except:
#         return None

# def make_prediction(input_data):
#     try:
#         response = requests.post(
#             f"{API_BASE_URL}/predict", 
#             json=input_data, 
#             timeout=10,
#             headers={'Content-Type': 'application/json'}
#         )
        
#         if response.status_code == 200:
#             return response.json()
#         else:
#             error_detail = response.text
#             st.error(f"Prediction failed with status {response.status_code}: {error_detail}")
#             return None
#     except requests.exceptions.Timeout:
#         st.error("Prediction request timed out. Please try again.")
#         return None
#     except requests.exceptions.ConnectionError:
#         st.error("Cannot connect to the prediction server. Please ensure the API is running.")
#         return None
#     except Exception as e:
#         st.error(f"Prediction failed: {str(e)}")
#         return None

# def create_input_data_from_session():
#     """Create input data dictionary from session state"""
#     return {
#         "Cement (component 1)(kg in a m^3 mixture)": st.session_state.cement,
#         "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": st.session_state.blast_slag,
#         "Fly Ash (component 3)(kg in a m^3 mixture)": st.session_state.fly_ash,
#         "Water  (component 4)(kg in a m^3 mixture)": st.session_state.water,
#         "Superplasticizer (component 5)(kg in a m^3 mixture)": st.session_state.superplasticizer,
#         "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": st.session_state.coarse_agg,
#         "Fine Aggregate (component 7)(kg in a m^3 mixture)": st.session_state.fine_agg,
#         "Age (day)": st.session_state.age
#     }

# def load_scenario(scenario_data):
#     """Load a test scenario into session state"""
#     for key, value in scenario_data.items():
#         if key in st.session_state:
#             st.session_state[key] = value

# def main():
#     # Initialize session state
#     initialize_session_state()
    
#     # Header
#     st.title("🏗️ Cement Strength Predictor")
#     st.markdown("Predict concrete compressive strength using machine learning")
    
#     # Check API health
#     with st.spinner("Checking API connection..."):
#         api_healthy, health_data = check_api_health()
    
#     if not api_healthy:
#         st.error("""
#         **FastAPI Server Not Running!**
        
#         Please start your FastAPI server first:
#         ```bash
#         uvicorn app.main:app --reload --port 8000
#         ```
        
#         Make sure:
#         1. Your FastAPI server is running on port 8000
#         2. The endpoint paths match (/health, /predict, /metadata)
#         3. CORS is properly configured on the server
#         """)
#         return
    
#     st.success(f"✅ API Connected - Model Version: {health_data.get('model_version', 'Unknown')}")
    
#     # Main layout
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.header("Concrete Mix Parameters")
        
#         # Input form with clear organization
#         with st.form("prediction_form"):
#             st.subheader("Binder Materials")
#             cement = st.number_input(
#                 "Cement (kg/m³)", 
#                 min_value=100.0, 
#                 max_value=600.0, 
#                 value=st.session_state.cement,
#                 key="cement_input"
#             )
#             blast_slag = st.number_input(
#                 "Blast Furnace Slag (kg/m³)", 
#                 min_value=0.0, 
#                 max_value=400.0, 
#                 value=st.session_state.blast_slag,
#                 key="blast_slag_input"
#             )
#             fly_ash = st.number_input(
#                 "Fly Ash (kg/m³)", 
#                 min_value=0.0, 
#                 max_value=200.0, 
#                 value=st.session_state.fly_ash,
#                 key="fly_ash_input"
#             )
            
#             st.subheader("Water & Additives")
#             water = st.number_input(
#                 "Water (kg/m³)", 
#                 min_value=120.0, 
#                 max_value=250.0, 
#                 value=st.session_state.water,
#                 key="water_input"
#             )
#             superplasticizer = st.number_input(
#                 "Superplasticizer (kg/m³)", 
#                 min_value=0.0, 
#                 max_value=40.0, 
#                 value=st.session_state.superplasticizer,
#                 step=0.1,
#                 key="superplasticizer_input"
#             )
            
#             st.subheader("Aggregates & Age")
#             coarse_agg = st.number_input(
#                 "Coarse Aggregate (kg/m³)", 
#                 min_value=800.0, 
#                 max_value=1300.0, 
#                 value=st.session_state.coarse_agg,
#                 key="coarse_agg_input"
#             )
#             fine_agg = st.number_input(
#                 "Fine Aggregate (kg/m³)", 
#                 min_value=600.0, 
#                 max_value=1000.0, 
#                 value=st.session_state.fine_agg,
#                 key="fine_agg_input"
#             )
#             age = st.number_input(
#                 "Age (days)", 
#                 min_value=1, 
#                 max_value=365, 
#                 value=st.session_state.age,
#                 key="age_input"
#             )
            
#             submitted = st.form_submit_button("Predict Compressive Strength", type="primary")
            
#             # Update session state when form is submitted
#             if submitted:
#                 st.session_state.cement = cement
#                 st.session_state.blast_slag = blast_slag
#                 st.session_state.fly_ash = fly_ash
#                 st.session_state.water = water
#                 st.session_state.superplasticizer = superplasticizer
#                 st.session_state.coarse_agg = coarse_agg
#                 st.session_state.fine_agg = fine_agg
#                 st.session_state.age = age
    
#     with col2:
#         st.header("Prediction Results")
        
#         if submitted:
#             # Input validation
#             st.subheader("🔍 Input Validation")
#             is_valid = validate_inputs(cement, water, age)
            
#             with st.spinner("Making prediction..."):
#                 input_data = create_input_data_from_session()
                
#                 prediction_result = make_prediction(input_data)
                
#                 if prediction_result:
#                     strength = prediction_result.get('predicted_strength', 0)
                    
#                     # Store the prediction
#                     st.session_state.last_prediction = {
#                         'strength': strength,
#                         'inputs': input_data,
#                         'timestamp': pd.Timestamp.now()
#                     }
                    
#                     # Display result
#                     st.subheader("📊 Strength Prediction")
#                     st.metric(
#                         label="Compressive Strength",
#                         value=f"{strength:.1f} MPa"
#                     )
                    
#                     # Strength classification
#                     st.subheader("🏷️ Classification")
#                     if strength < 20:
#                         st.error("**Very Low Strength Concrete** (C12/15)")
#                         st.info("Suitable for non-structural applications")
#                     elif strength < 25:
#                         st.warning("**Low Strength Concrete** (C16/20)")
#                         st.info("Suitable for foundations and mass concrete")
#                     elif strength < 30:
#                         st.info("**Moderate Strength Concrete** (C25/30)")
#                         st.info("General purpose construction")
#                     elif strength < 40:
#                         st.success("**Standard Strength Concrete** (C30/37)")
#                         st.info("Reinforced concrete structures")
#                     elif strength < 50:
#                         st.success("**High Strength Concrete** (C40/50)")
#                         st.info("Pre-stressed concrete, high-rise buildings")
#                     elif strength < 60:
#                         st.success("**Very High Strength Concrete** (C50/60)")
#                         st.info("Special structures, bridges")
#                     else:
#                         st.success("**Ultra High Strength Concrete** (C60/75+)")
#                         st.info("Special applications, high-performance structures")
                    
#                     # Mix ratio calculations
#                     st.subheader("📐 Mix Design Ratios")
#                     ratios = calculate_mix_ratios(cement, water, blast_slag, fly_ash, coarse_agg, fine_agg)
                    
#                     col_ratio1, col_ratio2, col_ratio3 = st.columns(3)
                    
#                     with col_ratio1:
#                         wc_ratio = ratios['water_cement_ratio']
#                         st.metric(
#                             "Water-Cement Ratio", 
#                             f"{wc_ratio:.2f}",
#                             help="Lower ratios typically yield higher strength"
#                         )
                        
#                     with col_ratio2:
#                         total_agg = ratios['total_aggregate']
#                         st.metric(
#                             "Total Aggregate", 
#                             f"{total_agg:.0f} kg/m³",
#                             help="Combined coarse and fine aggregate content"
#                         )
                        
#                     with col_ratio3:
#                         binder_content = ratios['total_binder']
#                         st.metric(
#                             "Total Binder", 
#                             f"{binder_content:.0f} kg/m³",
#                             help="Cement + Slag + Fly Ash"
#                         )
                    
#                     # Additional ratios
#                     col_ratio4, col_ratio5 = st.columns(2)
                    
#                     with col_ratio4:
#                         agg_binder_ratio = ratios['aggregate_binder_ratio']
#                         st.metric(
#                             "Aggregate-Binder Ratio",
#                             f"{agg_binder_ratio:.1f}",
#                             help="Total aggregate / total binder"
#                         )
                    
#                     with col_ratio5:
#                         fine_agg_ratio = ratios['fine_agg_ratio']
#                         st.metric(
#                             "Fine Aggregate Ratio",
#                             f"{fine_agg_ratio:.2f}",
#                             help="Fine aggregate / total aggregate"
#                         )
                    
#                     # Show confidence if available
#                     if 'confidence' in prediction_result:
#                         st.subheader("🎯 Prediction Confidence")
#                         confidence = prediction_result['confidence']
#                         st.progress(confidence / 100)
#                         st.write(f"Model confidence: {confidence:.1f}%")
    
#     # Test scenarios
#     st.markdown("---")
#     st.header("Quick Test Scenarios")
    
#     scenarios = {
#         "High-Strength": {
#             "cement": 450.0, 
#             "blast_slag": 100.0, 
#             "fly_ash": 50.0, 
#             "water": 150.0,
#             "superplasticizer": 3.0, 
#             "coarse_agg": 1000.0, 
#             "fine_agg": 700.0, 
#             "age": 28
#         },
#         "Standard": {
#             "cement": 300.0, 
#             "blast_slag": 50.0, 
#             "fly_ash": 30.0, 
#             "water": 180.0,
#             "superplasticizer": 1.0, 
#             "coarse_agg": 1100.0, 
#             "fine_agg": 750.0, 
#             "age": 28
#         },
#         "Early Strength": {
#             "cement": 400.0, 
#             "blast_slag": 0.0, 
#             "fly_ash": 0.0, 
#             "water": 170.0,
#             "superplasticizer": 2.0, 
#             "coarse_agg": 1050.0, 
#             "fine_agg": 680.0, 
#             "age": 7
#         }
#     }
    
#     cols = st.columns(3)
#     for idx, (name, data) in enumerate(scenarios.items()):
#         with cols[idx]:
#             if st.button(f"Load {name} Scenario", use_container_width=True, key=f"scenario_{idx}"):
#                 load_scenario(data)
#                 st.success(f"{name} scenario loaded!")
#                 st.rerun()

#     # Sidebar with enhanced information
#     with st.sidebar:
#         st.header("🏭 Model Information")
#         metadata = get_metadata()
#         if metadata:
#             st.write(f"**Model Type:** {metadata.get('model_type', 'XGBRegressor')}")
#             st.write(f"**Version:** {metadata.get('model_version', '1.0.0')}")
#             st.write(f"**Features:** {metadata.get('features_used', 8)}")
            
#             if 'performance_metrics' in metadata:
#                 st.subheader("📈 Performance Metrics")
#                 metrics = metadata['performance_metrics']
#                 col_metric1, col_metric2 = st.columns(2)
#                 with col_metric1:
#                     st.metric("R² Score", f"{metrics.get('r2_score', 0.89):.3f}")
#                 with col_metric2:
#                     st.metric("RMSE", f"{metrics.get('rmse', 4.23):.2f} MPa")
        
#         # Professional guidance
#         st.header("💡 Professional Guidance")
#         with st.expander("Water-Cement Ratio"):
#             st.write("""
#             **Recommended ranges:**
#             - **0.35-0.40**: High strength concrete
#             - **0.40-0.50**: Standard concrete
#             - **0.50-0.60**: Mass concrete
#             - **>0.60**: Low strength applications
#             """)
        
#         with st.expander("Strength Classes"):
#             st.write("""
#             **Concrete strength classes (MPa):**
#             - **C12/15**: 12-15 MPa (Non-structural)
#             - **C25/30**: 25-30 MPa (General purpose)
#             - **C30/37**: 30-37 MPa (Reinforced structures)
#             - **C40/50**: 40-50 MPa (High-rise buildings)
#             - **C50/60+**: 50+ MPa (Special structures)
#             """)
        
#         # Debug section
#         st.header("🔧 Debug Information")
#         if st.checkbox("Show Session State"):
#             st.write(st.session_state)
        
#         if st.checkbox("Show Input Data"):
#             input_data = create_input_data_from_session()
#             st.json(input_data)

# if __name__ == "__main__":
#     main() 