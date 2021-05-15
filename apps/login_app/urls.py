from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^identity$', views.identity),
    url(r'^unclaimed$', views.unclaimed),
    url(r'^login$', views.login),
    url(r'^accountcreation$', views.accountcreation),
    url(r'^checklogin$', views.checklogin),
    url(r'^logout$', views.logout),

]
