import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .services import AlertService

logger = logging.getLogger(__name__)


def check_all_alerts():
    """Check all active alerts"""
    try:
        service = AlertService()
        triggered_count = service.check_all_alerts()
        logger.info(f"Checked alerts, triggered {triggered_count}")
    except Exception as e:
        logger.error(f"Error checking alerts: {e}")


def check_alert_by_id(alert_id):
    """Check a specific alert"""
    try:
        from .models import Alert
        alert = Alert.objects.get(id=alert_id, status='active', is_active=True)
        service = AlertService()
        if service.check_alert_condition(alert):
            service.trigger_alert(alert)
            logger.info(f"Alert {alert_id} triggered")
        else:
            logger.info(f"Alert {alert_id} condition not met")
    except Alert.DoesNotExist:
        logger.warning(f"Alert {alert_id} not found or not active")
    except Exception as e:
        logger.error(f"Error checking alert {alert_id}: {e}")


def send_daily_summary():
    """Send daily summaries to users"""
    try:
        users_with_alerts = User.objects.filter(
            alerts__isnull=False,
            email_notifications=True
        ).distinct()

        sent_count = 0
        service = AlertService()

        for user in users_with_alerts:
            stats = service.get_alert_statistics(user=user)
            subject = "Daily Stock Alert Summary"
            message = f"""
        Dear, {user.first_name},

        Here's your daily stock alert summary:

       - Total Alerts: {stats['total_alerts']}
       - Active Alerts: {stats['active_alerts']}
       - Triggered Today: {stats['triggered_alerts']}



        Best regards,
        Farapi team 
            """.strip()
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
                sent_count += 1
            except Exception as e:
                logger.error(f"Error sending summary to {user.email}: {e}")

        logger.info(f"Sent daily summary to {sent_count} users")
    except Exception as e:
        logger.error(f"Error sending daily summaries: {e}")


def cleanup_old_data():
    """Cleanup old triggered alerts and notification logs"""
    try:
        service = AlertService()
        alert_count, log_count = service.cleanup_old_alerts(days=30)
        logger.info(f"Cleaned up {alert_count} old alerts and {log_count} old notification logs")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")


def start_scheduler():
    scheduler = BackgroundScheduler(timezone=str(timezone.get_current_timezone()))
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Add recurring jobs
    scheduler.add_job(check_all_alerts, 'interval', minutes=1, id='check_all_alerts', replace_existing=True)
    scheduler.add_job(cleanup_old_data, 'cron', hour=0, minute=0, id='cleanup_old_data', replace_existing=True)
    scheduler.add_job(send_daily_summary, 'cron', hour=9, minute=0, id='send_daily_summary', replace_existing=True)

    register_events(scheduler)
    scheduler.start()
    logger.info("Scheduler started...")
