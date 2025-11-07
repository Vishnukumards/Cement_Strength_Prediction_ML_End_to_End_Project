# monitoring/drift_detector.py
from scipy.stats import ks_2samp
import numpy as np

class DataDriftDetector:
    def detect_drift(self, training_dist, current_data, threshold=0.05):
        """Monitor feature distribution changes"""
        p_values = {}
        for feature in training_dist.keys():
            stat, p_value = ks_2samp(training_dist[feature], current_data[feature])
            p_values[feature] = p_value
        return p_values 