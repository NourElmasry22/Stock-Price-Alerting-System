# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Alert
from .services import AlertService
from .serializers import AlertSerializer

alert_service = AlertService()

@api_view(['GET'])
@permission_classes([AllowAny])
def list_alerts(request):
    """Get all alerts"""
    alerts = Alert.objects.all()
    serializer = AlertSerializer(alerts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_alert(request):
    """Create a new alert"""
    serializer = AlertSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_alert_statistics(request):
    """Get alert statistics"""
    stats = alert_service.get_alert_statistics()
    return Response(stats)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_all_alerts(request):
    """Run all alerts check manually"""
    alert_service.check_all_alerts()
    return Response({"message": "All alerts checked"})


@api_view(['POST'])
@permission_classes([AllowAny])
def trigger_alert(request, alert_id):
    """Trigger a single alert check manually"""
    alert = get_object_or_404(Alert, id=alert_id)
    alert_service.check_single_alert(alert)
    return Response({"message": f"Alert {alert.id} checked"})


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_alert(request, alert_id):
    """Delete an alert"""
    alert = get_object_or_404(Alert, id=alert_id)
    alert.delete()
    return Response({"message": f"Alert {alert.id} deleted"})
