"""
Recommendation Engine for FreshCart

This module implements various recommendation algorithms including
collaborative filtering, content-based filtering, and hybrid approaches.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix
import warnings
warnings.filterwarnings('ignore')

class FreshCartRecommender:
    """Main recommendation engine for FreshCart"""
    
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.customer_product_matrix = None
        self.product_cooccurrence_matrix = None
        self.product_similarity_matrix = None
        self.customer_similarity_matrix = None
        self.svd_model = None
        self.scaler = StandardScaler()
        
    def fit(self):
        """Fit the recommendation models"""
        print("Fitting recommendation models...")
        
        # Get matrices
        self.customer_product_matrix = self.data_processor.get_customer_product_matrix()
        self.product_cooccurrence_matrix = self.data_processor.get_product_cooccurrence_matrix()
        
        # Calculate similarity matrices
        self._calculate_product_similarity()
        self._calculate_customer_similarity()
        
        # Fit SVD for collaborative filtering
        self._fit_svd_model()
        
        print("Models fitted successfully!")
    
    def _calculate_product_similarity(self):
        """Calculate product similarity based on co-occurrence"""
        # Normalize co-occurrence matrix by product popularity
        product_counts = self.product_cooccurrence_matrix.sum(axis=1)
        normalized_matrix = self.product_cooccurrence_matrix.div(product_counts, axis=0)
        
        # Calculate cosine similarity
        self.product_similarity_matrix = pd.DataFrame(
            cosine_similarity(normalized_matrix),
            index=normalized_matrix.index,
            columns=normalized_matrix.index
        )
    
    def _calculate_customer_similarity(self):
        """Calculate customer similarity based on purchase patterns"""
        # Calculate cosine similarity between customers
        self.customer_similarity_matrix = pd.DataFrame(
            cosine_similarity(self.customer_product_matrix),
            index=self.customer_product_matrix.index,
            columns=self.customer_product_matrix.index
        )
    
    def _fit_svd_model(self):
        """Fit SVD model for collaborative filtering"""
        # Convert to sparse matrix for efficiency
        sparse_matrix = csr_matrix(self.customer_product_matrix.values)
        
        # Fit SVD with components <= number of products
        n_components = min(15, sparse_matrix.shape[1] - 1)  # Use 15 or fewer components
        self.svd_model = TruncatedSVD(n_components=n_components, random_state=42)
        self.svd_model.fit(sparse_matrix)
    
    def get_product_recommendations(self, product, n_recommendations=5, method='hybrid'):
        """
        Get product recommendations based on a given product
        
        Args:
            product: Product name
            n_recommendations: Number of recommendations to return
            method: 'similarity', 'cooccurrence', or 'hybrid'
        """
        if product not in self.product_similarity_matrix.index:
            return []
        
        if method == 'similarity':
            recommendations = self._get_similarity_recommendations(product, n_recommendations)
        elif method == 'cooccurrence':
            recommendations = self._get_cooccurrence_recommendations(product, n_recommendations)
        else:  # hybrid
            recommendations = self._get_hybrid_recommendations(product, n_recommendations)
        
        return recommendations
    
    def _get_similarity_recommendations(self, product, n_recommendations):
        """Get recommendations based on product similarity"""
        similarities = self.product_similarity_matrix[product].sort_values(ascending=False)
        # Exclude the product itself
        similarities = similarities.drop(product)
        
        recommendations = []
        for similar_product, similarity in similarities.head(n_recommendations).items():
            recommendations.append({
                'product': similar_product,
                'score': similarity,
                'method': 'similarity'
            })
        
        return recommendations
    
    def _get_cooccurrence_recommendations(self, product, n_recommendations):
        """Get recommendations based on co-occurrence frequency"""
        cooccurrences = self.product_cooccurrence_matrix[product].sort_values(ascending=False)
        # Exclude the product itself
        cooccurrences = cooccurrences.drop(product)
        
        recommendations = []
        for co_product, count in cooccurrences.head(n_recommendations).items():
            if count > 0:
                recommendations.append({
                    'product': co_product,
                    'score': count,
                    'method': 'cooccurrence'
                })
        
        return recommendations
    
    def _get_hybrid_recommendations(self, product, n_recommendations):
        """Get hybrid recommendations combining similarity and co-occurrence - optimized version"""
        # Use only co-occurrence for faster performance in deployment
        co_recs = self._get_cooccurrence_recommendations(product, n_recommendations * 2)
        
        # If we have enough co-occurrence recommendations, use them
        if len(co_recs) >= n_recommendations:
            return co_recs[:n_recommendations]
        
        # Otherwise, get some similarity recommendations to fill the gap
        sim_recs = self._get_similarity_recommendations(product, n_recommendations)
        
        # Combine and deduplicate
        all_recs = {}
        for rec in co_recs + sim_recs:
            if rec['product'] not in all_recs:
                all_recs[rec['product']] = rec
        
        # Return top recommendations
        recommendations = list(all_recs.values())[:n_recommendations]
        
        # Update method to hybrid
        for rec in recommendations:
            rec['method'] = 'hybrid'
        
        return recommendations
    
    def get_customer_recommendations(self, customer_id, n_recommendations=5):
        """Get recommendations for a specific customer using collaborative filtering - optimized"""
        if customer_id not in self.customer_product_matrix.index:
            return []
        
        # Get customer's purchase history
        customer_products = set(self.customer_product_matrix.loc[customer_id][
            self.customer_product_matrix.loc[customer_id] == 1
        ].index)
        
        # Use only top 5 similar customers for faster performance
        customer_similarities = self.customer_similarity_matrix[customer_id].sort_values(ascending=False)
        customer_similarities = customer_similarities.drop(customer_id).head(5)
        
        # Get products from similar customers more efficiently
        product_scores = {}
        for similar_customer, similarity in customer_similarities.items():
            # Skip very dissimilar customers
            if similarity < 0.2:
                continue
                
            similar_products = set(self.customer_product_matrix.loc[similar_customer][
                self.customer_product_matrix.loc[similar_customer] == 1
            ].index)
            
            # Score products based on similarity
            for product in similar_products:
                if product not in customer_products:  # Don't recommend already purchased
                    if product not in product_scores:
                        product_scores[product] = 0
                    product_scores[product] += similarity
        
        # If no collaborative recommendations, fall back to popular products
        if not product_scores:
            return self.get_popular_products(n_recommendations)
        
        # Sort and return top recommendations
        sorted_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for product, score in sorted_products[:n_recommendations]:
            recommendations.append({
                'product': product,
                'score': score,
                'method': 'collaborative'
            })
        
        return recommendations
    
    def get_basket_recommendations(self, basket_products, n_recommendations=5):
        """Get recommendations for a basket of products - optimized version"""
        if not basket_products:
            return []
        
        # Limit basket size for performance (max 3 products)
        basket_products = basket_products[:3]
        
        # Get recommendations for each product in basket
        all_recommendations = {}
        
        for product in basket_products:
            if product in self.product_cooccurrence_matrix.index:
                # Use direct co-occurrence lookup for faster performance
                cooccurrences = self.product_cooccurrence_matrix[product].sort_values(ascending=False)
                cooccurrences = cooccurrences.drop(product)  # Remove self
                
                # Add top co-occurring products
                for co_product, score in cooccurrences.head(5).items():
                    if co_product not in basket_products:  # Don't recommend products already in basket
                        if co_product not in all_recommendations:
                            all_recommendations[co_product] = 0
                        all_recommendations[co_product] += score
        
        # If no recommendations found, return popular products
        if not all_recommendations:
            return self.get_popular_products(n_recommendations)
        
        # Sort by combined score
        sorted_products = sorted(all_recommendations.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for product, score in sorted_products[:n_recommendations]:
            recommendations.append({
                'product': product,
                'score': score,
                'method': 'basket_hybrid'
            })
        
        return recommendations
    
    def get_popular_products(self, n_products=10, category=None):
        """Get most popular products, optionally filtered by category"""
        product_stats = self.data_processor.get_product_stats()
        
        if category:
            product_stats = product_stats[product_stats['Category'] == category]
        
        popular_products = product_stats.head(n_products)
        
        recommendations = []
        for product, stats in popular_products.iterrows():
            recommendations.append({
                'product': product,
                'score': stats['TotalTransactions'],
                'method': 'popularity'
            })
        
        return recommendations
    
    def get_category_recommendations(self, category, n_recommendations=5):
        """Get recommendations within a specific category"""
        product_stats = self.data_processor.get_product_stats()
        category_products = product_stats[product_stats['Category'] == category]
        
        recommendations = []
        for product, stats in category_products.head(n_recommendations).iterrows():
            recommendations.append({
                'product': product,
                'score': stats['TotalTransactions'],
                'method': 'category_popularity'
            })
        
        return recommendations
    
    def explain_recommendation(self, product, recommended_product):
        """Provide explanation for why a product was recommended"""
        explanations = []
        
        # Check co-occurrence
        if product in self.product_cooccurrence_matrix.index and recommended_product in self.product_cooccurrence_matrix.columns:
            cooccurrence = self.product_cooccurrence_matrix.loc[product, recommended_product]
            if cooccurrence > 0:
                explanations.append(f"Frequently bought together ({cooccurrence} times)")
        
        # Check similarity
        if product in self.product_similarity_matrix.index and recommended_product in self.product_similarity_matrix.columns:
            similarity = self.product_similarity_matrix.loc[product, recommended_product]
            if similarity > 0.3:
                explanations.append(f"Similar purchase patterns (similarity: {similarity:.2f})")
        
        # Check category
        categories = self.data_processor.product_categories
        if categories.get(product) == categories.get(recommended_product):
            explanations.append(f"Same category: {categories.get(product)}")
        
        return explanations if explanations else ["Based on general popularity"]
