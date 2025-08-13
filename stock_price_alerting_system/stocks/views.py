from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Stock, StockPrice
from .serializers import StockSerializer, StockPriceSerializer

@api_view(['GET'])
def stock_list(request):
    """
    List all stocks with their latest price
    """
    stocks = Stock.objects.prefetch_related('prices').all()
    serializer = StockSerializer(stocks, many=True)
    
    # Add latest price to each stock
    response_data = []
    for stock, serialized_data in zip(stocks, serializer.data):
        stock_data = serialized_data
        latest_price = stock.prices.first()
        
        stock_data['latest_price'] = {
            'price': str(latest_price.price),
            'timestamp': latest_price.timestamp,
            'open_price': str(latest_price.open_price) if latest_price.open_price else None,
            'high_price': str(latest_price.high_price) if latest_price.high_price else None,
            'low_price': str(latest_price.low_price) if latest_price.low_price else None,
            'volume': latest_price.volume
        } if latest_price else None
        
        response_data.append(stock_data)
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def stock_detail_by_symbol(request, symbol):
    """
    Retrieve a stock by symbol with its latest price and price history
    """
    try:
        stock = Stock.objects.prefetch_related('prices').get(symbol__iexact=symbol)
    except Stock.DoesNotExist:
        return Response(
            {'error': f'Stock with symbol {symbol} not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = StockSerializer(stock)
    data = serializer.data
    
    # Add latest price (most recent by timestamp)
    latest_price = stock.prices.order_by('-timestamp').first()
    data['latest_price'] = StockPriceSerializer(latest_price).data if latest_price else None
    
    # Add price history (last 30 prices, newest first)
    price_history = stock.prices.all().order_by('-timestamp')[:30]
    data['price_history'] = StockPriceSerializer(price_history, many=True).data
    
    return Response(data)