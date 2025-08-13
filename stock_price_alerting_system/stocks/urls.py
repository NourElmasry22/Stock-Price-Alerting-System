from django.urls import path
from . import views

urlpatterns = [
    path("stocks/", views.list_stocks, name="list_stocks"),
    path("stocks/<str:symbol>/", views.stock_detail, name="stock_detail"),
    
]
