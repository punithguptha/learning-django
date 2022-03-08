from django.shortcuts import render
from rest_framework import generics,status
from .serializers import RegisterSerializer,EmailVerificationSerializer,LoginSerializer,PasswordResetSerializer,SetNewPasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer
    renderer_classes=(UserRenderer,)

    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data=serializer.data

        user=User.objects.get(email=user_data["email"])

        token=RefreshToken.for_user(user)
        access_token=token.access_token

        # We are getting the current site's domain from the request
        current_site=get_current_site(request)
        domain=current_site.domain
        relative_link=reverse('email-verify')
        absoluteurl='http://'+domain+relative_link+"?token="+str(access_token)
        email_body='Hi '+user.username+" User Link below to verify your email \n"+ absoluteurl
        data={'email_body':email_body,'to_email':user.email, 'email_subject':"Verify your email"}
        Util.send_email(data)

        return Response(user_data,status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):

    serializer_class=EmailVerificationSerializer

    # in_ means where the param exists..In our case since it is the query param we specify it
    token_param_openapi=openapi.Parameter('token',in_=openapi.IN_QUERY,description="JWT Token",type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_openapi])
    def get(self,request):
        # HttpRequest.GET is the request here which is django's request object and it returns a QueryDict
        #To access the values inside QueryDict the syntax is QueryDict.get('keyname',default=None) where default is an optional param
        token=request.GET.get('token')
        try:
            # The secret key which is used to generate the token is the django's secret key in settings.py file which we need to pass to decode this completely
            decoded_token_payload=jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            # django simplejwt library stores the user's id claim as user_id.
            user=User.objects.get(id=decoded_token_payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({'email':'Succesfully verified and activated'},status=status.HTTP_200_OK)
            return Response({'email':"User already verified"},status=status.status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Link Expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):

    serializer_class=LoginSerializer

    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class RequestPasswordResetEmailAPIView(generics.GenericAPIView):

    serializer_class=PasswordResetSerializer
    # renderer_classes=(UserRenderer,)

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        email=request.data['email']
        user_exists=User.objects.filter(email=email).exists()

        if user_exists:
            user=User.objects.get(email=email)
            if user.is_verified and user.is_active:
                # Encoded UserId..This should be in bytes so we are using smart_bytes..If not this it throws an error
                uidb64=urlsafe_base64_encode(smart_bytes(user.id))
                token=PasswordResetTokenGenerator().make_token(user)
                current_site=get_current_site(request)
                domain=current_site.domain
                relative_link=reverse('password-reset-check',kwargs={'uidb64':uidb64,'token':token})
                absoluteurl='http://'+domain+relative_link
                email_body='Hello, \n Use the link below to reset your password \n'+ absoluteurl
                data={'email_body':email_body,'to_email':user.email, 'email_subject':"Reset your password"}
                Util.send_email(data)
            elif not user.is_active:
                return Response({'error':'User account disabled...Please contact your administrator'},status=status.HTTP_400_BAD_REQUEST)
            elif not user.is_verified:
                return Response({'error':'User not verified..Please verify your email and try again '},status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        # We send a response like below even if the user doesnot exist because this prevents the other people not to use our api to see who are present in our database based on the response
        return Response({'success':"We have sent you a link to reset your password"},status=status.HTTP_200_OK)

class PasswordTokenCheckAPIView(generics.GenericAPIView):

     serializer_class=SetNewPasswordSerializer

     # Currently we only check if the token is valid or not..But in future it should be the one to redirect to the setnewpassword api when the link is clicked from email
     def get(self,request,uidb64,token):
         try:
             id=smart_str(urlsafe_base64_decode(uidb64))
             user=User.objects.get(id=id)
             # We want the password reset link to be one time use Link
             # For this purpose we take help of PasswordResetTokenGenerator() inbuild method which basically invalidates the token once it is used to change the password
             if not PasswordResetTokenGenerator().check_token(user,token):
                 return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
             return Response({'success':True,'message':'Credentials are valid','uid':uidb64,'token':token},status=status.HTTP_200_OK)

         except DjangoUnicodeDecodeError as identifier:
             return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Password reset successfully'},status=status.HTTP_200_OK)
