"""
Configuration settings for the ML Service Recommendation System
"""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SRC_DIR = os.path.join(BASE_DIR, 'src')

# Dataset Configuration
DATASET_URL = "https://drive.google.com/drive/folders/1AeS9t8bCQpzCTCxfuQuXfqiJgSW8KzJy"
DATASET_FILE = os.path.join(DATA_DIR, 'services_dataset.csv')

# Feature Configuration
CATEGORICAL_FEATURES = [
    'Target_Business_Type',
    'Price_Category',
    'Language_Support',
    'Location_Area'
]

REQUIRED_COLUMNS = [
    'Service_ID',
    'Service_Name',
    'Target_Business_Type',
    'Price_Category',
    'Language_Support',
    'Location_Area',
    'Description'
]

# Business Type Options
BUSINESS_TYPES = [
    'Retail',
    'Restaurant',
    'Healthcare',
    'Education',
    'Technology',
    'Manufacturing',
    'Real Estate',
    'Hospitality',
    'Finance',
    'Consulting'
]

# Price Categories
PRICE_CATEGORIES = ['Low', 'Medium', 'High']

# Language Options
LANGUAGE_OPTIONS = ['Hindi', 'English', 'Both']

# Recommendation Configuration
TOP_N_RECOMMENDATIONS = 3
SIMILARITY_THRESHOLD = 0.3
MIN_MATCH_SCORE = 0.4

# Scoring Weights
WEIGHTS = {
    'business_type': 0.35,
    'price_category': 0.25,
    'language': 0.20,
    'location': 0.20
}

# Match Quality Thresholds
MATCH_QUALITY_THRESHOLDS = {
    'High': 0.75,
    'Medium': 0.50,
    'Low': 0.0
}

# UI Configuration
APP_TITLE = "🎯 ML Service Recommendation System"
APP_ICON = "🎯"
PAGE_CONFIG = {
    'page_title': 'Service Recommendations',
    'page_icon': '🎯',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Streamlit Theme Colors
COLORS = {
    'primary': '#FF6B6B',
    'secondary': '#4ECDC4',
    'success': '#95E1D3',
    'warning': '#F38181',
    'info': '#AA96DA'
}
