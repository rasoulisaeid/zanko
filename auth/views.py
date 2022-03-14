import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import permissions, generics, status
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import TokenAuthentication, authenticate
from .models import User, PhoneOTP
from django.contrib.auth import login
from .serializers import CreateUserSerializer, LoginUserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from knox.auth import TokenAuthentication
import random


app_name = "auth"

def generate_otp(phone):
    if phone:
        return random.randint(9999,99999)
    else:
        return False    
        
API_KEY = "686B724A38367657522B496D65555744692B6851526B2F433334554253544552"

def send_otp_to_phone(phone, code):
    url = "https://api.kavenegar.com/v1/" + API_KEY + "/verify/lookup.json" 
    params = {
        'receptor': phone,
        'token': code,
        'template': 'zankoverify'
    }
    headers = {'content-type' : 'application/json'}
    response = requests.post(url, params=params, headers=headers)
    return response

class ValidatePhoneSendOTP(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            code = generate_otp(phone)
            if code:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    old.otp = code
                    old.save()
                    send_otp_to_phone(phone, code)
                    return Response({
                            'status':True,
                            'details': code
                        }) 
                else:
                    otp_model = PhoneOTP.objects.create(
                        phone = phone,
                        otp = code,
                    )  
                    if otp_model:
                        send_otp_to_phone(phone, code)
                        return Response({
                            'status':True,
                            'details': code
                        })  
                    else:
                        return Response({
                        'status':False,
                        'details': 'Sending otp error'
                    })  
            else:
                return Response({
                    'status':False,
                    'details': 'Sending otp error'
                })    
        else:
            return Response({
                'status':False,
                'details': 'phone number is not given.'
            })    

class ValidateOTP(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent   = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            user = User.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.validated = True
                    old.save()
                    if create_user(phone):
                        return Response({'status' : True})
                    else:
                        return Response({'status' : False})
                    
                else:
                    return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or otp was not recieved in Post request'
            })

def create_user(phone):
    password = phone[:4] + "@Aran" + phone[4:] + "@Noha"
    user_data = {'phone': phone, 'password': password }
    serializer = CreateUserSerializer(data=user_data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return True
    else:
        return False    


def check_otp(phone, otp_sent):
    if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.validated = True
                    old.save()
                    user = User.objects.filter(phone__iexact = phone)
                    if user.exists():
                        return True, "user_exists"
                    else:
                        if create_user(phone):
                            return True, "user_created"
                        else:
                            return False, "user_not_created"    
                else:
                    return False, "otp_incorrect"
            else:
                return False, "phone_not_recognized"


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        otp = request.data.get('otp')
        phone = request.data.get('phone')
        result, message = check_otp(phone, otp)
        if result:
            serializer = LoginUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            if user.last_login is None :
                user.first_login = True
                user.save()
                
            elif user.first_login:
                user.first_login = False
                user.save() 
            login(request, user)
            return super().post(request, format=None)
        else:
            return Response({'status':False, 'message': message})          

class RegisterAPI(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        password = phone[:4] + "@Aran" + phone[3:] + "@Noha"
        if phone and password:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                if old.validated:
                    user_data = {
                        'phone': phone,
                        'password': password
                    }
                    serializer = CreateUserSerializer(data=user_data)
                    if serializer.is_valid(raise_exception=True):
                        user = serializer.save()
                        
                        user.first_login = True
                        user.save() 
                        login(request, user)
                        old.delete()
                        return super().post(request, format=None)
                    return Response(serializer.errors, status=400)  
                else:
                    return Response({
                            'status': False,
                            'details': "Otp haven't verified."
                        })         
            else:
                return Response({
                        'status': False,
                        'details': "Please verify your phone."
                    })     
        else:
            return Response({
                    'status': False,
                    'details': "Phone and Password are required."
                })

