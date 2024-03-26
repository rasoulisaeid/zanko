from django.urls import re_path
from auth.views import ValidatePhoneSendOTP, ValidateOTP, RegisterAPI, LoginAPI
from knox.views import LogoutView


urlpatterns = [
    re_path(r'^check-phone', ValidatePhoneSendOTP.as_view()),
    re_path(r'logout', LogoutView.as_view()),
   # re_path(r'^validate_otp', ValidateOTP.as_view()),
   # re_path(r'^register', RegisterAPI.as_view()),
    re_path(r'^login', LoginAPI.as_view()),
]

