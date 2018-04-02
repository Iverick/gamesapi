# django imports
from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('games.urls')),
    url(r'^api-auth/', include('rest_framework.urls'))
]
