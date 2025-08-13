from rest_framework import serializers
from .models import Stock, StockPrice

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = ('price', 'open_price', 'high_price', 'low_price', 'volume', 'timestamp')

class StockSerializer(serializers.ModelSerializer):
    latest_price = serializers.DictField(read_only=True)
    price_history = StockPriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Stock
        fields = ('id', 'symbol', 'name', 'exchange', 'sector', 'is_active', 
                'latest_price', 'price_history', 'created_at')
        read_only_fields = ('id', 'created_at')