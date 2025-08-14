from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Alert, AlertHistory, NotificationLog
from .serializers import (
    AlertSerializer, CreateAlertSerializer, AlertHistorySerializer,
    NotificationLogSerializer, AlertSummarySerializer
)
from .services import AlertService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_alerts(request):
    alerts = Alert.objects.filter(user=request.user)
    serializer = AlertSerializer(alerts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_alert(request):
    serializer = CreateAlertSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        alert = serializer.save()
        return Response(AlertSerializer(alert).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alert_detail(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id, user=request.user)
    serializer = AlertSerializer(alert)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_alert(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id, user=request.user)
    serializer = AlertSerializer(alert, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_alert(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id, user=request.user)
    alert.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alert_history_list(request):
    histories = AlertHistory.objects.filter(alert__user=request.user)
    serializer = AlertHistorySerializer(histories, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_log_list(request):
    """List notification logs for authenticated user"""
    queryset = NotificationLog.objects.filter(user=request.user).order_by('-sent_at')
    queryset = NotificationLog.objects.filter(user=request.user).order_by('-sent_at')
    
    if not queryset.exists():
        return Response(
            {"message": "No notifications found for this user."},
            status=status.HTTP_200_OK
        )
    
    serializer = NotificationLogSerializer(queryset, many=True)
    return Response(serializer.data)


