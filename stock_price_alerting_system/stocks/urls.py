from django.urls import path
from . import views

urlpatterns = [
    path("stocks/", views.stock_list, name="list_stocks"),
    path("stocks/<str:symbol>/", views.stock_detail_by_symbol, name="stock_detail"),
    
]
