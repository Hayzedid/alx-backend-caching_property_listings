# ALX Backend Caching Property Listings

A Django application demonstrating advanced caching strategies with PostgreSQL and Redis.

## Features

- **Property Management**: CRUD operations for property listings
- **Page-Level Caching**: 15-minute cache for property list views
- **Low-Level Caching**: 1-hour cache for property querysets
- **Cache Invalidation**: Automatic cache invalidation using Django signals
- **Cache Metrics**: Redis hit/miss ratio analysis
- **Dockerized Services**: PostgreSQL and Redis in Docker containers

## Project Structure

```
alx-backend-caching_property_listings/
├── alx_backend_caching_property_listings/
│   ├── __init__.py
│   ├── settings.py          # Django settings with PostgreSQL and Redis config
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py
├── properties/
│   ├── __init__.py         # App configuration
│   ├── apps.py             # App config with signal imports
│   ├── models.py           # Property model
│   ├── views.py            # Cached views
│   ├── urls.py             # App URL patterns
│   ├── utils.py            # Caching utilities and metrics
│   └── signals.py          # Cache invalidation signals
├── docker-compose.yml      # PostgreSQL and Redis services
├── requirements.txt        # Python dependencies
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Docker Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432
- Redis on port 6379

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Start Development Server

```bash
python manage.py runserver
```

## API Endpoints

### Property List
- **URL**: `/properties/`
- **Method**: GET
- **Caching**: Page-level cache (15 minutes) + Low-level cache (1 hour)
- **Response**: JSON list of all properties

### Cache Metrics
- **URL**: `/properties/cache-metrics/`
- **Method**: GET
- **Response**: Redis cache hit/miss statistics

## Caching Strategy

### 1. Page-Level Caching
- Uses `@cache_page(60 * 15)` decorator
- Caches entire HTTP response for 15 minutes
- Stored in Redis

### 2. Low-Level Caching
- Uses Django's cache API (`cache.get()`, `cache.set()`)
- Caches property queryset for 1 hour
- Key: `all_properties`

### 3. Cache Invalidation
- Django signals (`post_save`, `post_delete`) automatically invalidate cache
- Ensures data consistency when properties are created, updated, or deleted

### 4. Cache Metrics
- Monitors Redis keyspace hits/misses
- Calculates hit ratio percentage
- Provides insights into cache performance

## Environment Variables

Create a `.env` file for production:

```env
DEBUG=False
SECRET_KEY=your-secret-key
DB_NAME=property_listings
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/1
```

## Docker Services Configuration

### PostgreSQL
- Image: `postgres:latest`
- Port: 5432
- Database: `property_listings`
- User: `postgres`
- Password: `postgres`

### Redis
- Image: `redis:latest`
- Port: 6379
- Used for Django caching backend

## Testing the Application

1. **Create some properties** via Django admin or API
2. **Test caching** by making multiple requests to `/properties/`
3. **Check cache metrics** at `/properties/cache-metrics/`
4. **Test invalidation** by creating/updating/deleting properties

## Performance Benefits

- **Reduced Database Load**: Cached queries reduce PostgreSQL hits
- **Faster Response Times**: Redis serves cached data in microseconds
- **Automatic Invalidation**: Ensures fresh data without manual cache clearing
- **Scalability**: Supports high-traffic applications with minimal database impact

## Monitoring

Use the cache metrics endpoint to monitor:
- Cache hit ratio
- Total cache requests
- Performance optimization opportunities

## Production Considerations

- Configure Redis persistence
- Set up Redis clustering for high availability
- Monitor cache memory usage
- Implement cache warming strategies
- Use environment variables for sensitive configuration
