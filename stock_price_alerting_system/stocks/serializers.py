from rest_framework import serializers
from .models import Stock, StockPrice

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'symbol', 'name', 'exchange', 'sector', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')


class StockPriceSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source='stock.symbol', read_only=True)
    stock_name = serializers.CharField(source='stock.name', read_only=True)

    class Meta:
        model = StockPrice
        fields = ('id', 'stock_symbol', 'stock_name', 'price', 'open_price',
                  'high_price', 'low_price', 'volume', 'timestamp', 'created_at')
        read_only_fields = ('id', 'created_at')


class StockPriceHistorySerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=4)
    open_price = serializers.DecimalField(max_digits=12, decimal_places=4, allow_null=True)
    high_price = serializers.DecimalField(max_digits=12, decimal_places=4, allow_null=True)
    low_price = serializers.DecimalField(max_digits=12, decimal_places=4, allow_null=True)
    volume = serializers.IntegerField(allow_null=True)
    timestamp = serializers.DateTimeField()


class StockDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    symbol = serializers.CharField()
    name = serializers.CharField()
    exchange = serializers.CharField(allow_blank=True)
    sector = serializers.CharField(allow_blank=True)
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    latest_price = StockPriceSerializer()
    price_history = StockPriceHistorySerializer(many=True)


