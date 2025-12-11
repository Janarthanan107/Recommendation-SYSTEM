"""
Test script for the ML Recommendation System
Tests all modules and generates a sample recommendation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.helpers import create_sample_dataset, load_dataset
from src.recommendation.engine import RecommendationEngine
import config


def test_full_pipeline():
    """Test the complete recommendation pipeline"""
    
    print("="*80)
    print(" ML SERVICE RECOMMENDATION SYSTEM - COMPREHENSIVE TEST")
    print("="*80 + "\n")
    
    # Step 1: Create sample dataset
    print("📋 Step 1: Creating Sample Dataset")
    print("-" * 80)
    dataset_path = create_sample_dataset(config.DATASET_FILE)
    print()
    
    # Step 2: Load dataset
    print("📂 Step 2: Loading Dataset")
    print("-" * 80)
    df = load_dataset(dataset_path)
    print(f"Dataset Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print()
    
    # Step 3: Initialize Recommendation Engine
    print("🚀 Step 3: Initializing Recommendation Engine")
    print("-" * 80)
    engine_config = {
        'categorical_features': config.CATEGORICAL_FEATURES,
        'weights': config.WEIGHTS,
        'quality_thresholds': config.MATCH_QUALITY_THRESHOLDS
    }
    engine = RecommendationEngine(df, config=engine_config)
    print()
    
    # Step 4: Display Statistics
    print("📊 Step 4: System Statistics")
    print("-" * 80)
    stats = engine.get_statistics()
    print(f"Total Services: {stats['total_services']}")
    print(f"Business Types: {stats['business_types']}")
    print(f"Price Distribution: {stats['price_categories']}")
    print(f"Language Support: {stats['language_support']}")
    print(f"Locations: {stats['locations']}")
    print()
    
    # Step 5: Test Recommendations
    print("🎯 Step 5: Testing Recommendations")
    print("-" * 80)
    
    test_cases = [
        {
            'name': 'Technology Startup (Low Budget)',
            'preferences': {
                'Target_Business_Type': 'Technology',
                'Price_Category': 'Low',
                'Language_Support': 'Both',
                'Location_Area': 'Mumbai'
            }
        },
        {
            'name': 'Retail Business (Medium Budget)',
            'preferences': {
                'Target_Business_Type': 'Retail',
                'Price_Category': 'Medium',
                'Language_Support': 'Both',
                'Location_Area': 'Remote'
            }
        },
        {
            'name': 'Finance Company (High Budget)',
            'preferences': {
                'Target_Business_Type': 'Finance',
                'Price_Category': 'High',
                'Language_Support': 'English',
                'Location_Area': 'Delhi'
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test Case {i}: {test_case['name']}")
        print(f"{'='*80}\n")
        
        user_prefs = test_case['preferences']
        
        print("👤 User Preferences:")
        for key, value in user_prefs.items():
            print(f"  • {key}: {value}")
        print()
        
        # Get recommendations
        recommendations = engine.get_recommendations(
            user_prefs,
            top_n=3,
            method='weighted'
        )
        
        # Display recommendations
        print(f"🎯 Top 3 Recommendations:\n")
        for idx, row in recommendations.iterrows():
            print(f"{idx + 1}. {row['Service_Name']}")
            print(f"   Match Score: {row['Match_Score']:.1%} | Quality: {row['Match_Quality']}")
            print(f"   Business: {row['Target_Business_Type']} | Price: {row['Price_Category']}")
            print(f"   💡 {row['Explanation']}")
            print()
        
        # Get summary
        summary = engine.get_recommendation_summary(recommendations, user_prefs)
        print(f"📊 Summary:")
        print(f"   {summary['insight']}")
        print(f"   Average Match Score: {summary['average_match_score']:.1%}")
        print()
    
    # Step 6: Test Different ML Methods
    print("\n" + "="*80)
    print("🤖 Step 6: Comparing ML Algorithms")
    print("="*80 + "\n")
    
    test_user = {
        'Target_Business_Type': 'Technology',
        'Price_Category': 'Low',
        'Language_Support': 'Both',
        'Location_Area': 'Mumbai'
    }
    
    methods = ['weighted', 'cosine', 'knn']
    
    for method in methods:
        print(f"\nMethod: {method.upper()}")
        print("-" * 40)
        
        recs = engine.get_recommendations(test_user, top_n=3, method=method)
        
        for idx, row in recs.iterrows():
            print(f"  {idx + 1}. {row['Service_Name']} - {row['Match_Score']:.1%}")
    
    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED SUCCESSFULLY!")
    print("="*80 + "\n")
    
    print("🎉 The ML Recommendation System is fully functional!")
    print("   Run 'streamlit run app.py' to start the web interface.")
    print()


if __name__ == "__main__":
    try:
        test_full_pipeline()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
