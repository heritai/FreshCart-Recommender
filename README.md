# 🛒 FreshCart — AI-Powered Product Recommendation System

**FreshCart — AI-powered product recommendation system to boost sales and customer satisfaction.**

---

## 🏢 Business Context

FreshCart is a leading supermarket chain looking to enhance customer experience and increase revenue through intelligent product recommendations. 

**The Challenge:**
- Customers often purchase limited items per visit, missing cross-sell opportunities
- Manual product placement and promotion strategies are inefficient
- Lack of personalized shopping experiences leads to lower customer satisfaction

**The Solution:**
FreshCart's AI-powered recommendation engine analyzes customer behavior patterns and product relationships to suggest complementary items, increasing basket size and revenue while improving customer satisfaction.

---

## 🚀 Dashboard Features

### 📊 Global Insights
- **Key Performance Indicators**: Total transactions, customer base, product catalog size, and average basket size
- **Top Products Analysis**: Bar charts showing best-selling products across categories
- **Category Distribution**: Pie charts and performance metrics by product category
- **Basket Size Analysis**: Distribution patterns and trends in shopping behavior
- **Co-occurrence Heatmaps**: Visual representation of products frequently bought together
- **Network Graphs**: Interactive product relationship networks
- **Monthly Trends**: Time-series analysis of sales patterns
- **Category Performance**: Comparative analysis across product categories

### 🔍 Recommendation Explorer
- **Product-Based Recommendations**: Select any product to see similar or complementary items
- **Multiple Algorithms**: Choose from hybrid, similarity-based, or co-occurrence-based recommendations
- **Customer-Based Recommendations**: Personalized suggestions based on individual purchase history
- **Purchase History Viewer**: Detailed transaction history for any customer
- **Interactive Visualizations**: Dynamic charts showing recommendation scores and methods

### 🛒 Basket Simulation
- **Multi-Product Selection**: Build custom baskets and get intelligent recommendations
- **Complementary Product Suggestions**: AI-powered cross-sell recommendations
- **Popular Products Browser**: Explore trending items by category
- **Real-time Analysis**: Instant recommendations as you modify your basket
- **Category Filtering**: Focus on specific product categories

---

## 🎯 Key Benefits

- **📈 Increased Revenue**: Cross-sell recommendations boost average basket size
- **🎯 Personalized Experience**: Tailored suggestions based on individual preferences
- **📊 Data-Driven Insights**: Comprehensive analytics for business decision-making
- **⚡ Real-Time Recommendations**: Instant suggestions for optimal customer experience
- **🔄 Scalable Solution**: Handles growing customer base and product catalog

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit for interactive dashboard
- **Data Processing**: pandas, numpy for data manipulation
- **Machine Learning**: scikit-learn for collaborative filtering and similarity analysis
- **Visualizations**: Plotly, seaborn, matplotlib for interactive charts
- **Network Analysis**: NetworkX for product relationship graphs
- **Deployment**: Ready for Streamlit Cloud deployment

---

## 🚀 Live Demo

👉 **[Try FreshCart on Streamlit Cloud](https://freshcart-recommender.streamlit.app)**

*Experience the full recommendation system with interactive features and real-time insights.*

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

This demonstration uses a **synthetic dataset** carefully designed to mimic realistic shopping behavior patterns. The data includes:

- 594 unique customers with varying shopping frequencies
- 20 products across 5 categories (Groceries & Pantry, Beverages, Fresh Produce, Meat & Dairy, Household)
- 90,816 transactions over a 1-year period
- Realistic co-purchase patterns (e.g., Pasta ↔ Tomato Sauce ↔ Parmesan)
- Cross-category relationships (e.g., Wine ↔ Pasta, Coffee ↔ Cereal)
- Seasonal and behavioral variations

**Methods simplified for demo purposes** - Production implementations would include additional features like:
- Real-time data processing
- A/B testing frameworks
- Advanced deep learning models
- Customer segmentation
- Inventory optimization

---

## 👨‍💻 Developer Notes

### Prerequisites
- Python 3.10+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/freshcart-recommender.git
   cd freshcart-recommender
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard**
   Open your browser to `http://localhost:8501`

### Project Structure

```
freshcart-recommender/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── utils/                   # Core utilities
│   ├── data_prep.py         # Data processing and analysis
│   ├── recommender.py       # Recommendation algorithms
│   └── visualizations.py    # Chart and graph generation
├── sample_data/             # Synthetic transaction data
│   └── transactions.csv     # Main dataset (90K+ transactions)
└── reports/                 # Documentation and examples
    └── example_report.pdf   # Sample business report
```

### Key Components

#### Data Processing (`utils/data_prep.py`)
- Transaction data loading and preprocessing
- Customer-product interaction matrices
- Product co-occurrence analysis
- Statistical summaries and insights

#### Recommendation Engine (`utils/recommender.py`)
- **Collaborative Filtering**: Customer-based recommendations using SVD
- **Content-Based Filtering**: Product similarity using cosine similarity
- **Hybrid Approach**: Combines multiple algorithms for optimal results
- **Basket Analysis**: Multi-product recommendation logic

#### Visualizations (`utils/visualizations.py`)
- Interactive charts with Plotly
- Network graphs for product relationships
- KPI dashboards and performance metrics
- Real-time recommendation displays

### Customization

#### Adding New Products
1. Update the `PRODUCTS` dictionary in `utils/data_prep.py`
2. Add co-purchase patterns in `CO_PURCHASE_PATTERNS`
3. Regenerate the dataset or update existing data

#### Modifying Algorithms
- Edit `utils/recommender.py` to implement new recommendation methods
- Adjust similarity calculations and scoring functions
- Add new features like seasonal patterns or price sensitivity

#### Styling Changes
- Modify CSS in `app.py` for different color schemes
- Update `utils/visualizations.py` for chart styling
- Customize the Streamlit theme in `.streamlit/config.toml`

### Performance Optimization

For production deployment:
- Implement data caching with Redis
- Use database connections instead of CSV files
- Add async processing for large datasets
- Implement model versioning and A/B testing

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📊 Dataset Statistics

- **Total Transactions**: 90,816
- **Unique Customers**: 594
- **Unique Products**: 20
- **Date Range**: January 2023 - December 2023
- **Average Basket Size**: 1.8 items
- **Most Popular Product**: Laundry Detergent (8,637 transactions)
- **Top Category**: Household (17,244 transactions)

---

## 🔮 Future Enhancements

- **Real-time Recommendations**: Live data processing and instant suggestions
- **Mobile App Integration**: API endpoints for mobile applications
- **Advanced Analytics**: Customer segmentation and lifetime value analysis
- **Inventory Integration**: Stock-aware recommendations
- **Seasonal Patterns**: Time-based recommendation adjustments
- **Price Optimization**: Dynamic pricing recommendations
- **A/B Testing**: Framework for testing recommendation strategies

---

## 📞 Contact

For business inquiries or technical support:
- **Email**: contact@freshcart.com
- **LinkedIn**: [FreshCart Analytics](https://linkedin.com/company/freshcart)
- **Website**: [www.freshcart.com](https://www.freshcart.com)

---

*Built with ❤️ for the future of retail analytics*
