from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.HistoryListAPIView.as_view()
    ),
]
