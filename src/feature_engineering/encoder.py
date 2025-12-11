"""
Module 1: User Input Processing & Feature Encoding
Handles extraction and conversion of user inputs into ML-ready numerical vectors
using encoding and feature mapping.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from typing import Dict, List, Tuple
import pickle


class FeatureEncoder:
    """Encodes categorical features into numerical representations"""
    
    def __init__(self):
        """Initialize encoders"""
        self.label_encoders = {}
        self.feature_mappings = {}
        self.fitted = False
        
    def fit(self, df: pd.DataFrame, categorical_features: List[str]):
        """
        Fit encoders on the dataset
        
        Args:
            df: Training dataframe
            categorical_features: List of categorical column names
        """
        print("🔧 Fitting feature encoders...")
        
        for feature in categorical_features:
            if feature in df.columns:
                # Create label encoder for each feature
                le = LabelEncoder()
                le.fit(df[feature].astype(str))
                self.label_encoders[feature] = le
                
                # Create mapping dictionary
                self.feature_mappings[feature] = {
                    label: idx for idx, label in enumerate(le.classes_)
                }
                
                print(f"  ├─ Encoded {feature}: {len(le.classes_)} unique values")
        
        self.fitted = True
        print("✅ Feature encoders fitted successfully!\n")
        
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform categorical features to numerical
        
        Args:
            df: Dataframe to transform
            
        Returns:
            Dataframe with encoded features
        """
        if not self.fitted:
            raise ValueError("Encoders must be fitted before transform")
        
        df_encoded = df.copy()
        
        for feature, encoder in self.label_encoders.items():
            if feature in df_encoded.columns:
                # Handle unknown categories by using -1
                df_encoded[f'{feature}_encoded'] = df_encoded[feature].apply(
                    lambda x: self.safe_encode(encoder, str(x))
                )
        
        return df_encoded
    
    def safe_encode(self, encoder: LabelEncoder, value: str) -> int:
        """
        Safely encode a value, returning -1 for unknown values
        
        Args:
            encoder: Fitted LabelEncoder
            value: Value to encode
            
        Returns:
            Encoded integer value
        """
        try:
            return encoder.transform([value])[0]
        except ValueError:
            # Unknown category, return -1
            return -1
    
    def fit_transform(self, df: pd.DataFrame, categorical_features: List[str]) -> pd.DataFrame:
        """
        Fit and transform in one step
        
        Args:
            df: Dataframe to fit and transform
            categorical_features: List of categorical features
            
        Returns:
            Transformed dataframe
        """
        self.fit(df, categorical_features)
        return self.transform(df)
    
    def get_feature_vector(self, user_input: Dict[str, str]) -> np.ndarray:
        """
        Convert user input dictionary to feature vector
        
        Args:
            user_input: Dictionary with user preferences
            
        Returns:
            Numerical feature vector
        """
        feature_vector = []
        
        for feature, encoder in self.label_encoders.items():
            if feature in user_input:
                encoded_value = self.safe_encode(encoder, str(user_input[feature]))
                feature_vector.append(encoded_value)
            else:
                feature_vector.append(-1)  # Missing value
        
        return np.array(feature_vector)
    
    def save(self, filepath: str):
        """Save encoders to file"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'label_encoders': self.label_encoders,
                'feature_mappings': self.feature_mappings,
                'fitted': self.fitted
            }, f)
        print(f"💾 Encoders saved to {filepath}")
    
    def load(self, filepath: str):
        """Load encoders from file"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.label_encoders = data['label_encoders']
            self.feature_mappings = data['feature_mappings']
            self.fitted = data['fitted']
        print(f"📂 Encoders loaded from {filepath}")


class UserInputProcessor:
    """Processes and validates user inputs"""
    
    def __init__(self, encoder: FeatureEncoder):
        """
        Initialize processor with feature encoder
        
        Args:
            encoder: Fitted FeatureEncoder instance
        """
        self.encoder = encoder
        
    def validate_input(self, user_input: Dict[str, str]) -> Tuple[bool, List[str]]:
        """
        Validate user input
        
        Args:
            user_input: User preferences dictionary
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields
        required_fields = ['Target_Business_Type', 'Price_Category', 
                          'Language_Support', 'Location_Area']
        
        for field in required_fields:
            if field not in user_input or not user_input[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate budget range if provided
        if 'budget_min' in user_input and 'budget_max' in user_input:
            try:
                min_budget = float(user_input['budget_min'])
                max_budget = float(user_input['budget_max'])
                if min_budget > max_budget:
                    errors.append("Minimum budget cannot exceed maximum budget")
            except ValueError:
                errors.append("Budget values must be numbers")
        
        return len(errors) == 0, errors
    
    def process_input(self, user_input: Dict[str, str]) -> Dict:
        """
        Process and prepare user input for recommendation
        
        Args:
            user_input: Raw user input
            
        Returns:
            Processed input dictionary with encoded features
        """
        # Validate input
        is_valid, errors = self.validate_input(user_input)
        if not is_valid:
            raise ValueError(f"Invalid input: {', '.join(errors)}")
        
        # Standardize input values
        processed = self.standardize_input(user_input)
        
        # Generate feature vector
        feature_vector = self.encoder.get_feature_vector(processed)
        
        # Create result dictionary
        result = {
            'original_input': user_input,
            'processed_input': processed,
            'feature_vector': feature_vector,
            'feature_names': list(self.encoder.label_encoders.keys())
        }
        
        return result
    
    def standardize_input(self, user_input: Dict[str, str]) -> Dict[str, str]:
        """
        Standardize user input values to match dataset format
        
        Args:
            user_input: Raw user input
            
        Returns:
            Standardized input dictionary
        """
        standardized = user_input.copy()
        
        # Standardize Target_Business_Type
        if 'Target_Business_Type' in standardized:
            standardized['Target_Business_Type'] = standardized['Target_Business_Type'].strip().title()
        
        # Standardize Price_Category
        if 'Price_Category' in standardized:
            price_mapping = {
                'low': 'Low',
                'medium': 'Medium',
                'high': 'High'
            }
            standardized['Price_Category'] = price_mapping.get(
                standardized['Price_Category'].lower(),
                standardized['Price_Category'].title()
            )
        
        # Standardize Language_Support
        if 'Language_Support' in standardized:
            lang_mapping = {
                'hindi': 'Hindi',
                'english': 'English',
                'both': 'Both'
            }
            standardized['Language_Support'] = lang_mapping.get(
                standardized['Language_Support'].lower(),
                standardized['Language_Support'].title()
            )
        
        # Standardize Location_Area
        if 'Location_Area' in standardized:
            standardized['Location_Area'] = standardized['Location_Area'].strip().title()
        
        return standardized
    
    def create_user_profile_vector(self, processed_input: Dict) -> np.ndarray:
        """
        Create a comprehensive user profile vector for similarity matching
        
        Args:
            processed_input: Processed user input
            
        Returns:
            User profile vector
        """
        return processed_input['feature_vector']


if __name__ == "__main__":
    # Test with sample data
    sample_df = pd.DataFrame({
        'Target_Business_Type': ['Technology', 'Retail', 'Healthcare', 'Technology'],
        'Price_Category': ['Low', 'Medium', 'High', 'Low'],
        'Language_Support': ['Both', 'English', 'Hindi', 'Both'],
        'Location_Area': ['Mumbai', 'Delhi', 'Remote', 'Mumbai']
    })
    
    print("Sample Dataset:")
    print(sample_df)
    print("\n")
    
    # Initialize and fit encoder
    encoder = FeatureEncoder()
    categorical_features = ['Target_Business_Type', 'Price_Category', 
                           'Language_Support', 'Location_Area']
    
    encoded_df = encoder.fit_transform(sample_df, categorical_features)
    print("\nEncoded Dataset:")
    print(encoded_df)
    
    # Test user input processing
    print("\n" + "="*50)
    print("Testing User Input Processing")
    print("="*50)
    
    processor = UserInputProcessor(encoder)
    
    user_input = {
        'Target_Business_Type': 'technology',
        'Price_Category': 'low',
        'Language_Support': 'both',
        'Location_Area': 'Mumbai'
    }
    
    print("\nUser Input:")
    print(user_input)
    
    result = processor.process_input(user_input)
    print("\nProcessed Result:")
    print(f"Feature Vector: {result['feature_vector']}")
    print(f"Feature Names: {result['feature_names']}")
