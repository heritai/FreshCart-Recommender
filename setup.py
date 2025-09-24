#!/usr/bin/env python3
"""
FreshCart Setup Script

This script helps set up the FreshCart recommendation system
for local development and deployment.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_data_file():
    """Check if data file exists"""
    data_path = Path("sample_data/transactions.csv")
    if data_path.exists():
        print("✅ Data file found")
        return True
    else:
        print("❌ Data file not found: sample_data/transactions.csv")
        print("Please ensure the transaction data file exists")
        return False

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    try:
        sys.path.append('utils')
        from data_prep import DataProcessor
        from recommender import FreshCartRecommender
        from visualizations import FreshCartVisualizer
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_application():
    """Test the application components"""
    print("🧪 Testing application components...")
    try:
        sys.path.append('utils')
        from data_prep import DataProcessor
        from recommender import FreshCartRecommender
        
        # Test data loading
        dp = DataProcessor()
        dp.load_data()
        print("✅ Data loading test passed")
        
        # Test recommendation engine
        rec = FreshCartRecommender(dp)
        rec.fit()
        print("✅ Recommendation engine test passed")
        
        # Test visualizations
        from visualizations import FreshCartVisualizer
        viz = FreshCartVisualizer(dp)
        print("✅ Visualization test passed")
        
        return True
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def create_git_repo():
    """Initialize git repository if not exists"""
    if Path(".git").exists():
        print("✅ Git repository already exists")
        return True
    
    try:
        subprocess.check_call(["git", "init"])
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to initialize git: {e}")
        return False

def main():
    """Main setup function"""
    print("🛒 FreshCart Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check data file
    if not check_data_file():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Test application
    if not test_application():
        return False
    
    # Initialize git if needed
    create_git_repo()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the application: streamlit run app.py")
    print("2. For deployment, see DEPLOYMENT.md")
    print("3. For development, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
