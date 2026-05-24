# Vercel Deployment Guide

## Quick Start

Deploy your Signature application to Vercel - the easiest way to host Next.js and Python backends.

## Prerequisites

1. **Vercel Account** - Sign up at https://vercel.com (free, sign in with GitHub)
2. **GitHub Repository** - Already set up ✓

## Setup Instructions

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign Up"
3. Select "Continue with GitHub"
4. Authorize Vercel to access your GitHub account

### Step 2: Deploy Frontend (Next.js)

1. In Vercel Dashboard, click **"Add New..." → "Project"**
2. Select your `signature` repository
3. Set these options:
   - **Framework Preset**: Next.js
   - **Root Directory**: `./frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

4. Click **"Deploy"**

**Save your Frontend Project ID** (you'll need it later)

### Step 3: Deploy Backend (FastAPI)

1. In Vercel Dashboard, click **"Add New..." → "Project"**
2. Select your `signature` repository again
3. Set these options:
   - **Framework Preset**: Other
   - **Root Directory**: `./backend`
   - **Build Command**: Leave blank (or `pip install -r requirements.txt`)
   - **Output Directory**: `.`

4. Click **"Deploy"**

**Save your Backend Project ID**

### Step 4: Set Environment Variables

#### For Frontend Project:
In Vercel Dashboard → Your Frontend Project → Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
```

#### For Backend Project:
In Vercel Dashboard → Your Backend Project → Settings → Environment Variables:

```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
CLAUDE_API_KEY=your-claude-api-key
PAYPAL_CLIENT_ID=your-paypal-id
PAYPAL_CLIENT_SECRET=your-paypal-secret
```

### Step 5: Configure GitHub Actions (Optional Auto-Deploy)

If you want auto-deployment when you push to `main`:

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `VERCEL_TOKEN` - Get from Vercel Account Settings
   - `VERCEL_ORG_ID` - Your org ID (in Vercel Settings)
   - `VERCEL_PROJECT_ID` - Frontend Project ID
   - `VERCEL_PROJECT_ID_BACKEND` - Backend Project ID

3. GitHub Actions will now auto-deploy on every push to `main`

## Important Notes

### Database & Redis

Vercel doesn't include PostgreSQL or Redis. You have options:

**Option 1: Use External Services (Recommended)**
- **Database**: Use Vercel Postgres (integrated), Railway, or Supabase
- **Redis**: Use Upstash Redis (free tier available)

**Option 2: Keep Local**
- Keep your local `docker-compose` setup for development
- Deploy only the frontend to Vercel
- Keep backend local or on a dedicated server

### Deployment URLs

After deployment, you'll get:
- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://your-backend.vercel.app`

### Cold Starts

Free tier: Services may take 10-30 seconds on first request (normal)
Pro tier: Always-on deployments available

## Troubleshooting

### Build Fails
- Check Vercel build logs in dashboard
- Verify environment variables are set
- Ensure `requirements.txt` and `package.json` are up to date

### Frontend can't reach Backend
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check CORS settings in backend
- Test API endpoint directly in browser

### Database Connection Errors
- Verify `DATABASE_URL` is correct
- Check network/IP allowlist in database provider
- Ensure database service is running

## Local Development

```bash
# Start all services locally
make up

# View logs
make logs

# Stop services
make down
```

## Next Steps

1. ✅ Create Vercel account
2. ✅ Deploy frontend project
3. ✅ Deploy backend project
4. ✅ Set environment variables
5. ✅ Test both deployments
6. ✅ (Optional) Set up GitHub Actions auto-deploy

## Resources

- Vercel Docs: https://vercel.com/docs
- Next.js Deployment: https://nextjs.org/learn-pages-router/basics/deploying-nextjs-app
- FastAPI on Vercel: https://vercel.com/guides/using-express-with-vercel

---

**Need help?** Check Vercel's support documentation or GitHub Actions logs for deployment issues.
