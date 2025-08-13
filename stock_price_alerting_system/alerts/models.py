from django.db import models
from stocks.models import Stock
from django.contrib.auth.models import User

class Alert(models.Model):
    
    ALERT_TYPES = [
        ('threshold', 'Threshold Alert'),
        ('duration', 'Duration Alert'),
    ]
    
    CONDITION_TYPES = [
        ('above', 'Above'),
        ('below', 'Below'),
        ('equal', 'Equal'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('triggered', 'Triggered'),
        ('expired', 'Expired'),
        ('paused', 'Paused'),
    ]
    user = models.ForeignKey(User,related_name='alerts', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    condition_type = models.CharField(max_length=10, choices=CONDITION_TYPES)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    duration_minutes = models.IntegerField(null=True, blank=True, help_text="Duration in minutes for duration alerts")
    duration_start = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    
    email_notification = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.stock.symbol} {self.condition_type} ${self.target_price}"
    
    class Meta:
        ordering = ['-created_at']


class AlertHistory(models.Model):
    """History of triggered alerts"""
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='history')
    triggered_price = models.DecimalField(max_digits=10, decimal_places=2)
    triggered_at = models.DateTimeField()
    notification_sent = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Alert {self.alert.id} triggered at ${self.triggered_price}"
    
    class Meta:
        ordering = ['-triggered_at']


class NotificationLog(models.Model):
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    recipient = models.CharField(max_length=200)  
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_successfully = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.notification_type} to {self.recipient} - {'Success' if self.sent_successfully else 'Failed'}"
    
    class Meta:
        ordering = ['-sent_at']