# 🚀 Quick Start Guide

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run System Test (Optional but Recommended)

```bash
python test_system.py
```

This will:
- Create a sample dataset with 50 services
- Test all ML modules
- Generate sample recommendations
- Verify the system is working correctly

### 3. Launch the Web Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
recommendation-system/
├── src/
│   ├── preprocessing/          # Module 5: Data Cleaning
│   │   └── data_cleaner.py
│   ├── feature_engineering/    # Module 1: Feature Encoding
│   │   └── encoder.py
│   ├── models/                 # Module 2 & 3: Ranking & Scoring
│   │   └── ranking_engine.py
│   ├── recommendation/         # Core Engine
│   │   └── engine.py
│   ├── explainability/         # Module 4: Explanations
│   │   └── explanation_generator.py
│   └── utils/                  # Helper Functions
│       └── helpers.py
├── data/                       # Dataset storage
├── app.py                      # Module 6: Streamlit UI
├── config.py                   # Configuration
├── test_system.py             # Testing script
└── requirements.txt           # Dependencies
```

## 🎯 Features

1. **ML-Powered Recommendations** - Uses Cosine Similarity, KNN, and Weighted Scoring
2. **Explainable AI** - Every recommendation comes with a clear explanation
3. **Interactive UI** - Beautiful Streamlit interface with visualizations
4. **Multiple Algorithms** - Choose between weighted, cosine, or KNN methods
5. **Real-time Processing** - Instant recommendations
6. **Data Validation** - Comprehensive preprocessing and cleaning

## 📊 Usage

### In the Web Interface:

1. Select your business type
2. Choose your budget range
3. Pick your language preference
4. Select your location
5. Click "Get Recommendations"
6. View personalized service recommendations with explanations

### Programmatically:

```python
from src.utils.helpers import load_dataset
from src.recommendation.engine import RecommendationEngine

# Load data
df = load_dataset('data/services_dataset.csv')

# Initialize engine
engine = RecommendationEngine(df)

# Get recommendations
user_input = {
    'Target_Business_Type': 'Technology',
    'Price_Category': 'Low',
    'Language_Support': 'Both',
    'Location_Area': 'Mumbai'
}

recommendations = engine.get_recommendations(user_input, top_n=3)
print(recommendations)
```

## 🔧 Configuration

Edit `config.py` to customize:
- Feature weights
- Match quality thresholds
- Number of recommendations
- UI colors and styling

## 📈 ML Techniques Used

- **Feature Engineering**: Label Encoding, Feature Vectorization
- **Similarity Measures**: Cosine Similarity, Euclidean Distance
- **Ranking Algorithms**: Weighted Scoring, KNN
- **Preprocessing**: Missing value handling, standardization, deduplication

## 🎓 Evaluation Metrics

The system tracks:
- Match Score (0-1)
- Match Quality (High/Medium/Low)
- Average recommendation accuracy
- Feature importance analysis

## 🐛 Troubleshooting

**Issue**: Dataset not found
**Solution**: Run `test_system.py` first to create a sample dataset

**Issue**: Import errors
**Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Streamlit won't start
**Solution**: Check if port 8501 is available, or use: `streamlit run app.py --server.port 8502`

## 📝 Notes

- The sample dataset contains 50 services across 5 business categories
- You can add your own dataset by placing a CSV file in the `data/` folder
- The system automatically cleans and preprocesses your data
- All recommendations include explanations based on feature matching

## 🎉 Enjoy!

Your ML Service Recommendation System is ready to use!
