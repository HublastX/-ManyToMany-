from django.urls import path, include

urlpatterns = [
    path("api/products/", include("api.urls.product_urls"))
]
