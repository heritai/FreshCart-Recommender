# 🛒 FreshCart: An AI-Powered Product Recommendation System

Boost sales and enhance customer satisfaction with FreshCart's intelligent product recommendation system.

---

## 🏢 Business Context

FreshCart, a leading supermarket chain, aims to significantly enhance customer experience and boost revenue through intelligent product recommendations.

**The Challenge:**
*   Customers often purchase a limited number of items per visit, missing potential cross-sell opportunities.
*   Inefficient manual product placement and promotion strategies.
*   A lack of personalized shopping experiences leads to lower customer satisfaction.

**The Solution:**
FreshCart's AI-powered recommendation engine analyzes customer behavior and product relationships to suggest complementary items. This approach effectively increases basket size, boosts revenue, and significantly enhances customer satisfaction.

---

## 🚀 Key Dashboard Features

### 📊 Global Insights
*   **Key Performance Indicators**: Displays total transactions, customer base, product catalog size, and average basket size.
*   **Top Products Analysis**: Bar charts showcasing best-selling products by category.
*   **Category Distribution**: Pie charts and performance metrics for product categories.
*   **Basket Size Analysis**: Distribution patterns and shopping behavior trends.
*   **Co-occurrence Heatmaps**: Visual representation of frequently co-purchased products.
*   **Network Graphs**: Interactive product relationship networks.
*   **Monthly Trends**: Time-series analysis of sales patterns.
*   **Category Performance**: Comparative analysis across product categories.

### 🔍 Recommendation Explorer
*   **Product-Based Recommendations**: Select any product to discover similar or complementary items.
*   **Multiple Algorithms**: Choose from hybrid, similarity-based, or co-occurrence-based recommendation strategies.
*   **Customer-Based Recommendations**: Personalized suggestions derived from individual purchase history.
*   **Purchase History Viewer**: Detailed transaction history for any customer.
*   **Interactive Visualizations**: Dynamic charts illustrating recommendation scores and methodologies.

### 🛒 Basket Simulation
*   **Multi-Product Selection**: Build custom baskets to receive intelligent recommendations.
*   **Complementary Product Suggestions**: AI-powered cross-sell recommendations.
*   **Popular Products Browser**: Explore trending items within categories.
*   **Real-time Analysis**: Instant recommendations as the basket is modified.
*   **Category Filtering**: Focus recommendations on specific categories.

---

## 🎯 Key Benefits

*   **📈 Increased Revenue**: Boosts average basket size via targeted cross-sell recommendations.
*   **🎯 Personalized Experience**: Delivers tailored suggestions based on individual preferences.
*   **📊 Data-Driven Insights**: Provides comprehensive analytics for informed business decisions.
*   **⚡ Real-Time Recommendations**: Offers instant suggestions for an optimized customer experience.
*   **🔄 Scalable Solution**: Designed to handle growing customer bases and product catalogs.

---

## 🛠️ Technology Stack

The FreshCart system leverages a robust and modern technology stack to deliver high performance and interactivity:

*   **Frontend**: [Streamlit](https://streamlit.io/) for the interactive dashboard.
*   **Data Processing**: [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) for efficient data manipulation.
*   **Machine Learning**: [scikit-learn](https://scikit-learn.org/) for collaborative filtering and similarity analysis.
*   **Visualizations**: [Plotly](https://plotly.com/), [seaborn](https://seaborn.pydata.org/), [matplotlib](https://matplotlib.org/) for rich, interactive charts.
*   **Network Analysis**: [NetworkX](https://networkx.org/) for product relationship graph generation.
*   **Deployment**: Configured for [Streamlit Cloud](https://streamlit.io/cloud) deployment.

---

## 🚀 Live Demo

👉 **[Try FreshCart on Streamlit Cloud](https://freshcart-recommender.streamlit.app)**

Explore the full recommendation system with interactive features and real-time insights.

---

## 📸 Screenshots

### Global Insights Dashboard
![Global Insights](reports/global_insights.png)
*Comprehensive overview of sales performance, product popularity, and customer behavior patterns.*

### Recommendation Explorer
![Recommendation Explorer](reports/recommendation_explorer.png)
*Interactive product recommendations with multiple algorithms and customer-specific suggestions.*

### Basket Simulation
![Basket Simulation](reports/basket_simulation.png)
*Real-time basket analysis with intelligent cross-sell recommendations.*

---

## ⚠️ Disclaimer

This demonstration utilizes a **synthetic dataset**, carefully designed to mimic realistic shopping behavior patterns and provide a robust testing environment.

Key characteristics of the synthetic data include:

*   594 unique customers with varying shopping frequencies
*   20 products across 5 categories (Groceries & Pantry, Beverages, Fresh Produce, Meat & Dairy, Household)
*   90,816 transactions over a 1-year period
*   Realistic co-purchase patterns (e.g., Pasta ↔ Tomato Sauce ↔ Parmesan)
*   Cross-category relationships (e.g., Wine ↔ Pasta, Coffee ↔ Cereal)
*   Seasonal and behavioral variations

For demonstration purposes, certain methods are simplified. A production-ready implementation would incorporate advanced features such as:
*   Robust real-time data processing
*   A/B testing frameworks
*   Advanced machine learning and deep learning models
*   Customer segmentation
*   Inventory optimization

---

## 👨‍💻 Developer Notes

### Prerequisites
*   Python 3.10 or higher
*   `pip` package manager

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/freshcart-recommender.git
    cd freshcart-recommender
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    streamlit run app.py
    ```

4.  **Access the dashboard**
    Open your browser to `http://localhost:8501`

### Project Structure

The project is organized as follows:

```
freshcart-recommender/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── utils/                    # Core utilities
│   ├── data_prep.py          # Data processing and analysis
│   ├── recommender.py        # Recommendation algorithms
│   └── visualizations.py     # Chart and graph generation
├── sample_data/              # Synthetic transaction data
│   └── transactions.csv      # Main dataset (90K+ transactions)
└── reports/                  # Documentation and examples
    └── example_report.pdf    # Sample business report
```

### Key Components

*   **Data Processing (`utils/data_prep.py`)**: Handles transaction data loading, preprocessing, customer-product interaction matrices, product co-occurrence analysis, and statistical summaries.
*   **Recommendation Engine (`utils/recommender.py`)**: Implements various recommendation algorithms including collaborative filtering (SVD), content-based filtering (cosine similarity), and a hybrid approach. Also includes logic for multi-product basket analysis.
*   **Visualizations (`utils/visualizations.py`)**: Generates interactive charts with Plotly, network graphs for product relationships, KPI dashboards, and real-time recommendation displays.

### Customization

#### Adding New Products
1.  Update the `PRODUCTS` dictionary within `utils/data_prep.py`.
2.  Add or modify co-purchase patterns in `CO_PURCHASE_PATTERNS`.
3.  Regenerate the synthetic dataset as needed.

#### Modifying Algorithms
*   Edit `utils/recommender.py` to implement new recommendation methods.
*   Adjust similarity calculations and scoring functions.
*   Add new features like seasonal patterns or price sensitivity.

#### Styling Changes
*   Modify CSS styling directly in `app.py` for different color schemes.
*   Update `utils/visualizations.py` for chart styling.
*   Customize the Streamlit theme via `.streamlit/config.toml`.

### Performance Optimization

For production deployment, consider:
*   Implementing data caching (e.g., with Redis).
*   Using database connections instead of CSV files for data storage.
*   Adding async processing for large datasets.
*   Implementing model versioning and A/B testing frameworks.

### Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

---

## 📊 Dataset Statistics

Summary of the Synthetic Dataset Statistics:

*   **Total Transactions**: 90,816
*   **Unique Customers**: 594
*   **Unique Products**: 20
*   **Date Range**: January 2023 - December 2023
*   **Average Basket Size**: 1.8 items per basket
*   **Most Popular Product**: Laundry Detergent (8,637 occurrences)
*   **Top Category**: Household (17,244 transactions)

---

## 🔮 Future Enhancements

*   **Real-time Recommendations**: Implement live data processing for instant, dynamic suggestions.
*   **Mobile App Integration**: Develop robust API endpoints for seamless integration with mobile applications.
*   **Advanced Analytics**: Incorporate deeper customer segmentation and lifetime value (LTV) analysis.
*   **Inventory Integration**: Provide stock-aware recommendations to optimize inventory management.
*   **Seasonal Patterns**: Incorporate time-based and seasonal adjustments for more relevant recommendations.
*   **Price Optimization**: Explore dynamic pricing recommendations based on demand and inventory.
*   **A/B Testing**: Framework for systematically testing and evaluating recommendation strategies.

---

## 📞 Contact

For business inquiries or technical support:
*   **Email**: contact@freshcart.com
*   **LinkedIn**: [FreshCart Analytics](https://linkedin.com/company/freshcart)
*   **Website**: [www.freshcart.com](https://www.freshcart.com)

---

*Built with ❤️ for the future of retail analytics*