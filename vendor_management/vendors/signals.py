from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    if not created:
        instance.vendor.update_performance_metrics()
