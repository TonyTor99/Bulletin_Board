from django.urls import path

from .views import ConfirmUser, RequestNewCode

urlpatterns = [
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('request_new_code/', RequestNewCode.as_view(), name='request_new_code'),
]
