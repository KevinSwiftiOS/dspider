# -*- coding:utf-8 -*-

from . import views
from django.urls import path

app_name = 'spider'
urlpatterns = [
    path('', views.Index, name='index'),
    path('status', views.Status, name='status'),
    path('runningresults', views.RunningResults, name='runningresults'),
    path('shopresults', views.ShopResults, name='shopresults'),
    path('commentresults', views.CommentsResults, name='commentresults'),
]