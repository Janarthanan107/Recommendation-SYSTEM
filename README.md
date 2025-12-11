# ML Service Recommendation System 🎯

An intelligent service recommendation engine that matches users with optimal services using **Machine Learning** techniques including feature engineering, similarity measurement, ranking algorithms, and explainable AI.

## 🎯 Project Overview

This system demonstrates industry-standard ML implementations used by e-commerce platforms, marketplaces, and service aggregators. It transforms structured data into actionable insights through preprocessing, modeling, scoring, and interactive UI development.

## ✨ Core ML Modules

1. **User Input Processing & Feature Encoding**
   - Converts user inputs (business type, budget, language, location) into ML-ready numerical vectors
   - Uses advanced encoding and feature mapping techniques

2. **Service Filtering & Ranking Engine**
   - Applies intelligent filtering based on user preferences
   - Uses ML techniques (Cosine Similarity / KNN) to rank services
   - Returns Top 3 most relevant services

3. **Similarity Score & Match Quality Generator**
   - Computes relevance scores using categorical and text similarity
   - Produces Match Score (0-1) and Match Quality (High/Medium/Low)

4. **Recommendation Explanation Generator**
   - Creates human-readable explanations for each recommendation
   - Based on service descriptions and feature match analysis

5. **Data Cleaning & Preprocessing Module**
   - Handles missing values and data quality issues
   - Standardizes categories and removes duplicates
   - Ensures ML-ready dataset

6. **Streamlit-Based Interactive UI**
   - User-friendly interface for input collection
   - Displays recommendations with scores, quality tags, and explanations
   - Real-time recommendation generation

7. **Evaluation & Optimization Layer**
   - Performance analysis and metrics
   - Weight optimization for ranking quality
   - Edge case handling

## 🏗️ Architecture

```
recommendation-system/
├── src/
│   ├── preprocessing/       # Data cleaning and preprocessing
│   ├── feature_engineering/ # Feature encoding and extraction
│   ├── models/             # ML models and algorithms
│   ├── recommendation/     # Core recommendation engine
│   ├── explainability/     # Explanation generation
│   └── utils/              # Helper functions
├── data/                   # Dataset storage
├── app.py                  # Streamlit application
├── config.py               # Configuration settings
└── requirements.txt        # Dependencies
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Dataset

The dataset will be automatically downloaded when you run the app for the first time.

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 Dataset Schema

| Column Name | Description |
|------------|-------------|
| Service_ID | Unique ID for each service |
| Service_Name | Human-readable service name |
| Target_Business_Type | Category of business the service supports |
| Price_Category | Cost category (Low/Medium/High) |
| Language_Support | Language options (Hindi/English/Both) |
| Location_Area | Service location or remote availability |
| Description | Short service overview |
| Match_Quality | Model-generated (High/Medium/Low) |

## 🧪 Features

- **Smart Filtering**: Initial filtering based on user preferences
- **ML-Powered Ranking**: Uses Cosine Similarity and KNN for relevance scoring
- **Explainable AI**: Clear explanations for why services are recommended
- **Interactive UI**: Beautiful Streamlit interface for seamless user experience
- **Real-time Recommendations**: Instant results as you input preferences
- **Quality Scoring**: Match quality indicators for each recommendation

## 🎓 ML Techniques Used

- Feature Engineering & Encoding
- Cosine Similarity
- K-Nearest Neighbors (KNN)
- Weighted Scoring Algorithms
- Text Similarity Measurement
- Multi-criteria Decision Making

## 📈 Performance

The system is optimized for:
- Fast recommendation generation (<1 second)
- High relevance accuracy
- Explainable results
- Scalability to large datasets

## 🛠️ Technology Stack

- **Python 3.8+**
- **Pandas & NumPy**: Data manipulation
- **Scikit-learn**: ML algorithms
- **Streamlit**: Interactive UI
- **Plotly**: Data visualization

## 📝 License

MIT License

## 👤 Author

Janarthanan

---

**Built with ❤️ using Machine Learning**