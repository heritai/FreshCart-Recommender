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

try:
    # Import and run the main application
    from app import main
    main()
except Exception as e:
    st.error(f"Error loading application: {str(e)}")
    st.error("Please check the logs for more details.")
    st.stop()
