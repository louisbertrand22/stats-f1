# 🗄️ Cache Implementation

## Overview

The F1 Dashboard API implements a **two-tier caching system** to minimize API calls and improve performance:

1. **Redis Cache (Primary)** - Persistent cache shared across instances
2. **In-Memory Cache (Fallback)** - Local cache when Redis is unavailable

## Architecture

```
Request → Check Redis → Check Memory Cache → Fetch from API → Store in both caches
```

### Cache Strategy

- **Redis First**: If Redis is available, it's checked first for cached data
- **Memory Fallback**: If Redis is unavailable or fails, in-memory cache is used
- **Graceful Degradation**: If both caches miss, data is fetched fresh from the API
- **Dual Storage**: Fresh data is stored in both Redis and memory for redundancy

## Features

### ✅ In-Memory Cache

- **TTL Support**: Automatic expiration of cached entries
- **Thread-Safe**: Uses asyncio locks for concurrent access
- **Statistics Tracking**: Monitors hits, misses, and hit rate
- **No External Dependencies**: Works even when Redis is unavailable

### ✅ Redis Cache

- **Persistent Storage**: Survives application restarts
- **Shared Across Instances**: Multiple backend instances share the same cache
- **Error Handling**: Gracefully handles connection failures

## Cache TTLs

Different endpoints have different cache durations based on data volatility:

| Endpoint | TTL | Reason |
|----------|-----|--------|
| `/drivers/current` | 24h (86400s) | Driver lineup rarely changes mid-season |
| `/constructors/current` | 24h (86400s) | Constructor list rarely changes |
| `/standings/drivers` | 1h (3600s) | Updates after each race |
| `/standings/constructors` | 1h (3600s) | Updates after each race |
| `/schedule/current` | 24h (86400s) | Schedule rarely changes |
| `/race/last` | 30m (1800s) | Recent race results |
| `/race/{season}/{round}` | 24h (86400s) | Historical data doesn't change |
| `/drivers/stats` | 24h (86400s) | Career statistics update infrequently |
| `/driver/{id}/stats` | 24h (86400s) | Career statistics update infrequently |

## Monitoring

### Cache Statistics Endpoint

Access cache statistics at `/cache/stats`:

```json
{
  "redis": {
    "status": "connected",
    "hits": 150,
    "misses": 25,
    "hit_rate": "85.71%"
  },
  "memory": {
    "entries": 12,
    "hits": 89,
    "misses": 23,
    "hit_rate": "79.46%"
  }
}
```

### Key Metrics

- **entries**: Number of items currently cached
- **hits**: Number of cache hits (data found in cache)
- **misses**: Number of cache misses (data not in cache)
- **hit_rate**: Percentage of requests served from cache

## Configuration

### Environment Variables

```bash
# Redis Configuration
REDIS_HOST=redis          # Redis server hostname
REDIS_PORT=6379          # Redis server port

# Mock Data Mode (bypasses cache)
USE_MOCK_DATA=true       # Use mock data instead of API calls
```

### When Mock Mode is Enabled

When `USE_MOCK_DATA=true`, the application returns mock data directly without using the cache. This is by design because:
- Mock data is already fast (no network calls)
- No need for caching layer overhead
- Useful for development and testing

## Implementation Details

### InMemoryCache Class

Located in `backend/main.py`, the `InMemoryCache` class provides:

```python
class InMemoryCache:
    async def get(key: str) -> Optional[any]
    async def set(key: str, value: any, ttl: int)
    async def clear()
    def get_stats() -> dict
```

### get_cached_data Function

The `get_cached_data()` function implements the caching strategy:

```python
async def get_cached_data(key: str, fetch_function, ttl: int = 3600):
    # 1. Try Redis cache
    if redis_client:
        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)
    
    # 2. Try memory cache
    cached = await memory_cache.get(key)
    if cached is not None:
        return cached
    
    # 3. Fetch fresh data
    data = await fetch_function()
    
    # 4. Store in both caches
    if redis_client and data is not None:
        redis_client.setex(key, ttl, json.dumps(data))
    
    if data is not None:
        await memory_cache.set(key, data, ttl)
    
    return data
```

## Benefits

1. **Reduced API Load**: Fewer calls to external APIs (Ergast F1 API)
2. **Better Performance**: Faster response times from cached data
3. **High Availability**: Works even when Redis is down (memory fallback)
4. **Cost Savings**: Reduced bandwidth and API quota usage
5. **Improved UX**: Faster page loads for users

## Testing

Run cache tests with:

```bash
cd backend
pytest tests/test_api.py::test_cache_stats -v
pytest tests/test_api.py::test_cache_functionality -v
```

## Future Improvements

Potential enhancements:
- [ ] Cache warming on startup
- [ ] Cache invalidation API endpoint
- [ ] Configurable TTL per endpoint via environment variables
- [ ] Cache size limits for memory cache
- [ ] Distributed cache with Redis Cluster
- [ ] Cache metrics export to monitoring systems (Prometheus, etc.)
