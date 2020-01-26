from django.urls import path
from products.views import ProductListCreateAPIView, ProductDetailAPIView

app_name = 'products'

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name="list"),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name="detail"),
]
