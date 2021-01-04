import jwt
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_short_url.models import ShortURL
from validate_email import validate_email
# Create your views here.
from rest_framework.generics import GenericAPIView

from FundooNote_Project.settings.dev import SECRET_KEY
from Note_APp.serializer import RegisterationFormSerializer, LoginFormFormSerializer, ForgotPasswordFormSerializer, \
    ResetPasswordFormSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, auth
from django_short_url.views import get_surl
import logging

from Note_APp.tokens import token_activation

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename="C:\\Users\\KatK\\django_projects\\FundooNote_Project\\static\\logtest.log",
                    level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger()


class registerForm(GenericAPIView):
    serializer_class = RegisterationFormSerializer

    def post(self, request):
        try:
            userName = request.data['username']
            email = request.data['email']
            password = request.data['password']
            confirm_password = request.data['confirm_password']

            if userName == "" or email == "" or password == "":
                return Response("You can not put empty fields", status=status.HTTP_406_NOT_ACCEPTABLE)
            if password == confirm_password:
                try:
                    validate_email(email)
                    user = User.objects.create(username=userName, email=email, password=password)
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    domain_name = current_site.domain

                    token = token_activation(
                        username=userName, password=password)

                    url = str(token)
                    surl = get_surl(url)
                    short_token = surl.split('/')

                    mail_subject = "Click link for activating "
                    msg = render_to_string('email_validation.html', {
                        'user': userName,
                        'domain': domain_name,
                        'surl': short_token[2]
                    })
                    recipients = email
                    print(msg)
                    email = EmailMessage(mail_subject, msg, to=[recipients])
                    email.send()
                    print('confirmation mail sent')
                    return Response('Please confirm your email address to complete the registration',
                                    status=status.HTTP_200_OK)

                except ValidationError:
                    return Response("Email not found", status=status.HTTP_404_NOT_FOUND)

            else:
                return Response("Password Missmatch", status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response("User Already exist")

def activate(request, surl):
        try:
            token_object = ShortURL.objects.get(surl=surl)
            token = token_object.lurl
            decode = jwt.decode(token, SECRET_KEY)
            user_name = str(decode['username'])

            user = User.objects.get(username=user_name)

            if user is not None:
                user.is_active = True
                user.save()
                return HttpResponse("successfully activate your account......")

            else:
                return Response("Something went wrong")

        except KeyError:
            return Response("Key Error")


class loginForm(GenericAPIView):
    serializer_class = LoginFormFormSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return Response("Login successfully", status=status.HTTP_202_ACCEPTED)
            else:
                return Response("Please activate your account")
        else:
            return Response("Log in failed", status=status.HTTP_406_NOT_ACCEPTABLE)


class logoutForm(GenericAPIView):
    serializer_class = LoginFormFormSerializer

    def get(self, request):
        try:
            auth.logout(request)
            return Response({'details': 'your succefully loggeg out,thankyou'})
        except Exception:
            return Response({'details': 'something went wrong while logout'})


class forgotPasswordForm(GenericAPIView):
    serializer_class = ForgotPasswordFormSerializer

    def post(self, request):
        email = request.data('email')
        try:
            user = User.objects.filter(email=email)
            if user.count() == 0:
                return Response("Not Found mail in database")
            else:
                username = user.values()[0]["username"]
                current_site = get_current_site(request)
                domain_name = current_site.domain

                token = token_activation(username=username)

                url = str(token)
                surl = get_surl(url)
                short_token = surl.split('/')

                mail_subject = "Click link for activating "
                msg = render_to_string('email_validation.html', {
                    'user': username,
                    'domain': domain_name,
                    'surl': short_token[2]
                })
                recipients = email
                email = EmailMessage(mail_subject, msg, to=[recipients])
                email.send()
                print('confirmation mail sent')
                return Response('Please confirm your email address to reset password')

        except KeyError:
            return Response("Key error")


class resetPasswordForm(GenericAPIView):
    serializer_class = ResetPasswordFormSerializer

    def post(self, request):
        username = self.request.user.username
        if username != "":
            password = request.data['password']
            confirm_password = request.data['confirm_password']

            if password == "" or confirm_password == "":
                return Response("you can not put empty field")

            if password == confirm_password:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()

                return Response("successfull reset password")

            else:
                return Response("password missmatch")

        else:
            return Response("First you have to login")

@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_decorator, name='dispatch')
def activate(request, token):
    try:
        url = ShortURL.objects.get(surl=token)
        token = url.lurl
        user_details = jwt.decode(token, 'private_secret', algorithms='HS256')
        user_name = user_details['username']
        user = User.objects.get(username=user_name)
        try:
            user = User.objects.get(username=user_name)
        except ObjectDoesNotExist as e:
            print(e)
        if user is not None:
            user.is_active = True
            user.save()
            messages.info(request, " Account is active now ")
            return redirect('login')
        else:
            return redirect('register')
    except KeyError:
        messages.info(request, ' Sending Email Failed ')
        return redirect('/register')
