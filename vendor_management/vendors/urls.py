from django.urls import path
from rest_framework.authtoken import views
from .views import (
    VendorListCreate,
    VendorRetrieveUpdateDestroy,
    PurchaseOrderListCreate,
    PurchaseOrderRetrieveUpdateDestroy,
    VendorPerformance,
    AcknowledgePurchaseOrder,
)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    # Vendor URLs
    path('vendors/', VendorListCreate.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroy.as_view(), name='vendor-retrieve-update-destroy'),
    
    # Purchase Order URLs
    path('purchase_orders/', PurchaseOrderListCreate.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroy.as_view(), name='purchase-order-retrieve-update-destroy'),
    
    # Vendor Performance Metrics URL
    path('vendors/<int:pk>/performance/', VendorPerformance.as_view(), name='vendor-performance'),
    
    # Acknowledge Purchase Order URL
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrder.as_view(), name='acknowledge-purchase-order'),
] 
   

