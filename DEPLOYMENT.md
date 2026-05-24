# Deployment Guide - Render.com

## Quick Start

This application is configured to deploy automatically to Render.com using GitHub Actions.

## Prerequisites

1. **Render.com Account** - Sign up at https://render.com (free tier available)
2. **GitHub Repository** - Already set up ✓

## Setup Instructions

### Step 1: Create Render Account & Services

1. Go to https://render.com and sign up
2. Connect your GitHub account
3. Create a new Blueprint/Web Service from this repository

### Step 2: Set Environment Variables

In Render Dashboard, set these secrets for the backend service:

```
DATABASE_URL=postgresql://user:password@hostname/dbname
REDIS_URL=redis://hostname:6379/0
CELERY_BROKER_URL=redis://hostname:6379/0
CELERY_RESULT_BACKEND=redis://hostname:6379/1
CLAUDE_API_KEY=your-api-key-here
PAYPAL_CLIENT_ID=your-paypal-id
PAYPAL_CLIENT_SECRET=your-paypal-secret
```

### Step 3: Configure GitHub Actions

1. Go to your GitHub repository Settings → Secrets and variables → Actions
2. Add these secrets:
   - `RENDER_SERVICE_ID` - Your Render service ID (found in Render dashboard URL)
   - `RENDER_API_KEY` - Generate from Render account settings

### Step 4: Deploy

Everytime you push to `main` branch:
```bash
git push origin main
```

GitHub Actions will automatically trigger a deployment to Render.

## Local Development

```bash
# Start all services
make up

# View logs
make logs

# Stop services
make down
```

## Monitoring

- **Render Dashboard**: Monitor deployments and logs at https://dashboard.render.com
- **GitHub Actions**: Check deployment status in repository → Actions tab

## Free Tier Limitations

- Services spin down after 15 minutes of inactivity
- Database has 100MB limit
- Perfect for development/testing

## Upgrade to Paid (Optional)

When ready for production:
1. Select paid plan in Render dashboard
2. Services will remain active 24/7
3. Increased resource limits

## Troubleshooting

### Services not connecting
- Verify environment variables are set correctly
- Check Render logs in dashboard
- Ensure database is running

### Deployment fails
- Check GitHub Actions logs
- Verify `render.yaml` configuration
- Check Render API key validity

### Cold starts (free tier)
- Normal behavior - services pause after inactivity
- First request will take 30-60 seconds
- Upgrade to paid to prevent this

## Next Steps

1. Create Render account at render.com
2. Connect GitHub repository
3. Set environment variables
4. Push code to main branch
5. Monitor deployment in Render dashboard

For detailed Render documentation: https://docs.render.com
