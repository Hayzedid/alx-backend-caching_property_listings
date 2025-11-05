from django.core.cache import cache
from django.conf import settings
from .models import Property
import logging

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Get all properties from cache or database.
    Cache the queryset in Redis for 1 hour using Django's low-level cache API.
    """
    cache_key = 'all_properties'
    
    # Try to get from cache first
    properties = cache.get(cache_key)
    
    if properties is None:
        # Not in cache, fetch from database
        logger.info("Properties not found in cache, fetching from database")
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        
        # Store in cache for 1 hour (3600 seconds)
        cache.set(cache_key, properties, 3600)
        logger.info(f"Cached {len(properties)} properties for 1 hour")
    else:
        logger.info(f"Retrieved {len(properties)} properties from cache")
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    """
    try:
        from django_redis import get_redis_connection
        
        # Get Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get keyspace info
        info = redis_conn.info()
        
        # Extract hit/miss statistics
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests * 100) if total_requests > 0 else 0
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 2)
        }
        
        logger.info(f"Cache metrics: {metrics}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0
        }
