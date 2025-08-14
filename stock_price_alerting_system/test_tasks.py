import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from alerts.models import Alert, AlertHistory, NotificationLog  # Updated imports
from alerts.tasks import (
    check_all_alerts,
    check_alert_by_id,
    send_daily_summary,
    cleanup_old_data,
    start_scheduler
)

@pytest.fixture
def mock_alert_service():
    with patch('alerts.tasks.AlertService') as mock:
        yield mock

@pytest.fixture
def mock_logger():
    with patch('alerts.tasks.logger') as mock:
        yield mock

@pytest.fixture
def mock_scheduler():
    with patch('alerts.tasks.BackgroundScheduler') as mock:
        yield mock

@pytest.fixture
def mock_django_job_store():
    with patch('alerts.tasks.DjangoJobStore') as mock:
        yield mock

@pytest.fixture
def mock_register_events():
    with patch('alerts.tasks.register_events') as mock:
        yield mock

@pytest.fixture
def mock_send_mail():
    with patch('alerts.tasks.send_mail') as mock:
        yield mock

@pytest.fixture
def mock_user_model():
    with patch('alerts.tasks.User') as mock:
        yield mock

@pytest.fixture
def mock_alert_model():
    with patch('alerts.models.Alert') as mock:  # Fixed path
        yield mock

class TestCheckAllAlerts:
    def test_successful_check(self, mock_alert_service, mock_logger):
        mock_service_instance = mock_alert_service.return_value
        mock_service_instance.check_all_alerts.return_value = 3
        
        result = check_all_alerts()
        
        mock_alert_service.assert_called_once()
        mock_service_instance.check_all_alerts.assert_called_once()
        mock_logger.info.assert_called_with("Checked alerts, triggered 3")
        assert result is None

    def test_exception_handling(self, mock_alert_service, mock_logger):
        mock_service_instance = mock_alert_service.return_value
        mock_service_instance.check_all_alerts.side_effect = Exception("Test error")
        
        result = check_all_alerts()
        
        mock_logger.error.assert_called_with("Error checking alerts: Test error")
        assert result is None


class TestSendDailySummary:
    def test_successful_summary(self, mock_user_model, mock_alert_service, mock_send_mail, mock_logger):
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.first_name = "Test"
        mock_user_model.objects.filter.return_value.distinct.return_value = [mock_user]
        
        mock_service_instance = mock_alert_service.return_value
        mock_service_instance.get_alert_statistics.return_value = {
            'total_alerts': 5,
            'active_alerts': 3,
            'triggered_alerts': 2
        }
        
        send_daily_summary()
        
        mock_user_model.objects.filter.assert_called()
        mock_service_instance.get_alert_statistics.assert_called_with(user=mock_user)
        mock_send_mail.assert_called_once()
        mock_logger.info.assert_called_with("Sent daily summary to 1 users")

    def test_no_users_with_alerts(self, mock_user_model, mock_logger):
        mock_user_model.objects.filter.return_value.distinct.return_value = []
        
        send_daily_summary()
        
        mock_logger.info.assert_called_with("Sent daily summary to 0 users")

    def test_email_send_failure(self, mock_user_model, mock_alert_service, mock_send_mail, mock_logger):
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.first_name = "Test"
        mock_user_model.objects.filter.return_value.distinct.return_value = [mock_user]
        
        mock_service_instance = mock_alert_service.return_value
        mock_service_instance.get_alert_statistics.return_value = {
            'total_alerts': 5,
            'active_alerts': 3,
            'triggered_alerts': 2
        }
        
        mock_send_mail.side_effect = Exception("Email error")
        
        send_daily_summary()
        
        mock_logger.error.assert_called_with("Error sending summary to test@example.com: Email error")
        mock_logger.info.assert_called_with("Sent daily summary to 0 users")

    def test_general_exception(self, mock_user_model, mock_logger):
        mock_user_model.objects.filter.side_effect = Exception("General error")
        
        send_daily_summary()
        
        mock_logger.error.assert_called_with("Error sending daily summaries: General error")

class TestCleanupOldData:
    def test_successful_cleanup(self, mock_alert_service, mock_logger):
        mock_service_instance = mock_alert_service.return_value
        mock_service_instance.cleanup_old_alerts.return_value = (5, 10)
        
        cleanup_old_data()
        
        mock_service_instance.cleanup_old_alerts.assert_called_with(days=30)
        mock_logger.info.assert_called_with("Cleaned up 5 old alerts and 10 old notification logs")

    def test_exception_handling(self, mock_alert_service, mock_logger):
        mock_service_instance = mock_alert_service.return_value
        mock_service_instance.cleanup_old_alerts.side_effect = Exception("Cleanup error")
        
        cleanup_old_data()
        
        mock_logger.error.assert_called_with("Error during cleanup: Cleanup error")

class TestStartScheduler:
    def test_scheduler_startup(self, mock_scheduler, mock_django_job_store, mock_register_events, mock_logger):
        mock_scheduler_instance = mock_scheduler.return_value
        
        start_scheduler()
        
        mock_scheduler.assert_called_once_with(timezone=str(timezone.get_current_timezone()))
        mock_scheduler_instance.add_jobstore.assert_called_once_with(mock_django_job_store.return_value, "default")
        
        assert mock_scheduler_instance.add_job.call_count == 3
        
        mock_register_events.assert_called_once_with(mock_scheduler_instance)
        mock_scheduler_instance.start.assert_called_once()
        mock_logger.info.assert_called_with("Scheduler started...")