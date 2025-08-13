import logging
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Alert, AlertHistory, NotificationLog

logger = logging.getLogger(__name__)

class AlertService:
    def check_all_alerts(self):
        """Check all active alerts and trigger notifications if conditions are met."""
        active_alerts = Alert.objects.filter(status='active', is_active=True)
        triggered_count = 0

        for alert in active_alerts:
            if self.is_alert_condition_met(alert):
                if self.trigger_alert(alert):
                    triggered_count += 1

        logger.info(f"Checked {active_alerts.count()} alerts, triggered {triggered_count}")
        return triggered_count

    def is_alert_condition_met(self, alert):
        """Determine if the alert condition has been met."""
        try:
            latest_price = alert.stock.prices.first()
            if not latest_price:
                return False

            current_price = latest_price.price
            target_price = alert.target_price

            if alert.alert_type == 'threshold':
                return self._check_threshold_condition(alert.condition_type, current_price, target_price)
            if alert.alert_type == 'duration':
                return self._check_duration_condition(alert, current_price, target_price)

            return False
        except Exception as e:
            logger.error(f"Error checking alert condition (ID: {alert.id}): {e}")
            return False

    def _check_threshold_condition(self, condition_type, current_price, target_price):
        """Evaluate threshold alert condition."""
        if condition_type == 'above':
            return current_price > target_price
        if condition_type == 'below':
            return current_price < target_price
        if condition_type == 'equal':
            tolerance = target_price * Decimal('0.001')  # 0.1% tolerance
            return abs(current_price - target_price) <= tolerance
        return False

    def _check_duration_condition(self, alert, current_price, target_price):
        """Evaluate duration alert condition."""
        if not alert.duration_minutes:
            return False

        condition_met = self._check_threshold_condition(alert.condition_type, current_price, target_price)

        if not condition_met:
            if alert.duration_start:
                alert.duration_start = None
                alert.save(update_fields=['duration_start'])
            return False

        if not alert.duration_start:
            alert.duration_start = timezone.now()
            alert.save(update_fields=['duration_start'])
            return False

        elapsed = timezone.now() - alert.duration_start
        required_duration = timedelta(minutes=alert.duration_minutes)
        return elapsed >= required_duration

    def trigger_alert(self, alert):
        """Trigger alert, log history, update status, and send notifications."""
        try:
            latest_price = alert.stock.prices.first()
            if not latest_price:
                return False

            alert_history = AlertHistory.objects.create(
                alert=alert,
                triggered_price=latest_price.price,
                triggered_at=timezone.now()
            )

            alert.status = 'triggered'
            alert.triggered_at = timezone.now()
            alert.save(update_fields=['status', 'triggered_at'])

            if alert.email_notification and getattr(alert.user, 'email_notifications', True):
                email_sent = self._send_email_notification(alert, alert_history)
                alert_history.email_sent = email_sent
                alert_history.notification_sent = email_sent
                alert_history.save(update_fields=['email_sent', 'notification_sent'])

            logger.info(f"Alert {alert.id} triggered for {alert.stock.symbol} at ${latest_price.price}")
            return True

        except Exception as e:
            logger.error(f"Error triggering alert (ID: {alert.id}): {e}")
            return False

    def _send_email_notification(self, alert, alert_history):
        """Send email notification and log the outcome."""
        subject = f"Stock Alert: {alert.stock.symbol} has {alert.condition_type} ${alert.target_price}"
        context = {
            'user': alert.user,
            'alert': alert,
            'current_price': alert_history.triggered_price,
            'stock': alert.stock,
            'triggered_at': alert_history.triggered_at,
        }

        message = self._build_email_message(context)

        try:
            success = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[alert.user.email],
                fail_silently=False,
            )

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
            logger.error(f"Failed to send email for alert {alert.id}: {e}")
            NotificationLog.objects.create(
                user=alert.user,
                alert=alert,
                notification_type='email',
                recipient=alert.user.email,
                subject=subject,
                message="Failed to send notification",
                sent_successfully=False,
                error_message=str(e),
            )
            return False

    def _build_email_message(self, context):
        alert = context['alert']
        condition_map = {
            'above': 'risen above',
            'below': 'fallen below',
            'equal': 'reached'
        }
        condition_text = condition_map.get(alert.condition_type, 'met')

        lines = [
            f"Dear {context['user'].first_name or context['user'].username},",
            "",
            f"Your stock alert for {context['stock'].symbol} has been triggered.",
            f"Condition: Price {condition_text} ${alert.target_price}",
            f"Current Price: ${context['current_price']}",
            f"Time: {context['triggered_at'].strftime('%Y-%m-%d %H:%M UTC')}",
        ]

        if alert.alert_type == 'duration':
            lines.append(f"Duration: {alert.duration_minutes} minutes")

        lines.extend([
            "",
            "Manage your alerts by logging into your account.",
            "",
            "Best regards,",
            "Stock Alerting System"
        ])

        return "\n".join(lines)
