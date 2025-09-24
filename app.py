"""
FreshCart - AI-Powered Product Recommendation System

A comprehensive dashboard for supermarket product recommendations
built with Streamlit, featuring collaborative filtering and
real-time insights.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

try:
    from data_prep import DataProcessor
    from recommender import FreshCartRecommender
    from visualizations import FreshCartVisualizer
except ImportError as e:
    st.error(f"Import error: {str(e)}")
    st.error("Please ensure all required files are present in the utils directory.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="FreshCart - Product Recommendation System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2C3E50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
        margin: 0.5rem 0;
        color: #2C3E50;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .recommendation-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #2C3E50;
    }
    .product-name {
        font-weight: bold;
        color: #2E8B57;
        font-size: 1.1rem;
    }
    .category-badge {
        background-color: #e9ecef;
        color: #495057;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        margin-left: 0.5rem;
        border: 1px solid #dee2e6;
    }
    .score-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        float: right;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache data processing components"""
    try:
        data_processor = DataProcessor()
        data_processor.load_data()
        
        recommender = FreshCartRecommender(data_processor)
        recommender.fit()
        
        visualizer = FreshCartVisualizer(data_processor)
        
        return data_processor, recommender, visualizer
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.error("Please ensure the transaction data file exists in the sample_data directory.")
        return None, None, None

@st.cache_data
def get_product_recommendations_cached(_recommender, product, method, n_recommendations):
    """Cached product recommendations"""
    return _recommender.get_product_recommendations(product, n_recommendations, method)

@st.cache_data
def get_customer_recommendations_cached(_recommender, customer_id, n_recommendations):
    """Cached customer recommendations"""
    return _recommender.get_customer_recommendations(customer_id, n_recommendations)

@st.cache_data
def get_basket_recommendations_cached(_recommender, selected_products, n_recommendations):
    """Cached basket recommendations"""
    return _recommender.get_basket_recommendations(selected_products, n_recommendations)

@st.cache_data
def get_popular_products_cached(_recommender, n_products, category=None):
    """Cached popular products"""
    if category and category != "All":
        return _recommender.get_category_recommendations(category, n_products)
    else:
        return _recommender.get_popular_products(n_products)

def display_kpi_cards(insights):
    """Display KPI cards"""
    kpis = [
        {
            'title': 'Total Transactions',
            'value': f"{insights['total_transactions']:,}",
            'icon': '📊',
            'description': 'All-time transaction count'
        },
        {
            'title': 'Unique Customers',
            'value': f"{insights['unique_customers']:,}",
            'icon': '👥',
            'description': 'Active customer base'
        },
        {
            'title': 'Unique Products',
            'value': f"{insights['unique_products']}",
            'icon': '🛒',
            'description': 'Product catalog size'
        },
        {
            'title': 'Avg Basket Size',
            'value': f"{insights['avg_basket_size']:.1f}",
            'icon': '📦',
            'description': 'Items per transaction'
        }
    ]
    
    cols = st.columns(4)
    for i, kpi in enumerate(kpis):
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card">
                <h3 style="margin: 0; color: #2E8B57;">{kpi['icon']} {kpi['value']}</h3>
                <p style="margin: 0.5rem 0 0 0; font-weight: bold;">{kpi['title']}</p>
                <p style="margin: 0; font-size: 0.9rem; color: #6c757d;">{kpi['description']}</p>
            </div>
            """, unsafe_allow_html=True)

def display_recommendation_cards(recommendations, title="Recommendations", data_processor=None):
    """Display recommendation cards"""
    if not recommendations:
        st.info("No recommendations available.")
        return
    
    st.markdown(f"<div class='sub-header'>{title}</div>", unsafe_allow_html=True)
    
    for i, rec in enumerate(recommendations[:5]):  # Show top 5
        product = rec['product']
        score = rec['score']
        method = rec['method']
        
        # Get category
        if data_processor:
            category = data_processor.product_categories.get(product, 'Unknown')
        else:
            category = 'Unknown'
        
        # Format score based on method
        if method in ['similarity', 'hybrid']:
            score_text = f"{score:.3f}"
        else:
            score_text = f"{score:.0f}"
        
        st.markdown(f"""
        <div class="recommendation-card">
            <div class="product-name">{product}</div>
            <span class="category-badge">{category}</span>
            <span class="score-badge">{score_text}</span>
            <div style="clear: both; margin-top: 0.5rem;">
                <small style="color: #6c757d;">Method: {method.title()}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Header
    st.markdown('<div class="main-header">🛒 FreshCart</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 1.2rem; color: #6c757d; margin-bottom: 2rem;">AI-Powered Product Recommendation System</div>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading FreshCart data and models..."):
        data_processor, recommender, visualizer = load_data()
    
    if data_processor is None:
        st.stop()
    
    # Get insights
    insights = data_processor.get_global_insights()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📊 Global Insights", "🔍 Recommendation Explorer", "🛒 Basket Simulation"])
    
    with tab1:
        st.markdown('<div class="sub-header">📊 Global Insights</div>', unsafe_allow_html=True)
        
        # KPI Cards
        display_kpi_cards(insights)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(visualizer.create_top_products_chart(10), use_container_width=True)
        
        with col2:
            st.plotly_chart(visualizer.create_category_distribution_chart(), use_container_width=True)
        
        # Additional charts
        st.plotly_chart(visualizer.create_basket_size_distribution(), use_container_width=True)
        
        # Network graph with improved error handling
        try:
            network_fig = visualizer.create_network_graph(15)
            # Check if the figure has any data (not just error messages)
            if network_fig.data and len(network_fig.data) > 0:
                st.plotly_chart(network_fig, use_container_width=True)
            else:
                st.warning("Network graph data not available. Showing alternative visualization.")
                # Show a simple bar chart of frequently bought together products instead
                frequently_bought = data_processor.get_frequently_bought_together(10)
                if not frequently_bought.empty:
                    fig = px.bar(
                        frequently_bought.head(10),
                        x='Cooccurrence',
                        y='Product1',
                        orientation='h',
                        title='Frequently Bought Together Products',
                        labels={'Cooccurrence': 'Times Bought Together', 'Product1': 'Product'}
                    )
                    fig.update_layout(
                        height=400,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No frequently bought together products found.")
        except Exception as e:
            st.warning(f"Network graph temporarily unavailable: {str(e)[:100]}...")
            # Show a simple bar chart of frequently bought together products instead
            try:
                frequently_bought = data_processor.get_frequently_bought_together(10)
                if not frequently_bought.empty:
                    fig = px.bar(
                        frequently_bought.head(10),
                        x='Cooccurrence',
                        y='Product1',
                        orientation='h',
                        title='Frequently Bought Together Products',
                        labels={'Cooccurrence': 'Times Bought Together', 'Product1': 'Product'}
                    )
                    fig.update_layout(
                        height=400,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No frequently bought together products found.")
            except Exception as e2:
                st.error(f"Unable to create alternative visualization: {str(e2)[:100]}...")
        
        # Co-occurrence heatmap
        st.plotly_chart(visualizer.create_cooccurrence_heatmap(10), use_container_width=True)
        
        # Monthly trends
        st.plotly_chart(visualizer.create_monthly_trends(), use_container_width=True)
        
        # Category performance
        st.plotly_chart(visualizer.create_category_performance(), use_container_width=True)
    
    with tab2:
        st.markdown('<div class="sub-header">🔍 Recommendation Explorer</div>', unsafe_allow_html=True)
        
        # Product selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Get all products
            all_products = list(data_processor.product_categories.keys())
            selected_product = st.selectbox(
                "Select a product to get recommendations:",
                all_products,
                index=0
            )
        
        with col2:
            method = st.selectbox(
                "Recommendation Method:",
                ["hybrid", "similarity", "cooccurrence"],
                index=0,
                help="Hybrid combines similarity and co-occurrence for best results"
            )
        
        # Get recommendations
        if selected_product:
            with st.spinner("Generating recommendations..."):
                recommendations = get_product_recommendations_cached(
                    recommender, selected_product, method, 5
                )
            
            # Display recommendations
            display_recommendation_cards(recommendations, f"Products similar to '{selected_product}'", data_processor)
            
            # Visualization
            if recommendations:
                st.plotly_chart(
                    visualizer.create_recommendation_visualization(
                        recommendations, 
                        f"Recommendations for {selected_product}"
                    ), 
                    use_container_width=True
                )
        
        # Customer recommendations
        st.markdown('<div class="sub-header">👤 Customer-Based Recommendations</div>', unsafe_allow_html=True)
        
        # Customer selection
        customer_ids = data_processor.df['CustomerID'].unique()
        selected_customer = st.selectbox(
            "Select a customer ID:",
            sorted(customer_ids),
            index=0
        )
        
        if selected_customer:
            with st.spinner("Generating customer recommendations..."):
                customer_recs = get_customer_recommendations_cached(recommender, selected_customer, 5)
            
            display_recommendation_cards(customer_recs, f"Recommendations for Customer {selected_customer}", data_processor)
            
            # Show customer's purchase history
            st.markdown('<div class="sub-header">📋 Purchase History</div>', unsafe_allow_html=True)
            customer_history = data_processor.get_customer_purchase_history(selected_customer)
            
            if not customer_history.empty:
                # Group by date for better display
                history_summary = customer_history.groupby('Date').agg({
                    'Product': lambda x: ', '.join(x),
                    'Category': lambda x: ', '.join(x.unique())
                }).reset_index()
                
                st.dataframe(
                    history_summary,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No purchase history found for this customer.")
    
    with tab3:
        st.markdown('<div class="sub-header">🛒 Basket Simulation</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #e7f3ff; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; color: #2C3E50;">
            <strong>💡 How it works:</strong> Select products to add to your basket, and we'll recommend complementary items 
            that customers frequently buy together with your selected products.
        </div>
        """, unsafe_allow_html=True)
        
        # Product selection for basket
        all_products = list(data_processor.product_categories.keys())
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_products = st.multiselect(
                "Add products to your basket:",
                all_products,
                default=[],
                help="Select multiple products to see recommendations"
            )
        
        with col2:
            n_recommendations = st.slider(
                "Number of recommendations:",
                min_value=3,
                max_value=10,
                value=5
            )
        
        # Display current basket
        if selected_products:
            st.markdown('<div class="sub-header">🛒 Your Current Basket</div>', unsafe_allow_html=True)
            
            for product in selected_products:
                category = data_processor.product_categories.get(product, 'Unknown')
                st.markdown(f"""
                <div class="recommendation-card">
                    <div class="product-name">{product}</div>
                    <span class="category-badge">{category}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Get basket recommendations
            with st.spinner("Analyzing your basket and generating recommendations..."):
                basket_recs = get_basket_recommendations_cached(recommender, selected_products, n_recommendations)
            
            if basket_recs:
                display_recommendation_cards(basket_recs, "🎯 Recommended for Your Basket", data_processor)
                
                # Visualization
                st.plotly_chart(
                    visualizer.create_recommendation_visualization(
                        basket_recs, 
                        "Basket-Based Recommendations"
                    ), 
                    use_container_width=True
                )
            else:
                st.info("No recommendations available for your current basket.")
        
        else:
            st.info("👆 Select products above to see recommendations!")
        
        # Popular products section
        st.markdown('<div class="sub-header">🔥 Popular Products</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            category_filter = st.selectbox(
                "Filter by category:",
                ["All"] + list(set(data_processor.product_categories.values())),
                key="popular_category"
            )
        
        with col2:
            n_popular = st.slider(
                "Number of products:",
                min_value=5,
                max_value=15,
                value=10,
                key="popular_count"
            )
        
        # Get popular products
        popular_recs = get_popular_products_cached(recommender, n_popular, category_filter)
        
        display_recommendation_cards(popular_recs, f"🔥 Most Popular Products" + (f" in {category_filter}" if category_filter != "All" else ""), data_processor)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
        <p><strong>FreshCart Recommendation System</strong> | Built with ❤️ using Streamlit, scikit-learn, and Plotly</p>
        <p><em>This demo uses synthetic data designed to mimic realistic shopping behavior patterns.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
