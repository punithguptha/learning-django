from django.shortcuts import render
from rest_framework import generics,status
from .serializers import RegisterSerializer,EmailVerificationSerializer
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


# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer

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
    pass
