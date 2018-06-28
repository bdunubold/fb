

from django.conf.urls import url

from .views import HomeView
from .views import PageListView
from .views import PageDetailView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^page/list/', PageListView.as_view(), name='page_list'),
    url(r'^page/(?P<id>[0-9]{15})/', PageDetailView.as_view(), name='page_detail'),
]
