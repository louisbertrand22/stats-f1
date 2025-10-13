# 🚀 Deployment Guide

## Environment Variables

### Critical: USE_MOCK_DATA

**⚠️ IMPORTANT**: The Ergast F1 API has been discontinued as of end of 2024. You **MUST** use mock data in production.

The backend supports two modes:

1. **Mock Data Mode** (RECOMMENDED for production)
   - Set `USE_MOCK_DATA=true` in your environment
   - Uses curated, accurate statistics from `backend/main.py`
   - Data is accurate as of end of 2024 season
   - **Max Verstappen: 67 wins** (correct)

2. **Live API Mode** (NO LONGER WORKS)
   - Set `USE_MOCK_DATA=false` 
   - Attempts to fetch from Ergast API (discontinued)
   - Will fail or show outdated cached data
   - **Max Verstappen: 62 wins** (outdated)

### Optional: LOG_LEVEL

Control the logging verbosity of the backend:

- Set `LOG_LEVEL=INFO` (default) for production - reduces log noise
- Set `LOG_LEVEL=DEBUG` for troubleshooting - shows all logs including Redis reconnection attempts
- Set `LOG_LEVEL=WARNING` for minimal logging - only warnings and errors

**Recommended for production**: `LOG_LEVEL=INFO` to avoid hitting Railway's log rate limits.

### Railway Deployment

To configure the production deployment:

1. Go to your Railway project
2. Navigate to Backend service → Variables tab
3. Add environment variables:
   ```
   USE_MOCK_DATA=true
   LOG_LEVEL=INFO
   ```
4. Redeploy the service

### Docker Compose

Add to your `docker-compose.prod.yml`:

```yaml
services:
  backend:
    environment:
      - USE_MOCK_DATA=true
```

### Verifying the Fix

After deployment, check:
```bash
curl https://your-backend.up.railway.app/health
# Should show: "mode": "mock"

curl https://your-backend.up.railway.app/driver/verstappen/stats
# Should show: "total_wins": 67
```

## Data Accuracy

The mock data in `backend/main.py` contains career statistics accurate as of the end of the 2024 F1 season:

- Max Verstappen: 67 wins, 121 podiums, 227 races, 46 poles
- Lewis Hamilton: 105 wins, 202 podiums, 374 races, 104 poles
- And more...

This data is more accurate and reliable than attempting to use the discontinued Ergast API.
