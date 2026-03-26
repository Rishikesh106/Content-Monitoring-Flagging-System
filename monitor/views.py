from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Flag
from .serializers import FlagSerializer, FlagStatusUpdateSerializer, KeywordSerializer
from .services import run_scan


class KeywordCreateAPIView(generics.CreateAPIView):
    serializer_class = KeywordSerializer


class ScanAPIView(APIView):
    def post(self, request, *args, **kwargs):
        result = run_scan()
        return Response(result, status=status.HTTP_200_OK)


class FlagListAPIView(generics.ListAPIView):
    serializer_class = FlagSerializer

    def get_queryset(self):
        queryset = Flag.objects.select_related("keyword", "content_item").all()
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class FlagStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Flag.objects.select_related("keyword", "content_item").all()
    serializer_class = FlagStatusUpdateSerializer
    http_method_names = ["patch"]

    def patch(self, request, *args, **kwargs):
        flag = self.get_object()
        serializer = self.get_serializer(flag, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data.get("status", flag.status)
        if new_status != flag.status:
            flag.status = new_status
            flag.reviewed_at = timezone.now()
            flag.save(update_fields=["status", "reviewed_at"])

        return Response(FlagSerializer(flag).data, status=status.HTTP_200_OK)
