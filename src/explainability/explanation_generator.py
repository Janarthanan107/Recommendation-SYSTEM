"""
Module 4: Recommendation Explanation Generator
Creates meaningful, human-readable explanations for recommendations.
"""

import pandas as pd
from typing import Dict, List
import random


class ExplanationGenerator:
    """Generates human-readable explanations for recommendations"""
    
    def __init__(self):
        """Initialize explanation templates"""
        self.templates = {
            'perfect_match': [
                "Perfect match! This service aligns perfectly with all your requirements.",
                "Excellent choice! Matches all your specified preferences.",
                "Outstanding fit! This service meets every criterion you specified."
            ],
            'high_match': [
                "Great match! This service strongly aligns with your needs.",
                "Highly recommended! Closely matches your business requirements.",
                "Excellent fit! This service is well-suited for your preferences."
            ],
            'medium_match': [
                "Good option! This service meets most of your requirements.",
                "Solid choice! Aligns well with your key preferences.",
                "Recommended! A good fit for your business needs."
            ],
            'low_match': [
                "Alternative option that might work for your needs.",
                "Consider this service as a potential alternative.",
                "May be worth exploring based on partial matches."
            ]
        }
        
        self.feature_descriptions = {
            'Target_Business_Type': 'business type',
            'Price_Category': 'budget range',
            'Language_Support': 'language preference',
            'Location_Area': 'location requirement'
        }
    
    def generate_explanation(
        self,
        user_input: Dict[str, str],
        service_row: pd.Series,
        match_score: float,
        match_quality: str
    ) -> str:
        """
        Generate a comprehensive explanation for a recommendation
        
        Args:
            user_input: User preferences
            service_row: Service data
            match_score: Match score (0-1)
            match_quality: Match quality label
            
        Returns:
            Human-readable explanation string
        """
        # Start with quality-based template
        explanation_parts = []
        
        # Add opening statement based on match quality
        template_key = self._get_template_key(match_score)
        opening = random.choice(self.templates[template_key])
        explanation_parts.append(opening)
        
        # Analyze feature matches
        matching_features = self._analyze_feature_matches(user_input, service_row)
        
        # Generate feature-specific explanations
        if matching_features['exact_matches']:
            match_text = self._create_match_text(matching_features['exact_matches'])
            explanation_parts.append(match_text)
        
        # Add service description insight
        if 'Description' in service_row.index and service_row['Description']:
            description_insight = self._extract_description_insight(
                service_row['Description']
            )
            if description_insight:
                explanation_parts.append(description_insight)
        
        # Add specific highlights
        highlights = self._generate_highlights(user_input, service_row)
        if highlights:
            explanation_parts.append(highlights)
        
        # Combine all parts
        full_explanation = " ".join(explanation_parts)
        
        return full_explanation
    
    def _get_template_key(self, match_score: float) -> str:
        """Determine which template category to use"""
        if match_score >= 0.9:
            return 'perfect_match'
        elif match_score >= 0.75:
            return 'high_match'
        elif match_score >= 0.50:
            return 'medium_match'
        else:
            return 'low_match'
    
    def _analyze_feature_matches(
        self,
        user_input: Dict[str, str],
        service_row: pd.Series
    ) -> Dict[str, List[str]]:
        """
        Analyze which features match and which don't
        
        Returns:
            Dictionary with exact_matches and partial_matches
        """
        exact_matches = []
        partial_matches = []
        
        for feature, description in self.feature_descriptions.items():
            if feature in user_input and feature in service_row.index:
                user_value = str(user_input[feature]).lower()
                service_value = str(service_row[feature]).lower()
                
                if user_value == service_value:
                    exact_matches.append({
                        'feature': feature,
                        'description': description,
                        'value': service_row[feature]
                    })
                else:
                    # Check for partial matches
                    if self._is_partial_match(feature, user_value, service_value):
                        partial_matches.append({
                            'feature': feature,
                            'description': description,
                            'user_value': user_input[feature],
                            'service_value': service_row[feature]
                        })
        
        return {
            'exact_matches': exact_matches,
            'partial_matches': partial_matches
        }
    
    def _is_partial_match(self, feature: str, user_value: str, service_value: str) -> bool:
        """Check if there's a partial match between values"""
        # Language partial matches
        if feature == 'Language_Support':
            if 'both' in service_value:
                return True
        
        # Location partial matches
        if feature == 'Location_Area':
            if 'remote' in service_value.lower():
                return True
        
        return False
    
    def _create_match_text(self, exact_matches: List[Dict]) -> str:
        """Create text describing exact matches"""
        if not exact_matches:
            return ""
        
        if len(exact_matches) == 1:
            match = exact_matches[0]
            return f"Matches your {match['description']} requirement ({match['value']})."
        
        elif len(exact_matches) == 2:
            return f"Matches your {exact_matches[0]['description']} and {exact_matches[1]['description']} requirements."
        
        else:
            # Multiple matches
            match_descriptions = [m['description'] for m in exact_matches[:-1]]
            text = f"Matches your {', '.join(match_descriptions)}, and {exact_matches[-1]['description']} requirements."
            return text
    
    def _extract_description_insight(self, description: str) -> str:
        """Extract relevant insight from service description"""
        # Take first meaningful sentence or phrase
        if len(description) > 100:
            # Truncate and add focus
            return f"Specializes in {description[:80]}..."
        elif len(description) > 20:
            return description
        else:
            return ""
    
    def _generate_highlights(
        self,
        user_input: Dict[str, str],
        service_row: pd.Series
    ) -> str:
        """Generate specific highlights about why this service is recommended"""
        highlights = []
        
        # Price highlights
        if 'Price_Category' in service_row.index:
            price = service_row['Price_Category']
            if price == 'Low':
                highlights.append("cost-effective solution")
            elif price == 'High':
                highlights.append("premium quality service")
        
        # Language highlights
        if 'Language_Support' in service_row.index:
            if service_row['Language_Support'] == 'Both':
                highlights.append("bilingual support available")
        
        # Location highlights
        if 'Location_Area' in service_row.index:
            location = service_row['Location_Area']
            if 'remote' in str(location).lower():
                highlights.append("remote service available")
            elif location in user_input.get('Location_Area', ''):
                highlights.append(f"local service in {location}")
        
        if highlights:
            return f"Features: {', '.join(highlights)}."
        return ""
    
    def generate_batch_explanations(
        self,
        user_input: Dict[str, str],
        recommendations_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Generate explanations for multiple recommendations
        
        Args:
            user_input: User preferences
            recommendations_df: DataFrame with recommendations
            
        Returns:
            DataFrame with added Explanation column
        """
        result_df = recommendations_df.copy()
        
        explanations = []
        for idx, row in result_df.iterrows():
            explanation = self.generate_explanation(
                user_input,
                row,
                row.get('Match_Score', 0.5),
                row.get('Match_Quality', 'Medium')
            )
            explanations.append(explanation)
        
        result_df['Explanation'] = explanations
        
        return result_df
    
    def generate_summary_insight(
        self,
        recommendations_df: pd.DataFrame,
        user_input: Dict[str, str]
    ) -> str:
        """
        Generate an overall summary of the recommendations
        
        Args:
            recommendations_df: DataFrame with recommendations
            user_input: User preferences
            
        Returns:
            Summary string
        """
        num_recommendations = len(recommendations_df)
        avg_score = recommendations_df.get('Match_Score', pd.Series([0])).mean()
        
        high_quality_count = len(
            recommendations_df[recommendations_df.get('Match_Quality', '') == 'High']
        )
        
        summary_parts = []
        
        # Overall assessment
        if avg_score >= 0.8:
            summary_parts.append("🌟 Excellent! We found highly relevant services for you.")
        elif avg_score >= 0.6:
            summary_parts.append("✅ Good results! Several services match your needs well.")
        else:
            summary_parts.append("📊 Here are some services that may interest you.")
        
        # Quality breakdown
        if high_quality_count > 0:
            summary_parts.append(
                f"{high_quality_count} out of {num_recommendations} are high-quality matches."
            )
        
        # Business type focus
        if 'Target_Business_Type' in user_input:
            business = user_input['Target_Business_Type']
            summary_parts.append(f"All recommendations are tailored for {business} businesses.")
        
        return " ".join(summary_parts)


if __name__ == "__main__":
    # Test explanation generation
    import pandas as pd
    
    # Sample service
    service_data = {
        'Service_ID': 'SRV_001',
        'Service_Name': 'Professional Web Design',
        'Target_Business_Type': 'Technology',
        'Price_Category': 'Low',
        'Language_Support': 'Both',
        'Location_Area': 'Mumbai',
        'Description': 'Professional web design services for modern businesses',
        'Match_Score': 0.85,
        'Match_Quality': 'High'
    }
    
    service_row = pd.Series(service_data)
    
    user_input = {
        'Target_Business_Type': 'Technology',
        'Price_Category': 'Low',
        'Language_Support': 'Both',
        'Location_Area': 'Mumbai'
    }
    
    # Generate explanation
    explainer = ExplanationGenerator()
    explanation = explainer.generate_explanation(
        user_input,
        service_row,
        service_row['Match_Score'],
        service_row['Match_Quality']
    )
    
    print("Service:", service_data['Service_Name'])
    print("Match Score:", service_data['Match_Score'])
    print("Match Quality:", service_data['Match_Quality'])
    print("\nExplanation:")
    print(explanation)
    
    # Test batch generation
    print("\n" + "="*60)
    print("Testing Batch Explanations")
    print("="*60 + "\n")
    
    recommendations_df = pd.DataFrame([
        {
            'Service_Name': 'Web Design Pro',
            'Target_Business_Type': 'Technology',
            'Price_Category': 'Low',
            'Language_Support': 'Both',
            'Location_Area': 'Mumbai',
            'Description': 'Expert web design',
            'Match_Score': 0.90,
            'Match_Quality': 'High'
        },
        {
            'Service_Name': 'App Development',
            'Target_Business_Type': 'Technology',
            'Price_Category': 'Medium',
            'Language_Support': 'English',
            'Location_Area': 'Remote',
            'Description': 'Mobile app development',
            'Match_Score': 0.65,
            'Match_Quality': 'Medium'
        }
    ])
    
    results = explainer.generate_batch_explanations(user_input, recommendations_df)
    
    for idx, row in results.iterrows():
        print(f"\n{row['Service_Name']} ({row['Match_Quality']} Match):")
        print(f"  {row['Explanation']}")
    
    # Generate summary
    print("\n" + "="*60)
    print("Summary Insight:")
    print("="*60)
    summary = explainer.generate_summary_insight(results, user_input)
    print(summary)
