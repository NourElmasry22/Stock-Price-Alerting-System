from django.urls import path
from . import views

urlpatterns = [
    path('alerts/', views.list_alerts, name='list_alerts'),
    path('alerts/create/', views.create_alert, name='create_alert'),
    path('alerts/statistics/', views.get_alert_statistics, name='get_alert_statistics'),
    path('alerts/check/', views.check_all_alerts, name='check_all_alerts'),
    path('alerts/check/<int:alert_id>/', views.trigger_alert, name='trigger_alert'),
    path('alerts/delete/<int:alert_id>/', views.delete_alert, name='delete_alert'),
]
