"""
Module 5: Data Cleaning & Preprocessing
Ensures the dataset is ML-ready by handling missing values, cleaning text fields,
standardizing categories, and removing duplicates.
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Optional


class DataPreprocessor:
    """Handles all data cleaning and preprocessing operations"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the preprocessor with a dataframe
        
        Args:
            df: Raw dataframe to preprocess
        """
        self.df = df.copy()
        self.original_shape = df.shape
        self.cleaning_report = {}
        
    def clean_dataset(self) -> pd.DataFrame:
        """
        Master cleaning pipeline - calls all cleaning methods
        
        Returns:
            Cleaned dataframe
        """
        print("🧹 Starting data cleaning pipeline...")
        
        # Step 1: Remove duplicates
        self.remove_duplicates()
        
        # Step 2: Handle missing values
        self.handle_missing_values()
        
        # Step 3: Clean text fields
        self.clean_text_fields()
        
        # Step 4: Standardize categories
        self.standardize_categories()
        
        # Step 5: Validate data types
        self.validate_data_types()
        
        # Step 6: Remove invalid records
        self.remove_invalid_records()
        
        print(f"✅ Cleaning complete! {self.original_shape[0]} → {self.df.shape[0]} records")
        
        return self.df
    
    def remove_duplicates(self):
        """Remove duplicate service entries"""
        initial_count = len(self.df)
        
        # Remove exact duplicates
        self.df.drop_duplicates(inplace=True)
        
        # Remove duplicates based on Service_ID
        if 'Service_ID' in self.df.columns:
            self.df.drop_duplicates(subset=['Service_ID'], keep='first', inplace=True)
        
        removed = initial_count - len(self.df)
        self.cleaning_report['duplicates_removed'] = removed
        print(f"  ├─ Removed {removed} duplicate records")
    
    def handle_missing_values(self):
        """Handle missing values intelligently"""
        missing_before = self.df.isnull().sum().sum()
        
        # Fill missing Service_ID with auto-generated IDs
        if 'Service_ID' in self.df.columns:
            self.df['Service_ID'] = self.df['Service_ID'].fillna(
                pd.Series([f"SRV_{x:04d}" for x in self.df.index], index=self.df.index)
            )
        
        # Fill missing Service_Name with placeholder
        if 'Service_Name' in self.df.columns:
            self.df['Service_Name'] = self.df['Service_Name'].fillna('Unnamed Service')
        
        # Fill missing categorical fields with mode or 'Unknown'
        categorical_cols = ['Target_Business_Type', 'Price_Category', 
                           'Language_Support', 'Location_Area']
        
        for col in categorical_cols:
            if col in self.df.columns:
                mode_value = self.df[col].mode()
                if len(mode_value) > 0:
                    self.df[col] = self.df[col].fillna(mode_value[0])
                else:
                    self.df[col] = self.df[col].fillna('Unknown')
        
        # Fill missing descriptions
        if 'Description' in self.df.columns:
            self.df['Description'] = self.df['Description'].fillna(
                'No description available for this service.'
            )
        
        missing_after = self.df.isnull().sum().sum()
        self.cleaning_report['missing_values_handled'] = missing_before - missing_after
        print(f"  ├─ Handled {missing_before} missing values")
    
    def clean_text_fields(self):
        """Clean and standardize text fields"""
        text_columns = ['Service_Name', 'Description']
        
        for col in text_columns:
            if col in self.df.columns:
                # Remove extra whitespace
                self.df[col] = self.df[col].str.strip()
                self.df[col] = self.df[col].str.replace(r'\s+', ' ', regex=True)
                
                # Remove special characters (keep alphanumeric and basic punctuation)
                self.df[col] = self.df[col].str.replace(r'[^\w\s\.,!?-]', '', regex=True)
                
                # Capitalize first letter for Service_Name
                if col == 'Service_Name':
                    self.df[col] = self.df[col].str.title()
        
        print(f"  ├─ Cleaned text fields")
    
    def standardize_categories(self):
        """Standardize categorical values"""
        
        # Standardize Target_Business_Type
        if 'Target_Business_Type' in self.df.columns:
            self.df['Target_Business_Type'] = self.df['Target_Business_Type'].str.strip().str.title()
            
        # Standardize Price_Category
        if 'Price_Category' in self.df.columns:
            price_mapping = {
                'low': 'Low',
                'medium': 'Medium',
                'med': 'Medium',
                'high': 'High',
                'expensive': 'High',
                'cheap': 'Low',
                'affordable': 'Low'
            }
            self.df['Price_Category'] = self.df['Price_Category'].str.lower().map(
                lambda x: price_mapping.get(x, x.title())
            )
            
        # Standardize Language_Support
        if 'Language_Support' in self.df.columns:
            language_mapping = {
                'hindi': 'Hindi',
                'english': 'English',
                'both': 'Both',
                'bilingual': 'Both',
                'hindi/english': 'Both',
                'english/hindi': 'Both'
            }
            self.df['Language_Support'] = self.df['Language_Support'].str.lower().map(
                lambda x: language_mapping.get(x, x.title())
            )
            
        # Standardize Location_Area
        if 'Location_Area' in self.df.columns:
            self.df['Location_Area'] = self.df['Location_Area'].str.strip().str.title()
            # Handle "Remote" variations
            self.df['Location_Area'] = self.df['Location_Area'].replace({
                'Online': 'Remote',
                'Virtual': 'Remote',
                'Anywhere': 'Remote'
            })
        
        print(f"  ├─ Standardized categorical values")
    
    def validate_data_types(self):
        """Ensure correct data types for all columns"""
        
        # Ensure Service_ID is string
        if 'Service_ID' in self.df.columns:
            self.df['Service_ID'] = self.df['Service_ID'].astype(str)
        
        # Ensure categorical columns are strings
        string_cols = ['Service_Name', 'Target_Business_Type', 'Price_Category',
                      'Language_Support', 'Location_Area', 'Description']
        
        for col in string_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str)
        
        print(f"  ├─ Validated data types")
    
    def remove_invalid_records(self):
        """Remove records that don't meet minimum quality standards"""
        initial_count = len(self.df)
        
        # Remove records with invalid Price_Category
        if 'Price_Category' in self.df.columns:
            valid_prices = ['Low', 'Medium', 'High', 'Unknown']
            self.df = self.df[self.df['Price_Category'].isin(valid_prices)]
        
        # Remove records with invalid Language_Support
        if 'Language_Support' in self.df.columns:
            valid_languages = ['Hindi', 'English', 'Both', 'Unknown']
            self.df = self.df[self.df['Language_Support'].isin(valid_languages)]
        
        # Remove records with extremely short descriptions (likely invalid)
        if 'Description' in self.df.columns:
            self.df = self.df[self.df['Description'].str.len() >= 10]
        
        removed = initial_count - len(self.df)
        self.cleaning_report['invalid_records_removed'] = removed
        print(f"  └─ Removed {removed} invalid records")
    
    def get_cleaning_report(self) -> Dict:
        """Return a report of all cleaning operations"""
        return {
            'original_records': self.original_shape[0],
            'final_records': self.df.shape[0],
            'records_removed': self.original_shape[0] - self.df.shape[0],
            **self.cleaning_report
        }


def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Convenience function to load and clean dataset in one step
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Cleaned dataframe
    """
    print(f"📂 Loading dataset from: {file_path}")
    df = pd.read_csv(file_path)
    
    preprocessor = DataPreprocessor(df)
    cleaned_df = preprocessor.clean_dataset()
    
    # Print summary
    report = preprocessor.get_cleaning_report()
    print(f"\n📊 Cleaning Summary:")
    print(f"  • Original records: {report['original_records']}")
    print(f"  • Final records: {report['final_records']}")
    print(f"  • Removed: {report['records_removed']}")
    
    return cleaned_df


if __name__ == "__main__":
    # Test with sample data
    sample_data = {
        'Service_ID': ['SRV_001', 'SRV_002', 'SRV_002', None],
        'Service_Name': ['web design', '  APP Development  ', 'Mobile Dev', None],
        'Target_Business_Type': ['technology', 'Technology', 'Tech', 'retail'],
        'Price_Category': ['low', 'HIGH', 'medium', 'expensive'],
        'Language_Support': ['both', 'English', 'hindi', 'bilingual'],
        'Location_Area': ['Mumbai', '  Delhi  ', 'Remote', 'online'],
        'Description': ['Great service', 'Excellent work here', 'Top quality', 'A']
    }
    
    df = pd.DataFrame(sample_data)
    print("Before cleaning:")
    print(df)
    print("\n")
    
    preprocessor = DataPreprocessor(df)
    cleaned = preprocessor.clean_dataset()
    
    print("\nAfter cleaning:")
    print(cleaned)
    print("\nReport:", preprocessor.get_cleaning_report())
