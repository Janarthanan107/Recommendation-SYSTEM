"""
Module 2: Service Filtering & Ranking Engine
Module 3: Similarity Score & Match Quality Generator

Uses ML techniques (Cosine Similarity / KNN) to rank services and compute match scores.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from typing import Dict, List, Tuple
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ServiceRankingEngine:
    """Filters and ranks services based on user preferences"""
    
    def __init__(self, services_df: pd.DataFrame, weights: Dict[str, float] = None):
        """
        Initialize the ranking engine
        
        Args:
            services_df: DataFrame with encoded service features
            weights: Feature importance weights
        """
        self.services_df = services_df
        self.weights = weights or {
            'Target_Business_Type': 0.35,
            'Price_Category': 0.25,
            'Language_Support': 0.20,
            'Location_Area': 0.20
        }
        
        # Initialize KNN model
        self.knn_model = None
        self.feature_matrix = None
        
    def build_feature_matrix(self) -> np.ndarray:
        """
        Build feature matrix from encoded service data
        
        Returns:
            Feature matrix for all services
        """
        feature_cols = [col for col in self.services_df.columns if col.endswith('_encoded')]
        
        if len(feature_cols) == 0:
            raise ValueError("No encoded features found in dataframe")
        
        self.feature_matrix = self.services_df[feature_cols].values
        return self.feature_matrix
    
    def train_knn_model(self, n_neighbors: int = 10):
        """
        Train KNN model for similarity-based recommendations
        
        Args:
            n_neighbors: Number of neighbors to consider
        """
        if self.feature_matrix is None:
            self.build_feature_matrix()
        
        # Ensure we don't request more neighbors than we have samples
        n_neighbors = min(n_neighbors, len(self.feature_matrix))
        
        self.knn_model = NearestNeighbors(
            n_neighbors=n_neighbors,
            metric='euclidean'
        )
        self.knn_model.fit(self.feature_matrix)
        
        print(f"✅ KNN model trained with {n_neighbors} neighbors")
    
    def filter_services(self, user_input: Dict[str, str]) -> pd.DataFrame:
        """
        Initial filtering based on exact or close matches
        
        Args:
            user_input: User preferences
            
        Returns:
            Filtered dataframe
        """
        filtered_df = self.services_df.copy()
        
        # Apply filters
        if 'Target_Business_Type' in user_input:
            business_type = user_input['Target_Business_Type']
            filtered_df = filtered_df[
                filtered_df['Target_Business_Type'].str.lower() == business_type.lower()
            ]
        
        # If no exact matches, return all services for ranking
        if len(filtered_df) == 0:
            print("⚠️ No exact matches found, using all services for ranking")
            filtered_df = self.services_df.copy()
        
        return filtered_df
    
    def compute_similarity_scores(
        self, 
        user_vector: np.ndarray,
        method: str = 'cosine'
    ) -> np.ndarray:
        """
        Compute similarity scores between user and all services
        
        Args:
            user_vector: User feature vector
            method: 'cosine' or 'knn'
            
        Returns:
            Array of similarity scores
        """
        if self.feature_matrix is None:
            self.build_feature_matrix()
        
        if method == 'cosine':
            # Reshape user vector for sklearn
            user_vector_2d = user_vector.reshape(1, -1)
            
            # Compute cosine similarity
            similarities = cosine_similarity(user_vector_2d, self.feature_matrix)[0]
            
        elif method == 'knn':
            # Use KNN distances (convert to similarity)
            if self.knn_model is None:
                self.train_knn_model()
            
            # Compute distances for ALL services, not just neighbors
            user_vector_2d = user_vector.reshape(1, -1)
            distances = np.linalg.norm(self.feature_matrix - user_vector_2d, axis=1)
            
            # Convert distances to similarities (inverse relationship)
            # Add small epsilon to avoid division by zero
            similarities = 1 / (1 + distances)
            
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return similarities
    
    def compute_weighted_similarity(
        self,
        user_input: Dict[str, str],
        user_vector: np.ndarray
    ) -> np.ndarray:
        """
        Compute weighted similarity considering feature importance
        
        Args:
            user_input: User input dictionary
            user_vector: Encoded user feature vector
            
        Returns:
            Weighted similarity scores
        """
        if self.feature_matrix is None:
            self.build_feature_matrix()
        
        # Get feature names
        feature_cols = [col for col in self.services_df.columns if col.endswith('_encoded')]
        
        # Compute component-wise similarity
        scores = np.zeros(len(self.services_df))
        
        for idx, feature_col in enumerate(feature_cols):
            # Extract base feature name
            feature_name = feature_col.replace('_encoded', '')
            
            # Get weight for this feature
            weight = self.weights.get(feature_name, 0.25)
            
            # Compute match for this feature (1 if match, 0 if not)
            user_value = user_vector[idx]
            service_values = self.feature_matrix[:, idx]
            
            # Binary matching
            feature_scores = (service_values == user_value).astype(float)
            
            # Add weighted score
            scores += weight * feature_scores
        
        return scores
    
    def rank_services(
        self,
        user_input: Dict[str, str],
        user_vector: np.ndarray,
        top_n: int = 3,
        method: str = 'weighted'
    ) -> pd.DataFrame:
        """
        Rank all services and return top N
        
        Args:
            user_input: User preferences
            user_vector: Encoded user vector
            top_n: Number of top services to return
            method: Ranking method ('cosine', 'knn', 'weighted')
            
        Returns:
            DataFrame with top N ranked services
        """
        # Compute similarity scores
        if method == 'weighted':
            scores = self.compute_weighted_similarity(user_input, user_vector)
        else:
            scores = self.compute_similarity_scores(user_vector, method)
        
        # Add scores to dataframe
        ranked_df = self.services_df.copy()
        ranked_df['similarity_score'] = scores
        
        # Sort by score
        ranked_df = ranked_df.sort_values('similarity_score', ascending=False)
        
        # Return top N
        return ranked_df.head(top_n)


class MatchQualityGenerator:
    """Generates match quality ratings and scores"""
    
    def __init__(self, thresholds: Dict[str, float] = None):
        """
        Initialize match quality generator
        
        Args:
            thresholds: Quality thresholds for High/Medium/Low
        """
        self.thresholds = thresholds or {
            'High': 0.75,
            'Medium': 0.50,
            'Low': 0.0
        }
    
    def calculate_match_score(
        self,
        user_input: Dict[str, str],
        service_row: pd.Series,
        similarity_score: float
    ) -> float:
        """
        Calculate overall match score (0-1)
        
        Args:
            user_input: User preferences
            service_row: Service data
            similarity_score: Base similarity score
            
        Returns:
            Match score between 0 and 1
        """
        # Start with similarity score
        match_score = similarity_score
        
        # Bonus for exact matches
        exact_matches = 0
        total_features = 4
        
        features_to_check = [
            'Target_Business_Type',
            'Price_Category',
            'Language_Support',
            'Location_Area'
        ]
        
        for feature in features_to_check:
            if feature in user_input and feature in service_row.index:
                if str(service_row[feature]).lower() == str(user_input[feature]).lower():
                    exact_matches += 1
        
        # Add bonus (up to 0.2) for exact matches
        match_bonus = (exact_matches / total_features) * 0.2
        match_score = min(1.0, match_score + match_bonus)
        
        return match_score
    
    def determine_match_quality(self, match_score: float) -> str:
        """
        Determine match quality label based on score
        
        Args:
            match_score: Match score (0-1)
            
        Returns:
            Quality label ('High', 'Medium', or 'Low')
        """
        if match_score >= self.thresholds['High']:
            return 'High'
        elif match_score >= self.thresholds['Medium']:
            return 'Medium'
        else:
            return 'Low'
    
    def generate_quality_metrics(
        self,
        ranked_services: pd.DataFrame,
        user_input: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Generate match scores and quality labels for ranked services
        
        Args:
            ranked_services: DataFrame with ranked services
            user_input: User preferences
            
        Returns:
            DataFrame with match scores and quality
        """
        result_df = ranked_services.copy()
        
        # Calculate match scores
        result_df['Match_Score'] = result_df.apply(
            lambda row: self.calculate_match_score(
                user_input,
                row,
                row['similarity_score']
            ),
            axis=1
        )
        
        # Determine match quality
        result_df['Match_Quality'] = result_df['Match_Score'].apply(
            self.determine_match_quality
        )
        
        return result_df


if __name__ == "__main__":
    # Test with sample data
    from feature_engineering.encoder import FeatureEncoder
    
    sample_df = pd.DataFrame({
        'Service_ID': ['SRV_001', 'SRV_002', 'SRV_003', 'SRV_004'],
        'Service_Name': ['Web Design', 'App Development', 'SEO Services', 'Cloud Hosting'],
        'Target_Business_Type': ['Technology', 'Technology', 'Retail', 'Technology'],
        'Price_Category': ['Low', 'High', 'Medium', 'Low'],
        'Language_Support': ['Both', 'English', 'Hindi', 'Both'],
        'Location_Area': ['Mumbai', 'Delhi', 'Remote', 'Mumbai'],
        'Description': ['Professional web design', 'Mobile app dev', 'SEO optimization', 'Cloud solutions']
    })
    
    print("Sample Services:")
    print(sample_df)
    print("\n")
    
    # Encode features
    encoder = FeatureEncoder()
    categorical_features = ['Target_Business_Type', 'Price_Category', 
                           'Language_Support', 'Location_Area']
    encoded_df = encoder.fit_transform(sample_df, categorical_features)
    
    print("Encoded Services:")
    print(encoded_df)
    print("\n")
    
    # Initialize ranking engine
    ranking_engine = ServiceRankingEngine(encoded_df)
    
    # User input
    user_input = {
        'Target_Business_Type': 'Technology',
        'Price_Category': 'Low',
        'Language_Support': 'Both',
        'Location_Area': 'Mumbai'
    }
    
    user_vector = encoder.get_feature_vector(user_input)
    
    print("User Preferences:")
    print(user_input)
    print(f"User Vector: {user_vector}")
    print("\n")
    
    # Rank services
    ranked = ranking_engine.rank_services(user_input, user_vector, top_n=3)
    
    print("Top Ranked Services:")
    print(ranked[['Service_Name', 'similarity_score']])
    print("\n")
    
    # Generate match quality
    quality_gen = MatchQualityGenerator()
    final_results = quality_gen.generate_quality_metrics(ranked, user_input)
    
    print("Final Results with Match Quality:")
    print(final_results[['Service_Name', 'Match_Score', 'Match_Quality']])
