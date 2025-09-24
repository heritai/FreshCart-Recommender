"""
Data Preparation Utilities for FreshCart Recommendation System

This module handles data loading, preprocessing, and feature engineering
for the recommendation system.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from functools import lru_cache

class DataProcessor:
    """Handles data loading and preprocessing for the recommendation system"""
    
    def __init__(self, data_path='sample_data/transactions.csv'):
        self.data_path = data_path
        self.df = None
        self.product_categories = {
            'Pasta (500g pack)': 'Groceries & Pantry',
            'Tomato Sauce (jar)': 'Groceries & Pantry', 
            'Parmesan Cheese (grated)': 'Groceries & Pantry',
            'Rice (1kg bag)': 'Groceries & Pantry',
            'Olive Oil (1L bottle)': 'Groceries & Pantry',
            'Cereal (cornflakes box)': 'Groceries & Pantry',
            'Red Wine (bottle)': 'Beverages',
            'Mineral Water (6-pack)': 'Beverages',
            'Orange Juice (1L carton)': 'Beverages',
            'Coffee (ground, 250g pack)': 'Beverages',
            'Green Tea (box of tea bags)': 'Beverages',
            'Bananas (1kg)': 'Fresh Produce',
            'Apples (1kg)': 'Fresh Produce',
            'Tomatoes (1kg)': 'Fresh Produce',
            'Lettuce (1 head)': 'Fresh Produce',
            'Chicken Breast (500g)': 'Meat & Dairy',
            'Yogurt (4-pack)': 'Meat & Dairy',
            'Milk (1L bottle)': 'Meat & Dairy',
            'Toilet Paper (12-roll pack)': 'Household',
            'Laundry Detergent (2L bottle)': 'Household'
        }
    
    def load_data(self):
        """Load transaction data from CSV file"""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        self.df = pd.read_csv(self.data_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Add product categories
        self.df['Category'] = self.df['Product'].map(self.product_categories)
        
        print(f"Loaded {len(self.df):,} transactions from {self.df['Date'].min().date()} to {self.df['Date'].max().date()}")
        print(f"Unique customers: {self.df['CustomerID'].nunique():,}")
        print(f"Unique products: {self.df['Product'].nunique()}")
        
        return self.df
    
    def get_basket_data(self):
        """Group transactions by customer and date to create baskets"""
        if self.df is None:
            self.load_data()
        
        # Group by customer and date to create baskets
        baskets = self.df.groupby(['CustomerID', 'Date'])['Product'].apply(list).reset_index()
        baskets.columns = ['CustomerID', 'Date', 'Products']
        baskets['BasketSize'] = baskets['Products'].apply(len)
        
        return baskets
    
    def get_customer_product_matrix(self):
        """Create customer-product interaction matrix for collaborative filtering"""
        if self.df is None:
            self.load_data()
        
        # Create binary matrix (1 if customer bought product, 0 otherwise)
        matrix = self.df.groupby(['CustomerID', 'Product']).size().unstack(fill_value=0)
        matrix = (matrix > 0).astype(int)  # Convert to binary
        
        return matrix
    
    def get_product_cooccurrence_matrix(self):
        """Create product co-occurrence matrix based on baskets"""
        baskets = self.get_basket_data()
        
        # Flatten all products from all baskets
        all_products = []
        for products in baskets['Products']:
            all_products.extend(products)
        
        # Get unique products
        unique_products = list(set(all_products))
        
        # Initialize co-occurrence matrix
        cooccurrence_matrix = pd.DataFrame(0, index=unique_products, columns=unique_products)
        
        # Count co-occurrences
        for products in baskets['Products']:
            for i, product1 in enumerate(products):
                for j, product2 in enumerate(products):
                    if i != j:  # Don't count self-co-occurrence
                        cooccurrence_matrix.loc[product1, product2] += 1
        
        return cooccurrence_matrix
    
    @lru_cache(maxsize=1)
    def get_product_stats(self):
        """Get comprehensive product statistics"""
        if self.df is None:
            self.load_data()
        
        stats = self.df.groupby('Product').agg({
            'CustomerID': ['count', 'nunique'],
            'Date': ['min', 'max']
        }).round(2)
        
        stats.columns = ['TotalTransactions', 'UniqueCustomers', 'FirstPurchase', 'LastPurchase']
        stats['Category'] = stats.index.map(self.product_categories)
        stats['AvgTransactionsPerCustomer'] = (stats['TotalTransactions'] / stats['UniqueCustomers']).round(2)
        
        # Sort by total transactions
        stats = stats.sort_values('TotalTransactions', ascending=False)
        
        return stats
    
    def get_customer_stats(self):
        """Get customer-level statistics"""
        if self.df is None:
            self.load_data()
        
        customer_stats = self.df.groupby('CustomerID').agg({
            'Product': ['count', 'nunique'],
            'Date': ['min', 'max', 'nunique']
        }).round(2)
        
        customer_stats.columns = ['TotalTransactions', 'UniqueProducts', 'FirstPurchase', 'LastPurchase', 'ShoppingDays']
        customer_stats['AvgBasketSize'] = (customer_stats['TotalTransactions'] / customer_stats['ShoppingDays']).round(2)
        
        return customer_stats
    
    def get_time_series_data(self, frequency='M'):
        """Get time series data for trend analysis"""
        if self.df is None:
            self.load_data()
        
        # Group by date and product
        time_series = self.df.groupby([pd.Grouper(key='Date', freq=frequency), 'Product']).size().unstack(fill_value=0)
        
        return time_series
    
    def get_frequently_bought_together(self, min_cooccurrence=10):
        """Get products that are frequently bought together"""
        cooccurrence_matrix = self.get_product_cooccurrence_matrix()
        
        # Get pairs with minimum co-occurrence
        pairs = []
        products = cooccurrence_matrix.index
        
        for i, product1 in enumerate(products):
            for j, product2 in enumerate(products):
                if i < j:  # Avoid duplicates
                    cooccurrence = cooccurrence_matrix.loc[product1, product2]
                    if cooccurrence >= min_cooccurrence:
                        pairs.append({
                            'Product1': product1,
                            'Product2': product2,
                            'Cooccurrence': cooccurrence,
                            'Category1': self.product_categories.get(product1, 'Unknown'),
                            'Category2': self.product_categories.get(product2, 'Unknown')
                        })
        
        # Sort by co-occurrence
        pairs_df = pd.DataFrame(pairs).sort_values('Cooccurrence', ascending=False)
        
        return pairs_df
    
    @lru_cache(maxsize=1)
    def get_global_insights(self):
        """Get key performance indicators for the dashboard"""
        if self.df is None:
            self.load_data()
        
        baskets = self.get_basket_data()
        
        insights = {
            'total_transactions': len(self.df),
            'unique_customers': self.df['CustomerID'].nunique(),
            'unique_products': self.df['Product'].nunique(),
            'avg_basket_size': baskets['BasketSize'].mean(),
            'total_baskets': len(baskets),
            'date_range': f"{self.df['Date'].min().strftime('%Y-%m-%d')} to {self.df['Date'].max().strftime('%Y-%m-%d')}",
            'top_products': self.df['Product'].value_counts().head(5).to_dict(),
            'top_categories': self.df['Category'].value_counts().head(5).to_dict()
        }
        
        return insights
    
    def filter_data_by_date_range(self, start_date, end_date):
        """Filter data by date range"""
        if self.df is None:
            self.load_data()
        
        mask = (self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)
        return self.df[mask].copy()
    
    def get_customer_purchase_history(self, customer_id):
        """Get purchase history for a specific customer"""
        if self.df is None:
            self.load_data()
        
        customer_data = self.df[self.df['CustomerID'] == customer_id].copy()
        customer_data = customer_data.sort_values('Date')
        
        return customer_data
