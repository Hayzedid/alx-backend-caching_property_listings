from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties, get_redis_cache_metrics


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to return all properties with caching enabled for 15 minutes.
    Uses low-level caching for the queryset.
    """
    properties_list = get_all_properties()
    
    return JsonResponse({
        'status': 'success',
        'count': len(properties_list),
        'properties': properties_list
    })


def cache_metrics(request):
    """
    View to display Redis cache metrics.
    """
    metrics = get_redis_cache_metrics()
    
    return JsonResponse({
        'status': 'success',
        'cache_metrics': metrics
    })
