from rest_framework import serializers
from .models import Stock, StockPrice


class StockSerializer(serializers.ModelSerializer):
    """Serializer for Stock model"""
    latest_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Stock
        fields = ('id', 'symbol', 'name', 'exchange', 'sector', 'is_active', 'latest_price', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_latest_price(self, obj):
        latest_price = obj.prices.first()
        if latest_price:
            return {
                'price': str(latest_price.price),
                'timestamp': latest_price.timestamp,
                'open_price': str(latest_price.open_price) if latest_price.open_price else None,
                'high_price': str(latest_price.high_price) if latest_price.high_price else None,
                'low_price': str(latest_price.low_price) if latest_price.low_price else None,
                'volume': latest_price.volume
            }
        return None


class StockPriceSerializer(serializers.ModelSerializer):
    """Serializer for StockPrice model"""
    stock_symbol = serializers.CharField(source='stock.symbol', read_only=True)
    stock_name = serializers.CharField(source='stock.name', read_only=True)
    
    class Meta:
        model = StockPrice
        fields = ('id', 'stock_symbol', 'stock_name', 'price', 'open_price', 
                 'high_price', 'low_price', 'volume', 'timestamp', 'created_at')
        read_only_fields = ('id', 'created_at')


class StockPriceHistorySerializer(serializers.ModelSerializer):
    """Serializer for stock price history"""
    
    class Meta:
        model = StockPrice
        fields = ('price', 'open_price', 'high_price', 'low_price', 'volume', 'timestamp')


class StockDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Stock with price history"""
    latest_price = serializers.SerializerMethodField()
    price_history = serializers.SerializerMethodField()
    
    class Meta:
        model = Stock
        fields = ('id', 'symbol', 'name', 'exchange', 'sector', 'is_active', 
                 'latest_price', 'price_history', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_latest_price(self, obj):
        latest_price = obj.prices.first()
        if latest_price:
            return StockPriceSerializer(latest_price).data
        return None
    
    def get_price_history(self, obj):
        # Get last 30 price records
        recent_prices = obj.prices.all()[:30]
        return StockPriceHistorySerializer(recent_prices, many=True).data

class StockChartDataSerializer(serializers.ModelSerializer):
    """Serializer for chart-ready price data"""
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = StockPrice
        fields = ("timestamp", "price")
