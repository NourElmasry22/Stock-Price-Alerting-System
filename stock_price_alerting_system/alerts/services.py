import logging
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Alert, AlertHistory, NotificationLog
from stocks.models import StockPrice

logger = logging.getLogger(__name__)


class AlertService:
    """Service class for managing alert operations"""
    
    def check_all_alerts(self):
        """Check all active alerts and trigger notifications if conditions are met"""
        active_alerts = Alert.objects.filter(status='active', is_active=True)
        triggered_count = 0
        
        for alert in active_alerts:
            if self.check_alert_condition(alert):
                self.trigger_alert(alert)
                triggered_count += 1
        
        logger.info(f"Checked {active_alerts.count()} alerts, triggered {triggered_count}")
        return triggered_count
    
    def check_alert_condition(self, alert):
        """Check if an alert condition is met"""
        try:
            # Get latest stock price
            latest_price = alert.stock.prices.first()
            if not latest_price:
                return False
            
            current_price = latest_price.price
            target_price = alert.target_price
            
            if alert.alert_type == 'threshold':
                return self._check_threshold_condition(alert.condition_type, current_price, target_price)
            elif alert.alert_type == 'duration':
                return self._check_duration_condition(alert, current_price, target_price)
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking alert {alert.id}: {e}")
            return False
    
    def _check_threshold_condition(self, condition_type, current_price, target_price):
        """Check threshold alert condition"""
        if condition_type == 'above':
            return current_price > target_price
        elif condition_type == 'below':
            return current_price < target_price
        elif condition_type == 'equal':
            # Allow small tolerance for equality
            tolerance = target_price * Decimal('0.001')  # 0.1% tolerance
            return abs(current_price - target_price) <= tolerance
        return False
    
    def _check_duration_condition(self, alert, current_price, target_price):
        """Check duration alert condition"""
        if not alert.duration_minutes:
            return False
        
        # Check if condition is currently met
        condition_met = self._check_threshold_condition(alert.condition_type, current_price, target_price)
        
        if not condition_met:
            # Reset duration start if condition is not met
            if alert.duration_start:
                alert.duration_start = None
                alert.save()
            return False
        
        # Set duration start if not set
        if not alert.duration_start:
            alert.duration_start = timezone.now()
            alert.save()
            return False
        
        # Check if duration has been met
        duration_elapsed = timezone.now() - alert.duration_start
        required_duration = timedelta(minutes=alert.duration_minutes)
        
        return duration_elapsed >= required_duration
    
    def trigger_alert(self, alert):
        """Trigger an alert and send notifications"""
        try:
            # Get current price
            latest_price = alert.stock.prices.first()
            if not latest_price:
                return False
            
            # Create alert history
            alert_history = AlertHistory.objects.create(
                alert=alert,
                triggered_price=latest_price.price,
                triggered_at=timezone.now()
            )
            
            # Update alert status
            alert.status = 'triggered'
            alert.triggered_at = timezone.now()
            alert.save()
            
            # Send notifications
            if alert.email_notification and alert.user.email_notifications:
                email_sent = self._send_email_notification(alert, alert_history)
                alert_history.email_sent = email_sent
                alert_history.notification_sent = email_sent
                alert_history.save()
            
            logger.info(f"Alert {alert.id} triggered for {alert.stock.symbol} at ${latest_price.price}")
            return True
            
        except Exception as e:
            logger.error(f"Error triggering alert {alert.id}: {e}")
            return False
    
    def _send_email_notification(self, alert, alert_history):
        """Send email notification for triggered alert"""
        try:
            subject = f"Stock Alert: {alert.stock.symbol} has {alert.condition_type} ${alert.target_price}"
            
            # Prepare context for email template
            context = {
                'user': alert.user,
                'alert': alert,
                'current_price': alert_history.triggered_price,
                'stock': alert.stock,
                'triggered_at': alert_history.triggered_at,
            }
            
            # Create email content
            message = self._create_email_message(context)
            
            # Send email
            success = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[alert.user.email],
                fail_silently=False,
            )
            
            # Log notification
            NotificationLog.objects.create(
                user=alert.user,
                alert=alert,
                notification_type='email',
                recipient=alert.user.email,
                subject=subject,
                message=message,
                sent_successfully=bool(success),
            )
            
            return bool(success)
            
        except Exception as e:
            logger.error(f"Error sending email for alert {alert.id}: {e}")
            
            # Log failed notification
            NotificationLog.objects.create(
                user=alert.user,
                alert=alert,
                notification_type='email',
                recipient=alert.user.email,
                subject=f"Stock Alert: {alert.stock.symbol}",
                message="Failed to send notification",
                sent_successfully=False,
                error_message=str(e),
            )
            
            return False
    
    def _create_email_message(self, context):
        """Create email message content"""
        alert = context['alert']
        condition_text = {
            'above': 'risen above',
            'below': 'fallen below',
            'equal': 'reached'
        }.get(alert.condition_type, 'met condition for')
        
        message = f"""
Hello {context['user'].first_name or context['user'].username},

Your stock alert has been triggered!

Stock: {context['stock'].symbol} - {context['stock'].name}
Alert Type: {alert.get_alert_type_display()}
Condition: Price {condition_text} ${alert.target_price}
Current Price: ${context['current_price']}
Triggered At: {context['triggered_at'].strftime('%Y-%m-%d %H:%M:%S UTC')}

{f'Duration: {alert.duration_minutes} minutes' if alert.alert_type == 'duration' else ''}

You can view more details and manage your alerts by logging into your account.

Best regards,
Stock Alerting System
        """.strip()
        
        return message
    
    def send_test_notification(self, alert):
        """Send a test notification for an alert"""
        try:
            subject = f"Test Alert: {alert.stock.symbol} Alert Test"
            
            message = f"""
Hello {alert.user.first_name or alert.user.username},

This is a test notification for your alert:

Stock: {alert.stock.symbol} - {alert.stock.name}
Alert Type: {alert.get_alert_type_display()}
Condition: {alert.get_condition_type_display()} ${alert.target_price}

This alert is currently {alert.get_status_display().lower()}.

Best regards,
Stock Alerting System
            """.strip()
            
            success = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[alert.user.email],
                fail_silently=False,
            )
            
            # Log test notification
            NotificationLog.objects.create(
                user=alert.user,
                alert=alert,
                notification_type='email',
                recipient=alert.user.email,
                subject=subject,
                message=message,
                sent_successfully=bool(success),
            )
            
            return bool(success)
            
        except Exception as e:
            logger.error(f"Error sending test notification for alert {alert.id}: {e}")
            return False
    
    def cleanup_old_alerts(self, days=30):
        """Clean up old triggered alerts and logs"""
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Delete old triggered alerts
        old_alerts = Alert.objects.filter(
            status='triggered',
            triggered_at__lt=cutoff_date
        )
        alert_count = old_alerts.count()
        old_alerts.delete()
        
        # Delete old notification logs
        old_logs = NotificationLog.objects.filter(sent_at__lt=cutoff_date)
        log_count = old_logs.count()
        old_logs.delete()
        
        logger.info(f"Cleaned up {alert_count} old alerts and {log_count} old logs")
        return alert_count, log_count
    
    def get_alert_statistics(self, user=None):
        """Get alert statistics"""
        queryset = Alert.objects.all()
        if user:
            queryset = queryset.filter(user=user)
        
        stats = {
            'total_alerts': queryset.count(),
            'active_alerts': queryset.filter(status='active').count(),
            'triggered_alerts': queryset.filter(status='triggered').count(),
            'paused_alerts': queryset.filter(status='paused').count(),
            'threshold_alerts': queryset.filter(alert_type='threshold').count(),
            'duration_alerts': queryset.filter(alert_type='duration').count(),
        }
        
        return stats