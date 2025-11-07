from setuptools import setup, find_packages

setup(
    name="cement_strength_predictor",
    version="1.0.0",
    description="ML pipeline for predicting concrete compressive strength",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "streamlit==1.28.0",
        "pandas==2.1.3",
        "numpy==1.24.3",
        "scikit-learn==1.3.2",
        "joblib==1.3.2",
        "pydantic==2.5.0",
        "plotly==5.17.0",
        "requests==2.31.0",
        "python-multipart==0.0.6"
    ],
    python_requires=">=3.8",
)