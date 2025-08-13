from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Stock
from .serializers import (
    StockSerializer,
    StockDetailSerializer,

)

@api_view(["GET"])
def list_stocks(request):
    """List all stocks with latest price"""
    stocks = Stock.objects.all()
    stock_list = []
    for stock in stocks:
        latest_price_obj = stock.prices.order_by('-timestamp').first()
        latest_price = None
        if latest_price_obj:
            latest_price = {
                'id': latest_price_obj.id,
                'stock_symbol': stock.symbol,
                'stock_name': stock.name,
                'price': latest_price_obj.price,
                'open_price': latest_price_obj.open_price,
                'high_price': latest_price_obj.high_price,
                'low_price': latest_price_obj.low_price,
                'volume': latest_price_obj.volume,
                'timestamp': latest_price_obj.timestamp,
                'created_at': latest_price_obj.created_at,
            }
        stock_list.append({
            'id': stock.id,
            'symbol': stock.symbol,
            'name': stock.name,
            'exchange': stock.exchange,
            'sector': stock.sector,
            'is_active': stock.is_active,
            'created_at': stock.created_at,
            'latest_price': latest_price,
        })

    serializer = StockDetailSerializer(stock_list, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def stock_detail(request, symbol):
    """Get detailed info + history for one stock"""
    try:
        stock = Stock.objects.get(symbol=symbol.upper())
    except Stock.DoesNotExist:
        return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

    latest_price_obj = stock.prices.order_by('-timestamp').first()
    latest_price = None
    if latest_price_obj:
        latest_price = {
            'id': latest_price_obj.id,
            'stock_symbol': stock.symbol,
            'stock_name': stock.name,
            'price': latest_price_obj.price,
            'open_price': latest_price_obj.open_price,
            'high_price': latest_price_obj.high_price,
            'low_price': latest_price_obj.low_price,
            'volume': latest_price_obj.volume,
            'timestamp': latest_price_obj.timestamp,
            'created_at': latest_price_obj.created_at,
        }

    recent_prices_qs = stock.prices.order_by('-timestamp')[:30]
    price_history = []
    for p in recent_prices_qs:
        price_history.append({
            'price': p.price,
            'open_price': p.open_price,
            'high_price': p.high_price,
            'low_price': p.low_price,
            'volume': p.volume,
            'timestamp': p.timestamp,
        })

    stock_data = {
        'id': stock.id,
        'symbol': stock.symbol,
        'name': stock.name,
        'exchange': stock.exchange,
        'sector': stock.sector,
        'is_active': stock.is_active,
        'created_at': stock.created_at,
        'latest_price': latest_price,
        'price_history': price_history,
    }

    serializer = StockDetailSerializer(stock_data)
    return Response(serializer.data)

