from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Views for Vendor
class VendorListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

# Views for Purchase Order
class PurchaseOrderListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

# View for Vendor Performance Metrics
class VendorPerformance(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        performance_metrics = {
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating_avg': instance.quality_rating_avg,
            'average_response_time': instance.average_response_time,
            'fulfillment_rate': instance.fulfillment_rate
        }
        serializer.data['performance_metrics'] = performance_metrics
        return Response(serializer.data)

# View for Acknowledgment Endpoint
class AcknowledgePurchaseOrder(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.vendor.average_response_time = self.calculate_average_response_time(instance.vendor)
        instance.vendor.save()

    def calculate_average_response_time(self, vendor):
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_times = [(order.acknowledgment_date - order.issue_date).seconds / 3600 for order in completed_orders]
        return sum(response_times) / len(response_times) if len(response_times) > 0 else 0