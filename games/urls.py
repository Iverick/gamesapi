# django imports
from django.conf.urls import url
# local imports
from . import views


urlpatterns = [
    url(r'^games/$', views.game_list),
    url(r'^games/(?P<pk>[0-9]+)/$', views.game_detail),
]
