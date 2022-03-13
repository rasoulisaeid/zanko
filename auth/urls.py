from django.urls import re_path
from auth.views import ValidatePhoneSendOTP, ValidateOTP, Register, LoginAPI


urlpatterns = [
    re_path(r'^validate_phone', ValidatePhoneSendOTP.as_view()),
    re_path(r'^validate_otp', ValidateOTP.as_view()),
    re_path(r'^register', Register.as_view()),
    re_path(r'^login', LoginAPI.as_view()),
]

