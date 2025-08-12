from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Stock, StockPrice
from .serializers import (
    StockSerializer,
    StockDetailSerializer,
    StockChartDataSerializer
)


@api_view(["GET"])
def list_stocks(request):
    """List all stocks with latest price"""
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def stock_detail(request, symbol):
    """Get detailed info + history for one stock"""
    try:
        stock = Stock.objects.get(symbol=symbol.upper())
    except Stock.DoesNotExist:
        return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = StockDetailSerializer(stock)
    return Response(serializer.data)


@api_view(["GET"])
def stock_chart_data(request, symbol):
    """Get chart-ready data (timestamp + price)"""
    try:
        stock = Stock.objects.get(symbol=symbol.upper())
    except Stock.DoesNotExist:
        return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

    prices = stock.prices.order_by("-timestamp")[:50]  # last 50 points
    serializer = StockChartDataSerializer(prices, many=True)
    return Response(serializer.data)
