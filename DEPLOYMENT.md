# 🚀 FreshCart Deployment Guide

This guide will help you deploy the FreshCart recommendation system to GitHub and Streamlit Cloud.

## 📋 Prerequisites

- GitHub account
- Streamlit Cloud account (free)
- Git installed locally

## 🔧 Step 1: Prepare the Repository

### 1.1 Initialize Git Repository
```bash
cd /path/to/freshcart-recommender
git init
```

### 1.2 Add All Files
```bash
git add .
git commit -m "Initial commit: FreshCart recommendation system"
```

## 📤 Step 2: Create GitHub Repository

### 2.1 Create Repository on GitHub
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Repository name: `freshcart-recommender`
4. Description: `AI-powered product recommendation system for supermarkets`
5. Make it **Public** (required for Streamlit Cloud free tier)
6. Don't initialize with README (we already have one)
7. Click "Create repository"

### 2.2 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/freshcart-recommender.git
git branch -M main
git push -u origin main
```

## ☁️ Step 3: Deploy to Streamlit Cloud

### 3.1 Access Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"

### 3.2 Configure Deployment
- **Repository**: `YOUR_USERNAME/freshcart-recommender`
- **Branch**: `main`
- **Main file path**: `streamlit_app.py`
- **App URL**: `https://freshcart-recommender.streamlit.app`

### 3.3 Deploy
1. Click "Deploy!"
2. Wait for deployment to complete (2-3 minutes)
3. Your app will be available at the provided URL

## 🔧 Step 4: Customize Deployment (Optional)

### 4.1 Environment Variables
If you need to add environment variables:
1. Go to your app's settings in Streamlit Cloud
2. Add any required environment variables
3. Redeploy

### 4.2 Custom Domain (Pro Feature)
- Streamlit Cloud Pro allows custom domains
- Free tier uses `*.streamlit.app` domains

## 📊 Step 5: Monitor and Update

### 5.1 Monitoring
- Check app logs in Streamlit Cloud dashboard
- Monitor performance and usage
- Set up alerts if needed

### 5.2 Updates
To update your deployed app:
```bash
# Make changes to your code
git add .
git commit -m "Update: Add new features"
git push origin main
```
Streamlit Cloud will automatically redeploy!

## 🛠️ Troubleshooting

### Common Issues:

1. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check file paths in imports

2. **Data Loading Issues**
   - Verify `sample_data/transactions.csv` exists
   - Check file permissions

3. **Performance Issues**
   - Monitor memory usage in Streamlit Cloud
   - Consider optimizing data loading

4. **Deployment Failures**
   - Check Streamlit Cloud logs
   - Verify all files are committed to GitHub

## 📈 Scaling Considerations

### Free Tier Limits:
- 1 app per GitHub account
- 1GB RAM
- 1 CPU core
- 1GB storage

### Pro Tier Benefits:
- Multiple apps
- More resources
- Custom domains
- Priority support

## 🔗 Useful Links

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Actions for CI/CD](https://docs.github.com/en/actions)
- [Streamlit Best Practices](https://docs.streamlit.io/knowledge-base/tutorials/deploy)

## 📞 Support

If you encounter issues:
1. Check Streamlit Cloud logs
2. Review GitHub repository
3. Consult Streamlit documentation
4. Contact support if needed

---

**Happy Deploying! 🚀**
