from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

urlpatterns = [
    # Dashboard
    url(r'^$', views.index),

    # Requests
    url(r'^my-requests$', views.myRequests),

    # Change Creation
    url(r'^request-change$', views.requestChange),
    url(r'^change-creation$', views.changeCreation),

    url(r'^assigned-me$', views.assignedMe),
    url(r'^active-changes$', views.activeChanges),
    url(r'^past-changes$', views.pastChanges),
    url(r'^change/(?P<id>\d+)$', views.viewChange),
    url(r'^report/all-changes$', views.error500),
    url(r'^report/change-timelines$', views.error500),
    url(r'^report/change-percentages$', views.error500),

    url(r'^account-suspended$', views.error403),
]
