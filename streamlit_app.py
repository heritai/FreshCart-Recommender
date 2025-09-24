"""
FreshCart - AI-Powered Product Recommendation System

Streamlit Cloud deployment entry point.
This file is used by Streamlit Cloud to run the application.
"""

import streamlit as st
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import and run the main application
from app import main

if __name__ == "__main__":
    main()
