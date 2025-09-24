#!/usr/bin/env python3
"""
Deployment Test Script for FreshCart

This script tests if all components work correctly
in a deployment environment.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import streamlit as st
        import pandas as pd
        import numpy as np
        import plotly.express as px
        import plotly.graph_objects as go
        import sklearn
        import networkx as nx
        import seaborn as sns
        import matplotlib
        import scipy
        print("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_file():
    """Test if data file exists and is readable"""
    try:
        data_path = "sample_data/transactions.csv"
        if not os.path.exists(data_path):
            print(f"❌ Data file not found: {data_path}")
            return False
        
        import pandas as pd
        df = pd.read_csv(data_path)
        print(f"✅ Data file loaded successfully: {len(df)} rows")
        return True
    except Exception as e:
        print(f"❌ Data file error: {e}")
        return False

def test_utils_imports():
    """Test if utils modules can be imported"""
    try:
        sys.path.append('utils')
        from data_prep import DataProcessor
        from recommender import FreshCartRecommender
        from visualizations import FreshCartVisualizer
        print("✅ Utils modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Utils import error: {e}")
        return False

def test_app_import():
    """Test if main app can be imported"""
    try:
        from app import main
        print("✅ Main app imported successfully")
        return True
    except ImportError as e:
        print(f"❌ App import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 FreshCart Deployment Test")
    print("=" * 40)
    
    tests = [
        ("Package Imports", test_imports),
        ("Data File", test_data_file),
        ("Utils Imports", test_utils_imports),
        ("App Import", test_app_import)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! App should work in deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
