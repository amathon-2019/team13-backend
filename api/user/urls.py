from django.urls import path

from . import views

urlpatterns = [
    path(
        'login/', 
        views.LoginAPIView.as_view(), 
        name='login'
    ),
    path(
        'signup/', 
        views.SignUpAPIView.as_view(), 
        name='signup'
    ),
    path(
        'duplicate/',
        views.DuplicateAPIView.as_view(),
        name='duplicate',
    ),
    path(
        'token/',
        views.TokenListAPIView.as_view(),
        name='token'
    )
]