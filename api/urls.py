from django.urls import path, include

urlpatterns = [
    path(
        'users/', 
        include(
            ('api.user.urls', 'user'), 
            namespace='user'
        ),
    ),
    path(
        'histories/', 
        include(
            ('api.history.urls', 'history'), 
            namespace='history'
        ),
    ),
]
