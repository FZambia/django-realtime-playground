# coding: utf-8
from django.conf.urls import patterns, url, include
import realtime.views as views
from django.contrib.auth.decorators import login_required


urlpatterns = patterns("",
    url(
        regex=r"^message/$",
        view=login_required(views.MessageListView.as_view()),
        name="realtime_message_list",
    ),
    url(
        regex=r"^message/create/$",
        view=login_required(views.MessageCreateView.as_view()),
        name="realtime_message_create",
    ),
    url(
        regex=r"^message/delete/(?P<pk>\d+)/$",
        view=login_required(views.MessageDeleteView.as_view()),
        name="realtime_message_delete",
    ),
)
