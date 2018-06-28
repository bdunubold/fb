

from django.conf.urls import url

from .views import PagePostListView
from .views import PagePostDAddView
from .views import PageNextView

urlpatterns = [
    url(r'^page/post_list/(?P<id>[0-9]{15})/', PagePostListView.as_view(), name='page_post_list'),
    url(r'^page/add_post/', PagePostDAddView.as_view(), name='page_post_add'),
    url(r'^page/next/', PageNextView.as_view(), name='page_post_next'),
]
