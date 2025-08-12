from rest_framework import serializers
from .models import Alert, AlertHistory, NotificationLog
from stocks.serializers import StockSerializer


class AlertSerializer(serializers.ModelSerializer):
    """Serializer for Alert model"""
    stock_details = StockSerializer(source='stock', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Alert
        fields = ('id', 'stock', 'stock_details', 'user_email', 'alert_type', 'condition_type', 
                 'target_price', 'duration_minutes', 'status', 'is_active', 'email_notification',
                 'created_at', 'updated_at', 'triggered_at')
        read_only_fields = ('id', 'user_email', 'created_at', 'updated_at', 'triggered_at')
    
    def validate(self, attrs):
        # Validate duration fields for duration alerts
        if attrs.get('alert_type') == 'duration':
            if not attrs.get('duration_minutes'):
                raise serializers.ValidationError("Duration minutes is required for duration alerts")
            if attrs.get('duration_minutes') <= 0:
                raise serializers.ValidationError("Duration minutes must be positive")
        
        # Validate target price
        if attrs.get('target_price') and attrs.get('target_price') <= 0:
            raise serializers.ValidationError("Target price must be positive")
        
        return attrs


class CreateAlertSerializer(serializers.ModelSerializer):
    """Serializer for creating alerts"""
    
    class Meta:
        model = Alert
        fields = ('stock', 'alert_type', 'condition_type', 'target_price', 
                 'duration_minutes', 'email_notification')
    
    def validate(self, attrs):
        # Validate duration fields for duration alerts
        if attrs.get('alert_type') == 'duration':
            if not attrs.get('duration_minutes'):
                raise serializers.ValidationError("Duration minutes is required for duration alerts")
            if attrs.get('duration_minutes') <= 0:
                raise serializers.ValidationError("Duration minutes must be positive")
        
        # Validate target price
        if attrs.get('target_price') and attrs.get('target_price') <= 0:
            raise serializers.ValidationError("Target price must be positive")
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AlertHistorySerializer(serializers.ModelSerializer):
    """Serializer for AlertHistory model"""
    alert_details = AlertSerializer(source='alert', read_only=True)
    
    class Meta:
        model = AlertHistory
        fields = ('id', 'alert', 'alert_details', 'triggered_price', 'triggered_at', 
                 'notification_sent', 'email_sent')
        read_only_fields = ('id',)


class NotificationLogSerializer(serializers.ModelSerializer):
    """Serializer for NotificationLog model"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    alert_details = AlertSerializer(source='alert', read_only=True)
    
    class Meta:
        model = NotificationLog
        fields = ('id', 'user_email', 'alert', 'alert_details', 'notification_type', 
                 'recipient', 'subject', 'message', 'sent_successfully', 'error_message', 'sent_at')
        read_only_fields = ('id', 'user_email')


class AlertSummarySerializer(serializers.Serializer):
    """Serializer for alert summary statistics"""
    total_alerts = serializers.IntegerField()
    active_alerts = serializers.IntegerField()
    triggered_alerts = serializers.IntegerField()
    paused_alerts = serializers.IntegerField()
    alerts_by_type = serializers.DictField()
    recent_triggers = AlertHistorySerializer(many=True)