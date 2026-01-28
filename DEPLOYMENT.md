# Rose Glass Platform - Vercel Deployment Guide

This guide covers deploying Rose Glass Platform to Vercel with PostgreSQL database support.

## Architecture Overview

The Rose Glass Platform uses an **adaptive database strategy**:
- **Local Development**: SQLite (automatic, no configuration)
- **Production/Vercel**: PostgreSQL (via DATABASE_URL environment variable)

The system automatically detects the environment and switches database backends accordingly via `src/db_adapter.py`.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your Rose Glass Platform code should be in a GitHub repository
3. **Vercel CLI** (optional but recommended):
   ```bash
   npm install -g vercel
   ```

## Step 1: Install Vercel CLI and Login

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to your Vercel account
vercel login
```

## Step 2: Configure Vercel Postgres

### Option A: Using Vercel Dashboard

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Navigate to **Storage** → **Create Database** → **Postgres**
3. Follow the setup wizard to create your database
4. Copy the `DATABASE_URL` connection string

### Option B: Using Vercel CLI

```bash
# Navigate to your project directory
cd /path/to/rose-glass-platform

# Create a Postgres database
vercel postgres create

# Note the DATABASE_URL from the output
```

## Step 3: Set Environment Variables

### Using Vercel Dashboard

1. Go to your project in Vercel
2. Navigate to **Settings** → **Environment Variables**
3. Add the following variables:

| Variable | Value | Environment |
|----------|-------|-------------|
| `DATABASE_URL` | `postgres://...` | Production, Preview, Development |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Production, Preview, Development |
| `OPENAI_API_KEY` | Your OpenAI API key | Production, Preview, Development |

### Using Vercel CLI

```bash
# Set DATABASE_URL
vercel env add DATABASE_URL production
# Paste your postgres://... connection string when prompted

# Set ANTHROPIC_API_KEY
vercel env add ANTHROPIC_API_KEY production
# Paste your key when prompted

# Set OPENAI_API_KEY
vercel env add OPENAI_API_KEY production
# Paste your key when prompted

# Repeat for preview and development environments if needed
vercel env add DATABASE_URL preview
vercel env add DATABASE_URL development
```

## Step 4: Deploy to Vercel

### Option A: Deploy via GitHub Integration (Recommended)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure the project:
   - **Framework Preset**: Other
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
   - **Install Command**: `pip install -r requirements.txt`
4. Click **Deploy**

Vercel will automatically detect `vercel.json` and deploy accordingly.

### Option B: Deploy via CLI

```bash
# Navigate to project directory
cd /path/to/rose-glass-platform

# Deploy to production
vercel --prod

# Or deploy to preview environment
vercel
```

## Step 5: Verify Deployment

Once deployed, Vercel will provide a URL (e.g., `https://rose-glass-platform.vercel.app`).

### Test the API

```bash
# Health check
curl https://your-deployment-url.vercel.app/health

# List available lenses
curl https://your-deployment-url.vercel.app/v1/lenses

# Test perception endpoint
curl https://your-deployment-url.vercel.app/v1/perceive \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I feel overwhelmed and disconnected.",
    "lens": "trauma_informed"
  }'

# Test chat completions
curl https://your-deployment-url.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key_here" \
  -d '{
    "model": "claude-sonnet-4",
    "messages": [
      {"role": "user", "content": "How are you today?"}
    ],
    "lens": "modern_western"
  }'
```

## Database Initialization

The PostgreSQL database tables are automatically created on first request via `src/db_postgres.py:_init_tables()`. The initialization creates:

- `conversations` - Conversation metadata
- `exchanges` - Individual message exchanges
- `perception_timeseries` - Dimensional perception tracking

No manual database setup is required.

## Project Structure for Vercel

```
rose-glass-platform/
├── api/
│   └── index.py              # Vercel serverless entry point
├── src/
│   ├── server.py             # FastAPI application
│   ├── rose_lens.py          # Perception engine
│   ├── calibrator.py         # Response calibration
│   ├── db_adapter.py         # Database adapter (NEW)
│   ├── db.py                 # SQLite implementation
│   └── db_postgres.py        # PostgreSQL implementation (NEW)
├── ui/
│   └── index.html            # Frontend UI
├── vercel.json               # Vercel configuration (NEW)
├── requirements.txt          # Python dependencies (updated)
├── .env.example              # Environment template (updated)
└── README.md
```

## Monitoring and Logs

### View Deployment Logs

```bash
# Using Vercel CLI
vercel logs

# Or view in Vercel Dashboard
# Go to your project → Deployments → [Select deployment] → Logs
```

### View Database Queries

```bash
# Using Vercel CLI
vercel postgres logs
```

## Troubleshooting

### Issue: "DATABASE_URL environment variable is required"

**Solution**: Ensure `DATABASE_URL` is set in Vercel environment variables for all environments (production, preview, development).

```bash
vercel env ls  # List all environment variables
```

### Issue: Database connection errors

**Solution**: Verify your DATABASE_URL format:
- Vercel Postgres: `postgres://default:password@host.vercel-storage.com:5432/verceldb`
- External Postgres: `postgresql://user:password@host:5432/database`

### Issue: Import errors or module not found

**Solution**: Ensure all dependencies are in `requirements.txt`:
```bash
cat requirements.txt | grep psycopg2-binary
```

### Issue: Cold starts taking too long

**Solution**: Vercel serverless functions have cold start latency. Consider:
1. Optimizing imports in `api/index.py`
2. Using Vercel's Pro plan for faster cold starts
3. Implementing connection pooling for database

## Local Development vs Production

### Local Development (SQLite)
```bash
# No DATABASE_URL needed
cd rose-glass-platform
./start.sh

# Server runs on localhost:8420
# Uses SQLite database at ./rose_glass.db
```

### Production (PostgreSQL)
```bash
# DATABASE_URL is set in Vercel
# Automatically uses PostgreSQL
# Deployed to https://your-app.vercel.app
```

The adapter in `src/db_adapter.py` handles switching automatically:
```python
if DATABASE_URL and not DATABASE_URL.startswith("sqlite"):
    from src.db_postgres import get_db, init_db, RoseGlassDB
else:
    from src.db import get_db, init_db, RoseGlassDB
```

## Security Considerations

1. **API Keys**: Never commit `.env` file. Use Vercel environment variables.
2. **Database Access**: Restrict PostgreSQL access to Vercel IP ranges if possible.
3. **CORS**: Current configuration allows all origins (`allow_origins=["*"]`). In production, restrict to your frontend domains.
4. **Rate Limiting**: Consider implementing rate limiting for production use.

## Updating Deployment

```bash
# Push changes to GitHub
git add .
git commit -m "Your changes"
git push origin main

# Vercel automatically redeploys on push to main branch
```

Or manually trigger redeployment:
```bash
vercel --prod
```

## Custom Domain

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain (e.g., `api.roseglass.ai`)
3. Update DNS records as instructed by Vercel
4. Update CORS settings in `src/server.py` if needed

## Cost Considerations

- **Vercel Hobby Plan**: Free tier includes:
  - 100GB bandwidth/month
  - Serverless function execution
  - Limited build minutes

- **Vercel Postgres**:
  - Free tier: 256MB storage, 60 hours compute/month
  - Pro tier: 512MB+ storage, unlimited compute

- **LLM API Costs**:
  - Anthropic/OpenAI charges apply per token
  - Monitor usage in respective dashboards

## Support and Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Postgres Documentation](https://vercel.com/docs/storage/vercel-postgres)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/vercel/)
- [Rose Glass GitHub Issues](https://github.com/GreatPyreneseDad/rose-glass-platform/issues)

---

**Next Steps**: After deployment, test all endpoints and monitor logs for any issues. The platform is production-ready once all API tests pass.
