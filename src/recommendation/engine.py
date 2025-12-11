"""
Core Recommendation Engine
Integrates all modules to provide end-to-end recommendations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from preprocessing.data_cleaner import DataPreprocessor
from feature_engineering.encoder import FeatureEncoder, UserInputProcessor
from models.ranking_engine import ServiceRankingEngine, MatchQualityGenerator
from explainability.explanation_generator import ExplanationGenerator


class RecommendationEngine:
    """Main recommendation engine integrating all ML modules"""
    
    def __init__(self, services_df: pd.DataFrame, config: Dict = None):
        """
        Initialize the recommendation engine
        
        Args:
            services_df: DataFrame with service data
            config: Configuration dictionary
        """
        self.config = config or {}
        self.original_df = services_df.copy()
        
        # Initialize modules
        print("🚀 Initializing ML Recommendation Engine...\n")
        
        # Module 5: Data Preprocessing
        self.preprocessor = DataPreprocessor(services_df)
        self.clean_df = self.preprocessor.clean_dataset()
        
        # Module 1: Feature Encoding
        self.encoder = FeatureEncoder()
        categorical_features = self.config.get('categorical_features', [
            'Target_Business_Type',
            'Price_Category',
            'Language_Support',
            'Location_Area'
        ])
        self.encoded_df = self.encoder.fit_transform(self.clean_df, categorical_features)
        
        # Module 1: User Input Processing
        self.input_processor = UserInputProcessor(self.encoder)
        
        # Module 2 & 3: Ranking and Match Quality
        weights = self.config.get('weights', {
            'Target_Business_Type': 0.35,
            'Price_Category': 0.25,
            'Language_Support': 0.20,
            'Location_Area': 0.20
        })
        self.ranking_engine = ServiceRankingEngine(self.encoded_df, weights)
        self.ranking_engine.build_feature_matrix()
        self.ranking_engine.train_knn_model()
        
        # Module 3: Match Quality
        thresholds = self.config.get('quality_thresholds', {
            'High': 0.75,
            'Medium': 0.50,
            'Low': 0.0
        })
        self.quality_generator = MatchQualityGenerator(thresholds)
        
        # Module 4: Explanations
        self.explainer = ExplanationGenerator()
        
        print("✅ Recommendation Engine Ready!\n")
    
    def get_recommendations(
        self,
        user_input: Dict[str, str],
        top_n: int = 3,
        method: str = 'weighted'
    ) -> pd.DataFrame:
        """
        Get personalized service recommendations
        
        Args:
            user_input: User preferences dictionary
            top_n: Number of recommendations to return
            method: Ranking method ('weighted', 'cosine', 'knn')
            
        Returns:
            DataFrame with recommendations, scores, and explanations
        """
        print(f"🔍 Generating recommendations for user preferences...")
        
        # Step 1: Process user input
        try:
            processed = self.input_processor.process_input(user_input)
            user_vector = processed['feature_vector']
        except ValueError as e:
            raise ValueError(f"Invalid user input: {e}")
        
        # Step 2: Rank services
        ranked_services = self.ranking_engine.rank_services(
            user_input,
            user_vector,
            top_n=top_n,
            method=method
        )
        
        # Step 3: Generate match scores and quality
        recommendations = self.quality_generator.generate_quality_metrics(
            ranked_services,
            user_input
        )
        
        # Step 4: Generate explanations
        recommendations = self.explainer.generate_batch_explanations(
            user_input,
            recommendations
        )
        
        # Step 5: Format results
        result_columns = [
            'Service_ID',
            'Service_Name',
            'Target_Business_Type',
            'Price_Category',
            'Language_Support',
            'Location_Area',
            'Description',
            'Match_Score',
            'Match_Quality',
            'Explanation'
        ]
        
        # Only include columns that exist
        available_columns = [col for col in result_columns if col in recommendations.columns]
        final_recommendations = recommendations[available_columns]
        
        print(f"✅ Generated {len(final_recommendations)} recommendations!\n")
        
        return final_recommendations
    
    def get_recommendation_summary(
        self,
        recommendations: pd.DataFrame,
        user_input: Dict[str, str]
    ) -> Dict:
        """
        Get a summary of recommendations with insights
        
        Args:
            recommendations: DataFrame with recommendations
            user_input: User preferences
            
        Returns:
            Summary dictionary
        """
        summary = {
            'total_recommendations': len(recommendations),
            'average_match_score': recommendations['Match_Score'].mean(),
            'quality_distribution': recommendations['Match_Quality'].value_counts().to_dict(),
            'top_recommendation': recommendations.iloc[0]['Service_Name'] if len(recommendations) > 0 else None,
            'insight': self.explainer.generate_summary_insight(recommendations, user_input)
        }
        
        return summary
    
    def explain_recommendation(
        self,
        service_id: str,
        user_input: Dict[str, str]
    ) -> str:
        """
        Get detailed explanation for a specific service
        
        Args:
            service_id: Service ID to explain
            user_input: User preferences
            
        Returns:
            Detailed explanation string
        """
        # Find the service
        service_row = self.clean_df[self.clean_df['Service_ID'] == service_id]
        
        if len(service_row) == 0:
            return f"Service {service_id} not found."
        
        service_row = service_row.iloc[0]
        
        # Calculate match score
        user_vector = self.input_processor.process_input(user_input)['feature_vector']
        scores = self.ranking_engine.compute_weighted_similarity(user_input, user_vector)
        service_idx = self.clean_df[self.clean_df['Service_ID'] == service_id].index[0]
        match_score = scores[service_idx]
        
        match_quality = self.quality_generator.determine_match_quality(match_score)
        
        # Generate explanation
        explanation = self.explainer.generate_explanation(
            user_input,
            service_row,
            match_score,
            match_quality
        )
        
        return explanation
    
    def get_statistics(self) -> Dict:
        """Get statistics about the recommendation system"""
        return {
            'total_services': len(self.clean_df),
            'original_services': len(self.original_df),
            'services_after_cleaning': len(self.clean_df),
            'business_types': self.clean_df['Target_Business_Type'].nunique(),
            'price_categories': self.clean_df['Price_Category'].value_counts().to_dict(),
            'language_support': self.clean_df['Language_Support'].value_counts().to_dict(),
            'locations': self.clean_df['Location_Area'].nunique(),
            'cleaning_report': self.preprocessor.get_cleaning_report()
        }


if __name__ == "__main__":
    # Test with sample data
    print("="*70)
    print(" ML SERVICE RECOMMENDATION ENGINE - DEMONSTRATION")
    print("="*70 + "\n")
    
    # Create sample dataset
    sample_services = pd.DataFrame({
        'Service_ID': [f'SRV_{i:03d}' for i in range(1, 11)],
        'Service_Name': [
            'Professional Web Design',
            'Mobile App Development',
            'Digital Marketing Suite',
            'Cloud Hosting Services',
            'SEO Optimization',
            'E-commerce Platform',
            'Business Analytics',
            'CRM Software',
            'Payment Gateway Integration',
            'Cybersecurity Solutions'
        ],
        'Target_Business_Type': [
            'Technology', 'Technology', 'Retail', 'Technology', 'Retail',
            'Retail', 'Finance', 'Technology', 'Finance', 'Technology'
        ],
        'Price_Category': [
            'Low', 'High', 'Medium', 'Low', 'Medium',
            'High', 'Medium', 'High', 'Low', 'High'
        ],
        'Language_Support': [
            'Both', 'English', 'Both', 'Both', 'Hindi',
            'English', 'Both', 'English', 'Both', 'English'
        ],
        'Location_Area': [
            'Mumbai', 'Delhi', 'Remote', 'Mumbai', 'Remote',
            'Delhi', 'Mumbai', 'Remote', 'Mumbai', 'Delhi'
        ],
        'Description': [
            'Professional web design services for modern businesses with responsive layouts',
            'Custom mobile app development for iOS and Android platforms',
            'Comprehensive digital marketing solutions including social media and content',
            'Reliable cloud hosting with 99.9% uptime guarantee',
            'Advanced SEO services to boost your online visibility',
            'Complete e-commerce platform with payment integration',
            'Business intelligence and analytics dashboard solutions',
            'Customer relationship management software for enterprises',
            'Secure payment gateway integration for online businesses',
            'Enterprise-grade cybersecurity and data protection services'
        ]
    })
    
    # Initialize recommendation engine
    engine = RecommendationEngine(sample_services)
    
    # Display statistics
    print("📊 System Statistics:")
    stats = engine.get_statistics()
    print(f"  • Total Services: {stats['total_services']}")
    print(f"  • Business Types: {stats['business_types']}")
    print(f"  • Price Distribution: {stats['price_categories']}")
    print(f"  • Language Support: {stats['language_support']}\n")
    
    # Test recommendation
    print("="*70)
    print(" RECOMMENDATION TEST")
    print("="*70 + "\n")
    
    user_preferences = {
        'Target_Business_Type': 'Technology',
        'Price_Category': 'Low',
        'Language_Support': 'Both',
        'Location_Area': 'Mumbai'
    }
    
    print("👤 User Preferences:")
    for key, value in user_preferences.items():
        print(f"  • {key}: {value}")
    print("\n")
    
    # Get recommendations
    recommendations = engine.get_recommendations(user_preferences, top_n=3)
    
    print("🎯 TOP 3 RECOMMENDATIONS:\n")
    for idx, row in recommendations.iterrows():
        print(f"{idx + 1}. {row['Service_Name']}")
        print(f"   Match Score: {row['Match_Score']:.2f} | Quality: {row['Match_Quality']}")
        print(f"   {row['Explanation']}")
        print()
    
    # Get summary
    summary = engine.get_recommendation_summary(recommendations, user_preferences)
    print("="*70)
    print(f"💡 {summary['insight']}")
    print("="*70)
