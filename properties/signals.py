from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Property)
def invalidate_properties_cache_on_save(sender, instance, created, **kwargs):
    """
    Invalidate the all_properties cache when a Property is created or updated.
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    
    action = "created" if created else "updated"
    logger.info(f"Property {instance.title} was {action}. Cache invalidated for key: {cache_key}")


@receiver(post_delete, sender=Property)
def invalidate_properties_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a Property is deleted.
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    
    logger.info(f"Property {instance.title} was deleted. Cache invalidated for key: {cache_key}")
