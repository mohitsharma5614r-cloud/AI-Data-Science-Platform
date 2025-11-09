# 🚀 Deployment Guide - Autonomous Data Science Agent

## ⚠️ Vercel Limitation

**Your application CANNOT be fully deployed to Vercel** due to the 250 MB serverless function size limit.

The heavy ML dependencies (scikit-learn, pandas, numpy, scipy, matplotlib, seaborn) exceed this limit when packaged together.

---

## ✅ Recommended Deployment Options

### **Option 1: Railway.app (Easiest - Recommended)**

Railway supports Docker and has no strict size limits for web services.

#### Steps:
1. Create account at [railway.app](https://railway.app)
2. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```
3. Login and deploy:
   ```bash
   railway login
   railway init
   railway up
   ```
4. Your app will be live with a URL like: `https://your-app.railway.app`

**Pros:**
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy deployment
- ✅ Supports full Python stack
- ✅ Persistent storage

---

### **Option 2: Render.com**

Render provides free web services with Docker support.

#### Steps:
1. Create account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect the `render.yaml` configuration
5. Click "Create Web Service"

**Pros:**
- ✅ Free tier (with limitations)
- ✅ Auto-deploy from Git
- ✅ Automatic HTTPS
- ✅ Easy setup

**Cons:**
- ⚠️ Free tier spins down after inactivity
- ⚠️ Limited resources on free tier

---

### **Option 3: Google Cloud Run**

Best for production with auto-scaling.

#### Steps:
1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Build and push Docker image:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ds-agent
   ```
3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy ds-agent \
     --image gcr.io/YOUR_PROJECT_ID/ds-agent \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --memory 2Gi
   ```

**Pros:**
- ✅ Auto-scaling
- ✅ Pay per use
- ✅ Production-ready
- ✅ High reliability

**Cons:**
- 💰 Costs money (but has free tier)
- 🔧 More complex setup

---

### **Option 4: AWS Elastic Beanstalk**

Good for AWS ecosystem integration.

#### Steps:
1. Install [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)
2. Initialize and deploy:
   ```bash
   eb init -p docker autonomous-ds-agent
   eb create ds-agent-env
   eb open
   ```

**Pros:**
- ✅ Integrated with AWS services
- ✅ Auto-scaling
- ✅ Load balancing

**Cons:**
- 💰 Can be expensive
- 🔧 Complex configuration

---

### **Option 5: Heroku**

Classic PaaS solution.

#### Steps:
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create `Procfile`:
   ```
   web: python web_app.py
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

**Pros:**
- ✅ Simple deployment
- ✅ Add-ons ecosystem

**Cons:**
- 💰 No free tier anymore
- ⚠️ Can be slow with heavy ML workloads

---

## 🔧 Local Development (Always Works)

The simplest option is to run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run web interface
python web_app.py

# Access at http://localhost:5000
```

**Pros:**
- ✅ No deployment complexity
- ✅ Full functionality
- ✅ No costs
- ✅ Fast processing

**Cons:**
- ⚠️ Not accessible from internet
- ⚠️ Requires your computer to be running

---

## 📊 Comparison Table

| Platform | Free Tier | Ease of Use | ML Support | Best For |
|----------|-----------|-------------|------------|----------|
| **Railway** | ✅ Yes | ⭐⭐⭐⭐⭐ | ✅ Full | **Recommended** |
| **Render** | ✅ Yes | ⭐⭐⭐⭐ | ✅ Full | Quick demos |
| **Cloud Run** | ✅ Limited | ⭐⭐⭐ | ✅ Full | Production |
| **AWS EB** | ❌ No | ⭐⭐ | ✅ Full | Enterprise |
| **Heroku** | ❌ No | ⭐⭐⭐⭐ | ✅ Full | Legacy apps |
| **Vercel** | ✅ Yes | ⭐⭐⭐⭐⭐ | ❌ Limited | Static/API only |
| **Local** | ✅ Free | ⭐⭐⭐⭐⭐ | ✅ Full | Development |

---

## 🎯 What About Vercel?

### Limited Vercel Deployment (API Only)

I've created a minimal API version that CAN run on Vercel, but it won't have ML functionality:

```bash
# Deploy to Vercel (API only)
npm install -g vercel
vercel
```

This deploys:
- ✅ Basic API endpoints
- ✅ Health checks
- ✅ Info endpoints
- ❌ No ML processing
- ❌ No file uploads
- ❌ No visualizations

**Use this only if you need a simple API gateway** and plan to process ML workloads elsewhere.

---

## 💡 Hybrid Architecture (Advanced)

For production at scale:

1. **Frontend**: Deploy static site to Vercel/Netlify
2. **API Gateway**: Lightweight API on Vercel
3. **ML Processing**: Heavy compute on Cloud Run/Railway
4. **Storage**: S3/GCS for files and results
5. **Queue**: SQS/Cloud Tasks for async processing

This separates concerns and optimizes costs.

---

## 🚀 Quick Start Recommendation

**For immediate deployment:**

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Deploy
railway up

# 5. Get your URL
railway open
```

**Done!** Your app is live in ~2 minutes.

---

## 📝 Environment Variables

For production deployments, set these:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_UPLOAD_SIZE=50  # MB
```

---

## 🔒 Security Considerations

Before deploying to production:

1. ✅ Change `SECRET_KEY` in `web_app.py`
2. ✅ Add authentication if needed
3. ✅ Set up CORS properly
4. ✅ Limit file upload sizes
5. ✅ Add rate limiting
6. ✅ Use HTTPS (automatic on most platforms)

---

## 📞 Need Help?

- Railway: [docs.railway.app](https://docs.railway.app)
- Render: [render.com/docs](https://render.com/docs)
- Cloud Run: [cloud.google.com/run/docs](https://cloud.google.com/run/docs)

---

**Bottom Line:** Use Railway or Render for easiest deployment. Vercel won't work for the full ML application.
