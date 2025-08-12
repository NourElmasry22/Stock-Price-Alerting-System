from django.urls import path
from . import views

urlpatterns = [
    path("stocks/", views.list_stocks, name="list_stocks"),
    path("stocks/<str:symbol>/", views.stock_detail, name="stock_detail"),
    path("stocks/<str:symbol>/chart/", views.stock_chart_data, name="stock_chart_data"),
]
