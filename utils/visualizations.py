"""
Visualization Utilities for FreshCart Recommendation System

This module provides various visualization functions for the dashboard
including charts, graphs, and interactive visualizations.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

class FreshCartVisualizer:
    """Handles all visualizations for the FreshCart dashboard"""
    
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.colors = {
            'primary': '#2E8B57',      # Sea Green
            'secondary': '#FF6B6B',    # Coral
            'accent': '#4ECDC4',       # Turquoise
            'background': '#F8F9FA',   # Light Gray
            'text': '#2C3E50',         # Dark Blue Gray
            'success': '#28A745',      # Green
            'warning': '#FFC107',      # Yellow
            'danger': '#DC3545'        # Red
        }
        
        # Category colors
        self.category_colors = {
            'Groceries & Pantry': '#8B4513',
            'Beverages': '#FF6347',
            'Fresh Produce': '#32CD32',
            'Meat & Dairy': '#FFB6C1',
            'Household': '#87CEEB'
        }
    
    def create_top_products_chart(self, n_products=10):
        """Create bar chart of top-selling products"""
        product_stats = self.data_processor.get_product_stats()
        top_products = product_stats.head(n_products)
        
        fig = px.bar(
            x=top_products['TotalTransactions'],
            y=top_products.index,
            orientation='h',
            title=f'Top {n_products} Products by Sales',
            labels={'x': 'Total Transactions', 'y': 'Product'},
            color=top_products['Category'],
            color_discrete_map=self.category_colors
        )
        
        fig.update_layout(
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        
        fig.update_traces(marker_line_width=0)
        
        return fig
    
    def create_category_distribution_chart(self):
        """Create pie chart of category distribution"""
        category_stats = self.data_processor.get_product_stats()
        category_counts = category_stats['Category'].value_counts()
        
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Product Distribution by Category',
            color_discrete_map=self.category_colors
        )
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        
        return fig
    
    def create_cooccurrence_heatmap(self, top_n=15):
        """Create heatmap of product co-occurrences"""
        cooccurrence_matrix = self.data_processor.get_product_cooccurrence_matrix()
        
        # Get top products by total transactions
        product_stats = self.data_processor.get_product_stats()
        top_products = product_stats.head(top_n).index.tolist()
        
        # Filter matrix to top products
        filtered_matrix = cooccurrence_matrix.loc[top_products, top_products]
        
        fig = px.imshow(
            filtered_matrix.values,
            x=filtered_matrix.columns,
            y=filtered_matrix.index,
            color_continuous_scale='Blues',
            title=f'Product Co-occurrence Heatmap (Top {top_n} Products)',
            labels=dict(x="Product", y="Product", color="Co-occurrences")
        )
        
        fig.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=10),
            title_font_size=16
        )
        
        return fig
    
    def create_network_graph(self, min_cooccurrence=20):
        """Create network graph of frequently bought together products"""
        frequently_bought_together = self.data_processor.get_frequently_bought_together(min_cooccurrence)
        
        if frequently_bought_together.empty:
            # Create empty graph if no data
            fig = go.Figure()
            fig.add_annotation(
                text="No products meet the co-occurrence threshold",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
        
        # Create network graph
        G = nx.Graph()
        
        # Add nodes and edges
        for _, row in frequently_bought_together.head(20).iterrows():
            G.add_edge(row['Product1'], row['Product2'], weight=row['Cooccurrence'])
        
        # Get positions using spring layout
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Create edge traces
        edge_x = []
        edge_y = []
        edge_info = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_info.append(f"{edge[0]} ↔ {edge[1]}<br>Co-occurrences: {G[edge[0]][edge[1]]['weight']}")
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node traces
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            
            # Color by category
            category = self.data_processor.product_categories.get(node, 'Unknown')
            node_colors.append(self.category_colors.get(category, '#CCCCCC'))
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            textfont=dict(size=10, family="Arial Black"),
            marker=dict(
                size=20,
                color=node_colors,
                line=dict(width=2, color='white')
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=f'Product Network Graph (Min Co-occurrence: {min_cooccurrence})',
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Products frequently bought together",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor='left', yanchor='bottom',
                               font=dict(size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)',
                           height=500
                       ))
        
        return fig
    
    def create_basket_size_distribution(self):
        """Create histogram of basket sizes"""
        baskets = self.data_processor.get_basket_data()
        
        fig = px.histogram(
            baskets,
            x='BasketSize',
            nbins=20,
            title='Distribution of Basket Sizes',
            labels={'BasketSize': 'Number of Items', 'count': 'Number of Baskets'},
            color_discrete_sequence=[self.colors['primary']]
        )
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        
        # Add mean line
        mean_basket_size = baskets['BasketSize'].mean()
        fig.add_vline(
            x=mean_basket_size,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {mean_basket_size:.1f}",
            annotation_position="top"
        )
        
        return fig
    
    def create_customer_activity_timeline(self, n_customers=5):
        """Create timeline of customer activity"""
        customer_stats = self.data_processor.get_customer_stats()
        top_customers = customer_stats.nlargest(n_customers, 'TotalTransactions').index
        
        timeline_data = []
        for customer_id in top_customers:
            customer_data = self.data_processor.get_customer_purchase_history(customer_id)
            for _, row in customer_data.iterrows():
                timeline_data.append({
                    'CustomerID': customer_id,
                    'Date': row['Date'],
                    'Product': row['Product'],
                    'Category': row['Category']
                })
        
        timeline_df = pd.DataFrame(timeline_data)
        
        fig = px.scatter(
            timeline_df,
            x='Date',
            y='CustomerID',
            color='Category',
            title=f'Customer Activity Timeline (Top {n_customers} Customers)',
            labels={'Date': 'Date', 'CustomerID': 'Customer ID'},
            color_discrete_map=self.category_colors
        )
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        
        return fig
    
    def create_recommendation_visualization(self, recommendations, title="Product Recommendations"):
        """Create visualization for product recommendations"""
        if not recommendations:
            fig = go.Figure()
            fig.add_annotation(
                text="No recommendations available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
        
        # Prepare data
        products = [rec['product'] for rec in recommendations]
        scores = [rec['score'] for rec in recommendations]
        methods = [rec['method'] for rec in recommendations]
        
        # Color by method
        method_colors = {
            'similarity': self.colors['primary'],
            'cooccurrence': self.colors['secondary'],
            'hybrid': self.colors['accent'],
            'collaborative': self.colors['success'],
            'popularity': self.colors['warning']
        }
        
        colors = [method_colors.get(method, self.colors['primary']) for method in methods]
        
        fig = px.bar(
            x=scores,
            y=products,
            orientation='h',
            title=title,
            labels={'x': 'Recommendation Score', 'y': 'Product'},
            color=methods,
            color_discrete_map=method_colors
        )
        
        fig.update_layout(
            height=max(300, len(products) * 40),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16,
            showlegend=True
        )
        
        fig.update_traces(marker_line_width=0)
        
        return fig
    
    def create_kpi_cards(self, insights):
        """Create KPI cards for the dashboard"""
        cards = []
        
        kpis = [
            {
                'title': 'Total Transactions',
                'value': f"{insights['total_transactions']:,}",
                'icon': '📊',
                'color': self.colors['primary']
            },
            {
                'title': 'Unique Customers',
                'value': f"{insights['unique_customers']:,}",
                'icon': '👥',
                'color': self.colors['secondary']
            },
            {
                'title': 'Unique Products',
                'value': f"{insights['unique_products']}",
                'icon': '🛒',
                'color': self.colors['accent']
            },
            {
                'title': 'Avg Basket Size',
                'value': f"{insights['avg_basket_size']:.1f}",
                'icon': '📦',
                'color': self.colors['success']
            }
        ]
        
        return kpis
    
    def create_monthly_trends(self):
        """Create monthly sales trends"""
        time_series = self.data_processor.get_time_series_data('M')
        
        # Get top 5 products
        product_stats = self.data_processor.get_product_stats()
        top_products = product_stats.head(5).index.tolist()
        
        # Filter time series to top products
        filtered_series = time_series[top_products]
        
        fig = px.line(
            filtered_series,
            title='Monthly Sales Trends (Top 5 Products)',
            labels={'value': 'Transactions', 'Date': 'Month'},
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_category_performance(self):
        """Create category performance comparison"""
        category_stats = self.data_processor.get_product_stats()
        category_performance = category_stats.groupby('Category').agg({
            'TotalTransactions': 'sum',
            'UniqueCustomers': 'sum',
            'AvgTransactionsPerCustomer': 'mean'
        }).round(2)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Total Transactions by Category', 'Avg Transactions per Customer'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Total transactions
        fig.add_trace(
            go.Bar(
                x=category_performance.index,
                y=category_performance['TotalTransactions'],
                name='Total Transactions',
                marker_color=[self.category_colors.get(cat, self.colors['primary']) for cat in category_performance.index]
            ),
            row=1, col=1
        )
        
        # Avg transactions per customer
        fig.add_trace(
            go.Bar(
                x=category_performance.index,
                y=category_performance['AvgTransactionsPerCustomer'],
                name='Avg per Customer',
                marker_color=[self.category_colors.get(cat, self.colors['secondary']) for cat in category_performance.index]
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_text="Category Performance Analysis",
            title_font_size=16,
            showlegend=False
        )
        
        return fig
