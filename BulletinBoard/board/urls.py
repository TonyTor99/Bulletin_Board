from django.urls import path

from .views import *


urlpatterns = [
    path('', welcome, name='welcome'),
    path('ads/', AdList.as_view(), name='ad_list'),
    path('ads/<int:pk>', AdDetail.as_view(), name='ad_detail'),
    path('ads/<int:pk>/delete', AdDelete.as_view(), name='ad_delete'),
    path('ads/<int:pk>/update', AdUpdate.as_view(), name='ad_update'),
    path('create/', AdCreate.as_view(), name='ad_create'),
    path('my_responses/', MyResponses.as_view(), name='my_responses'),
]
