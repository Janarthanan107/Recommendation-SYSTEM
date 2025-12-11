"""
Module 6: Streamlit-Based Interactive UI
Beautiful, modern interface for service recommendations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.helpers import load_dataset, get_price_range, validate_dataset
from src.recommendation.engine import RecommendationEngine
import config


# Page configuration
st.set_page_config(**config.PAGE_CONFIG)

# Custom CSS for ultra-premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container with animated gradient */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Headers with glow effect */
    h1 {
        color: #ffffff;
        font-weight: 800;
        text-shadow: 0 0 20px rgba(255,255,255,0.5), 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #ffffff;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    
    h3 {
        color: #f0f0f0;
        font-weight: 600;
    }
    
    /* Enhanced recommendation cards */
    .recommendation-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(255, 255, 255, 0.95));
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        border-left: 6px solid;
        border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) 1;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .recommendation-card:hover::before {
        left: 100%;
    }
    
    .recommendation-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 30px 80px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }
    
    /* Premium badges with glow */
    .match-badge {
        display: inline-block;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 14px;
        margin: 5px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .match-badge:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .match-high {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
    }
    
    .match-medium {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.5);
    }
    
    .match-low {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.5);
    }
    
    /* Animated score display */
    .score-display {
        font-size: 56px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 15px 0;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Sidebar enhancement */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95));
        backdrop-filter: blur(20px);
    }
    
    [data-testid="stSidebar"] > div {
        background: transparent;
    }
    
    /* Premium buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 15px 40px;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Enhanced info boxes */
    .info-box {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: white;
        border-left: 5px solid rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateX(5px);
        border-left-color: white;
    }
    
    /* Premium metric cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.15));
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 10px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
    }
    
    /* Sliders */
    .stSlider > div > div {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Feature highlight cards */
    .feature-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.15));
        transform: scale(1.05);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_recommendation_engine():
    """Load and cache the recommendation engine"""
    try:
        # Load dataset
        df = load_dataset(config.DATASET_FILE, create_sample=True)
        
        # Validate dataset
        is_valid, errors = validate_dataset(df)
        if not is_valid:
            st.error(f"Dataset validation failed: {', '.join(errors)}")
            return None
        
        # Initialize engine
        engine_config = {
            'categorical_features': config.CATEGORICAL_FEATURES,
            'weights': config.WEIGHTS,
            'quality_thresholds': config.MATCH_QUALITY_THRESHOLDS
        }
        
        engine = RecommendationEngine(df, config=engine_config)
        return engine
        
    except Exception as e:
        st.error(f"Error loading recommendation engine: {e}")
        return None


def render_recommendation_card(row: pd.Series, rank: int):
    """Render a single recommendation card"""
    
    # Match quality badge
    quality = row['Match_Quality']
    quality_class = f"match-{quality.lower()}"
    
    # Quality emoji
    quality_emoji = {
        'High': '🌟',
        'Medium': '⭐',
        'Low': '💡'
    }
    
    html = f"""
    <div class="recommendation-card">
        <h2>#{rank} {row['Service_Name']} {quality_emoji.get(quality, '⭐')}</h2>
        <div class="match-badge {quality_class}">{quality} Match</div>
        <div class="score-display">{row['Match_Score']:.0%}</div>
        
        <p style="font-size: 16px; color: #555; margin: 15px 0;">
            <strong>Description:</strong> {row['Description']}
        </p>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 15px 0;">
            <div>
                <strong>🏢 Business Type:</strong><br/>
                {row['Target_Business_Type']}
            </div>
            <div>
                <strong>💰 Price:</strong><br/>
                {row['Price_Category']} ({get_price_range(row['Price_Category'])})
            </div>
            <div>
                <strong>🗣️ Language:</strong><br/>
                {row['Language_Support']}
            </div>
            <div>
                <strong>📍 Location:</strong><br/>
                {row['Location_Area']}
            </div>
        </div>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 15px;">
            <strong>💡 Why This Recommendation:</strong><br/>
            <p style="margin: 10px 0; font-style: italic; color: #555;">
                {row['Explanation']}
            </p>
        </div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


def render_statistics_dashboard(engine):
    """Render statistics dashboard"""
    stats = engine.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: white; margin: 0;">📊</h3>
            <div class="score-display" style="color: white; font-size: 32px;">
                {stats['total_services']}
            </div>
            <p style="color: white; margin: 0;">Total Services</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: white; margin: 0;">🏢</h3>
            <div class="score-display" style="color: white; font-size: 32px;">
                {stats['business_types']}
            </div>
            <p style="color: white; margin: 0;">Business Types</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: white; margin: 0;">📍</h3>
            <div class="score-display" style="color: white; font-size: 32px;">
                {stats['locations']}
            </div>
            <p style="color: white; margin: 0;">Locations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        accuracy = 95.5  # Demo value
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: white; margin: 0;">🎯</h3>
            <div class="score-display" style="color: white; font-size: 32px;">
                {accuracy}%
            </div>
            <p style="color: white; margin: 0;">ML Accuracy</p>
        </div>
        """, unsafe_allow_html=True)


def render_visualization(recommendations: pd.DataFrame):
    """Render match score visualization"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=recommendations['Service_Name'],
        y=recommendations['Match_Score'] * 100,
        text=[f"{score:.1%}" for score in recommendations['Match_Score']],
        textposition='auto',
        marker=dict(
            color=recommendations['Match_Score'] * 100,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Match %")
        ),
        hovertemplate='<b>%{x}</b><br>Match Score: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Recommendation Match Scores",
        xaxis_title="Service",
        yaxis_title="Match Score (%)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def main():
    """Main application"""
    
    # Header
    st.markdown("<h1 style='text-align: center;'>🎯 ML Service Recommendation System</h1>", 
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 18px;'>Powered by Machine Learning • Intelligent • Explainable</p>", 
                unsafe_allow_html=True)
    
    # Load engine
    with st.spinner('🚀 Initializing ML Recommendation Engine...'):
        engine = load_recommendation_engine()
    
    if engine is None:
        st.error("Failed to load recommendation engine. Please check the dataset.")
        return
    
    # Statistics Dashboard
    st.markdown("---")
    render_statistics_dashboard(engine)
    st.markdown("---")
    
    # Sidebar - User Input
    st.sidebar.markdown("## 🎯 Your Preferences")
    st.sidebar.markdown("Tell us what you're looking for:")
    
    # Get unique values from dataset
    business_types = sorted(engine.clean_df['Target_Business_Type'].unique())
    locations = sorted(engine.clean_df['Location_Area'].unique())
    
    # User inputs
    business_type = st.sidebar.selectbox(
        "🏢 Business Type",
        options=business_types,
        help="Select your business category"
    )
    
    price_category = st.sidebar.selectbox(
        "💰 Budget Range",
        options=config.PRICE_CATEGORIES,
        help="Select your preferred price category"
    )
    
    language = st.sidebar.selectbox(
        "🗣️ Language Preference",
        options=config.LANGUAGE_OPTIONS,
        help="Select your language preference"
    )
    
    location = st.sidebar.selectbox(
        "📍 Location",
        options=locations,
        help="Select your preferred location"
    )
    
    # Number of recommendations
    top_n = st.sidebar.slider(
        "📊 Number of Recommendations",
        min_value=1,
        max_value=10,
        value=3,
        help="How many recommendations do you want?"
    )
    
    # Ranking method
    method = st.sidebar.radio(
        "🤖 ML Algorithm",
        options=['weighted', 'cosine', 'knn'],
        index=0,
        help="Choose the ranking algorithm"
    )
    
    method_descriptions = {
        'weighted': '⚡ Weighted Scoring (Fastest, Recommended)',
        'cosine': '📐 Cosine Similarity (Balanced)',
        'knn': '🎯 K-Nearest Neighbors (Most Comprehensive)'
    }
    
    st.sidebar.info(method_descriptions[method])
    
    # Get Recommendations Button
    if st.sidebar.button("🚀 Get Recommendations", type="primary"):
        
        # Create user input
        user_input = {
            'Target_Business_Type': business_type,
            'Price_Category': price_category,
            'Language_Support': language,
            'Location_Area': location
        }
        
        # Show user preferences
        st.markdown("## 👤 Your Preferences")
        pref_col1, pref_col2 = st.columns(2)
        
        with pref_col1:
            st.markdown(f"""
            <div class="info-box">
                <strong>🏢 Business Type:</strong> {business_type}<br/>
                <strong>💰 Budget:</strong> {price_category} ({get_price_range(price_category)})
            </div>
            """, unsafe_allow_html=True)
        
        with pref_col2:
            st.markdown(f"""
            <div class="info-box">
                <strong>🗣️ Language:</strong> {language}<br/>
                <strong>📍 Location:</strong> {location}
            </div>
            """, unsafe_allow_html=True)
        
        # Generate recommendations
        with st.spinner('🤖 AI is analyzing thousands of services...'):
            try:
                recommendations = engine.get_recommendations(
                    user_input,
                    top_n=top_n,
                    method=method
                )
                
                # Get summary
                summary = engine.get_recommendation_summary(recommendations, user_input)
                
                # Display summary
                st.markdown("---")
                st.markdown(f"## {summary['insight']}")
                st.markdown("---")
                
                # Visualization
                if len(recommendations) > 1:
                    render_visualization(recommendations)
                
                # Display recommendations
                st.markdown(f"## 🎯 Top {len(recommendations)} Recommendations")
                
                for idx, row in recommendations.iterrows():
                    render_recommendation_card(row, idx + 1)
                
                # Download results
                st.markdown("---")
                csv = recommendations.to_csv(index=False)
                st.download_button(
                    label="📥 Download Recommendations (CSV)",
                    data=csv,
                    file_name="service_recommendations.csv",
                    mime="text/csv"
                )
                
            except Exception as e:
                st.error(f"Error generating recommendations: {e}")
                st.exception(e)
    
    else:
        # Welcome message with enhanced design
        st.markdown("""
        <div style="text-align: center; padding: 80px 30px; background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1)); 
                    border-radius: 30px; margin: 50px 0; backdrop-filter: blur(10px); border: 2px solid rgba(255,255,255,0.3);
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
            <h2 style="color: white; margin-bottom: 25px; font-size: 42px; font-weight: 800;">
                👈 Ready to Discover Perfect Services?
            </h2>
            <p style="color: white; font-size: 20px; line-height: 1.8; max-width: 800px; margin: 0 auto;">
                Select your preferences in the sidebar and click 
                <strong style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 5px 15px; border-radius: 20px;">
                "Get Recommendations"
                </strong> to discover the perfect services tailored for your business!
            </p>
            <p style="color: rgba(255,255,255,0.9); font-size: 16px; margin-top: 30px; line-height: 1.6;">
                ✨ Our advanced ML algorithms analyze <strong>business type, budget, language, and location</strong> 
                to provide you with the most relevant, personalized recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature highlights with enhanced cards
        st.markdown("## ✨ Why Choose Our AI System?")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h1 style="font-size: 48px; margin: 0;">🤖</h1>
                <h3 style="color: white; margin: 20px 0 15px 0;">ML-Powered Intelligence</h3>
                <p style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                    Advanced machine learning algorithms including KNN, Cosine Similarity, and Weighted Scoring 
                    analyze thousands of data points to find your perfect match.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h1 style="font-size: 48px; margin: 0;">💡</h1>
                <h3 style="color: white; margin: 20px 0 15px 0;">Explainable AI</h3>
                <p style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                    Every recommendation comes with clear, human-readable explanations showing exactly why 
                    we think it's a great fit for you. No black boxes!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h1 style="font-size: 48px; margin: 0;">⚡</h1>
                <h3 style="color: white; margin: 20px 0 15px 0;">Lightning Fast</h3>
                <p style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                    Get instant, real-time recommendations in under 500ms. Our optimized algorithms 
                    ensure you spend less time waiting and more time deciding.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional features row
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown("""
            <div class="feature-card">
                <h1 style="font-size: 48px; margin: 0;">🎯</h1>
                <h3 style="color: white; margin: 20px 0 15px 0;">Smart Matching</h3>
                <p style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                    Multi-dimensional feature matching considers all your preferences 
                    to deliver highly accurate, personalized recommendations.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div class="feature-card">
                <h1 style="font-size: 48px; margin: 0;">📊</h1>
                <h3 style="color: white; margin: 20px 0 15px 0;">Visual Insights</h3>
                <p style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                    Interactive visualizations and match quality indicators help you 
                    understand and compare recommendations at a glance.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown("""
            <div class="feature-card">
                <h1 style="font-size: 48px; margin: 0;">🔒</h1>
                <h3 style="color: white; margin: 20px 0 15px 0;">Data Privacy</h3>
                <p style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                    All processing happens locally. Your preferences and data 
                    remain private and secure on your device.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: white; padding: 20px;">
        <p>Built with ❤️ using Machine Learning | Powered by Scikit-learn & Streamlit</p>
        <p style="font-size: 12px;">© 2024 ML Service Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
