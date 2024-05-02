from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    def update_performance_metrics(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()
        if total_completed_orders > 0:
            on_time_orders = completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date')).count()
            self.on_time_delivery_rate = (on_time_orders / total_completed_orders) * 100

            self.quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

            response_times = completed_orders.exclude(acknowledgment_date=None).annotate(
                response_time=models.F('acknowledgment_date') - models.F('issue_date')
            ).aggregate(Avg('response_time'))['response_time__avg']
            self.average_response_time = response_times.total_seconds() / 3600 if response_times else 0

            self.fulfillment_rate = (completed_orders.filter(quality_rating__isnull=False).count() / total_completed_orders) * 100

            self.save()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50,choices=(('Pending','pending'),('Completed','completed'),('Canceled','canceled')))
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    if created:
        vendor = instance.vendor
        # Calculate on-time delivery rate
        total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        on_time_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=instance.delivery_date).count()
        vendor.on_time_delivery_rate = (on_time_orders / total_completed_orders) * 100 if total_completed_orders != 0 else 0
        
        # Calculate quality rating average
        completed_orders_with_rating = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        vendor.quality_rating_avg = completed_orders_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
        
        # Calculate average response time
        completed_orders_with_acknowledgment = completed_orders_with_rating.exclude(acknowledgment_date=None)
        vendor.average_response_time = completed_orders_with_acknowledgment.aggregate(Avg(models.F('acknowledgment_date') - models.F('issue_date')))['acknowledgment_date__avg'].total_seconds() / 3600 if completed_orders_with_acknowledgment else 0
        
        # Calculate fulfillment rate
        total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
        fulfilled_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False).count()
        vendor.fulfillment_rate = (fulfilled_orders / total_orders) * 100 if total_orders != 0 else 0
        
        vendor.save()