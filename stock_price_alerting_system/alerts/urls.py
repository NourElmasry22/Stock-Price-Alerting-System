from django.urls import path
from . import views

urlpatterns = [
    path('alerts/', views.list_alerts, name='list_alerts'),
    path('alerts/create/', views.create_alert, name='create_alert'),
    path('alert-history/', views.alert_history_list, name='alert_history_list'),
    path('notification-log/', views.notification_log_list, name='notification_log_list'),
    path('alerts/<int:pk>/', views.update_alert, name='update_alert'),
    path('alerts/<int:pk>/delete/', views.delete_alert, name='delete_alert'),

]
