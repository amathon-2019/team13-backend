from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.history.models import History
from .serializers import HistorySerializer


class HistoryListAPIView(GenericAPIView):
    queryset = History.objects.all().order_by('-created')
    serializer_class = HistorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            user=self.request.user
        )

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'username': self.request.user.username,
            'data': serializer.data
        })
