"""
Utility functions for the recommendation system
"""

import pandas as pd
import os
import gdown
from typing import Dict, Optional


def download_dataset_from_drive(folder_url: str, output_dir: str) -> str:
    """
    Download dataset from Google Drive
    
    Args:
        folder_url: Google Drive folder URL
        output_dir: Directory to save the file
        
    Returns:
        Path to downloaded file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📥 Downloading dataset from Google Drive...")
    
    try:
        # Extract folder ID from URL
        if '/folders/' in folder_url:
            folder_id = folder_url.split('/folders/')[1].split('?')[0]
        else:
            raise ValueError("Invalid Google Drive folder URL")
        
        # Download folder
        output_path = os.path.join(output_dir, 'services_dataset.csv')
        gdown.download_folder(id=folder_id, output=output_dir, quiet=False)
        
        # Find CSV file in downloaded folder
        for file in os.listdir(output_dir):
            if file.endswith('.csv'):
                return os.path.join(output_dir, file)
        
        raise FileNotFoundError("No CSV file found in downloaded folder")
        
    except Exception as e:
        print(f"⚠️  Could not download from Google Drive: {e}")
        print("ℹ️  Please manually download the dataset and place it in the 'data' folder")
        return None


def create_sample_dataset(output_path: str) -> str:
    """
    Create a sample dataset for testing
    
    Args:
        output_path: Path to save the sample dataset
        
    Returns:
        Path to created dataset
    """
    print("📝 Creating sample dataset...")
    
    sample_data = {
        'Service_ID': [f'SRV_{i:04d}' for i in range(1, 51)],
        'Service_Name': [
            # Technology Services (15)
            'Professional Web Design', 'Mobile App Development', 'Cloud Hosting Pro',
            'AI Chatbot Development', 'Website Maintenance', 'Custom Software Development',
            'Database Management', 'API Integration Services', 'UI/UX Design Studio',
            'DevOps Consulting', 'Tech Support 24/7', 'Code Review Service',
            'System Migration Services', 'IT Infrastructure Setup', 'Cybersecurity Audit',
            
            # Retail Services (15)
            'Digital Marketing Suite', 'SEO Optimization Pro', 'E-commerce Platform',
            'Social Media Management', 'Content Writing Services', 'Brand Strategy Consulting',
            'Product Photography', 'Email Marketing Automation', 'Market Research Analysis',
            'Customer Analytics Dashboard', 'Inventory Management System', 'POS System Integration',
            'Retail Analytics Software', 'Customer Loyalty Program', 'Online Store Setup',
            
            # Finance Services (10)
            'Business Analytics Dashboard', 'Payment Gateway Integration', 'Accounting Software',
            'Financial Planning Tools', 'Tax Compliance Software', 'Invoice Management System',
            'Expense Tracking App', 'Payroll Management', 'Investment Portfolio Tracker',
            'Credit Score Analysis',
            
            # Healthcare Services (5)
            'Patient Management System', 'Telemedicine Platform', 'Medical Records Software',
            'Appointment Scheduling App', 'Health Analytics Dashboard',
            
            # Education Services (5)
            'Learning Management System', 'Online Course Platform', 'Student Portal Development',
            'Virtual Classroom Software', 'Education Analytics Tools'
        ],
        'Target_Business_Type': (
            ['Technology'] * 15 +
            ['Retail'] * 15 +
            ['Finance'] * 10 +
            ['Healthcare'] * 5 +
            ['Education'] * 5
        ),
        'Price_Category': [
            # Technology - mixed
            'Low', 'High', 'Low', 'High', 'Low', 'High', 'Medium', 'Medium', 'High', 'High',
            'Low', 'Medium', 'High', 'Medium', 'High',
            # Retail - mixed
            'Medium', 'Medium', 'High', 'Medium', 'Low', 'High', 'Medium', 'Medium', 'Low', 'Medium',
            'High', 'Medium', 'High', 'Low', 'Medium',
            # Finance - mixed
            'Medium', 'Low', 'High', 'High', 'Medium', 'Medium', 'Low', 'High', 'High', 'Medium',
            # Healthcare - mostly high
            'High', 'High', 'High', 'Medium', 'High',
            # Education - mixed
            'Medium', 'High', 'Medium', 'Medium', 'High'
        ],
        'Language_Support': [
            # Technology - mixed
            'Both', 'English', 'Both', 'English', 'Both', 'English', 'Both', 'English', 'English', 'Both',
            'Both', 'English', 'Both', 'Both', 'English',
            # Retail - mixed
            'Both', 'Hindi', 'English', 'Both', 'Both', 'English', 'Both', 'English', 'Hindi', 'Both',
            'English', 'Both', 'English', 'Both', 'Both',
            # Finance - mostly both
            'Both', 'Both', 'English', 'English', 'Both', 'Both', 'Both', 'English', 'English', 'Both',
            # Healthcare - mostly both
            'Both', 'Both', 'English', 'Both', 'English',
            # Education - mostly both
            'Both', 'English', 'Both', 'Both', 'English'
        ],
        'Location_Area': [
            # Technology - varied
            'Mumbai', 'Delhi', 'Remote', 'Bangalore', 'Mumbai', 'Remote', 'Delhi', 'Remote', 'Bangalore', 'Mumbai',
            'Remote', 'Delhi', 'Bangalore', 'Mumbai', 'Remote',
            # Retail - varied
            'Remote', 'Mumbai', 'Delhi', 'Remote', 'Bangalore', 'Mumbai', 'Delhi', 'Remote', 'Mumbai', 'Remote',
            'Bangalore', 'Delhi', 'Remote', 'Mumbai', 'Remote',
            # Finance - more remote
            'Mumbai', 'Mumbai', 'Remote', 'Delhi', 'Remote', 'Mumbai', 'Remote', 'Bangalore', 'Remote', 'Delhi',
            # Healthcare - mostly local
            'Mumbai', 'Delhi', 'Bangalore', 'Mumbai', 'Remote',
            # Education - mix
            'Remote', 'Remote', 'Mumbai', 'Remote', 'Bangalore'
        ]
    }
    
    # Generate descriptions
    descriptions = [
        # Technology (15)
        'Modern web design services with responsive layouts and SEO optimization',
        'Custom iOS and Android app development with cloud integration',
        'Scalable cloud hosting solutions with 99.9% uptime guarantee',
        'AI-powered chatbot development for customer service automation',
        'Comprehensive website maintenance and security updates',
        'Tailored software solutions for enterprise business needs',
        'Professional database design, optimization and management services',
        'Seamless API integration for third-party services and platforms',
        'User-centered design services with modern aesthetics',
        'DevOps consulting for continuous integration and deployment',
        'Round-the-clock technical support for your IT infrastructure',
        'Professional code review and quality assurance services',
        'Smooth system migration with zero downtime guarantee',
        'Complete IT infrastructure planning and implementation',
        'Comprehensive security audits and vulnerability assessments',
        
        # Retail (15)
        'Full-service digital marketing including SEO, PPC, and social media',
        'Advanced SEO services to boost organic traffic and rankings',
        'Complete e-commerce platform with payment and shipping integration',
        'Strategic social media management across all major platforms',
        'Professional content creation for blogs, websites and marketing',
        'Strategic brand development and positioning services',
        'Professional product photography and image editing',
        'Automated email marketing campaigns with analytics',
        'In-depth market research and competitive analysis',
        'Customer behavior analytics and insights dashboard',
        'Cloud-based inventory tracking and management system',
        'Modern POS system integration for retail businesses',
        'Comprehensive retail analytics and reporting tools',
        'Customer loyalty and rewards program development',
        'Complete online store setup with marketing integration',
        
        # Finance (10)
        'Interactive business analytics dashboards with real-time data',
        'Secure payment processing integration for online businesses',
        'Cloud-based accounting software for small businesses',
        'Comprehensive financial planning and forecasting tools',
        'Automated tax compliance and filing software',
        'Smart invoice generation and payment tracking system',
        'Expense tracking app with receipt scanning',
        'Complete payroll management with tax calculations',
        'Investment portfolio tracking and analysis tools',
        'Credit score monitoring and improvement recommendations',
        
        # Healthcare (5)
        'Complete patient management and EMR system',
        'HIPAA-compliant telemedicine platform with video consultations',
        'Secure electronic medical records management system',
        'Online appointment scheduling with automated reminders',
        'Healthcare analytics for patient outcomes and operations',
        
        # Education (5)
        'Full-featured LMS with course management and tracking',
        'Interactive online course platform with video streaming',
        'Student information system with grade management',
        'Live virtual classroom software with collaboration tools',
        'Education analytics dashboard for student performance tracking'
    ]
    
    sample_data['Description'] = descriptions
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Save to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"✅ Sample dataset created with {len(df)} services")
    print(f"   Saved to: {output_path}")
    
    return output_path


def load_dataset(file_path: Optional[str] = None, create_sample: bool = True) -> pd.DataFrame:
    """
    Load dataset from file or create sample
    
    Args:
        file_path: Path to dataset file
        create_sample: Whether to create sample if file not found
        
    Returns:
        Loaded DataFrame
    """
    if file_path and os.path.exists(file_path):
        print(f"📂 Loading dataset from: {file_path}")
        df = pd.read_csv(file_path)
        print(f"✅ Loaded {len(df)} services from dataset")
        return df
    
    elif create_sample:
        print("⚠️  Dataset file not found, creating sample dataset...")
        default_path = os.path.join('data', 'services_dataset.csv')
        create_sample_dataset(default_path)
        return pd.read_csv(default_path)
    
    else:
        raise FileNotFoundError(f"Dataset file not found: {file_path}")


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"₹{amount:,.2f}"


def get_price_range(category: str) -> str:
    """Get price range description for a category"""
    ranges = {
        'Low': '₹5,000 - ₹25,000',
        'Medium': '₹25,000 - ₹1,00,000',
        'High': '₹1,00,000+'
    }
    return ranges.get(category, 'Contact for pricing')


def validate_dataset(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate dataset structure
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    required_columns = [
        'Service_ID',
        'Service_Name',
        'Target_Business_Type',
        'Price_Category',
        'Language_Support',
        'Location_Area',
        'Description'
    ]
    
    errors = []
    
    # Check required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Check for empty dataframe
    if len(df) == 0:
        errors.append("Dataset is empty")
    
    return len(errors) == 0, errors


if __name__ == "__main__":
    # Test utilities
    print("Testing utility functions...\n")
    
    # Create sample dataset
    sample_path = 'data/test_services.csv'
    create_sample_dataset(sample_path)
    
    # Load dataset
    df = load_dataset(sample_path)
    print(f"\nDataset shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    
    # Validate dataset
    is_valid, errors = validate_dataset(df)
    print(f"\nDataset valid: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    # Test price formatting
    print(f"\nPrice range for Low: {get_price_range('Low')}")
    print(f"Price range for Medium: {get_price_range('Medium')}")
    print(f"Price range for High: {get_price_range('High')}")
