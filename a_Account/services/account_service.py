# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.conf import settings



class AccountService:

    @classmethod
    def forgot_password_email(cls, request, user, email):
        """
        Envia e-mail para redefinição de senha.
        """
        try:
            current_site = get_current_site(request)
            mail_subject = "Redefinir sua senha - Gestor Sites 3.0"
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Contexto para o template
            context = {
                "user": user,
                "domain": current_site.domain if hasattr(current_site, 'domain') else getattr(settings, 'DOMAIN_NAME', 'localhost:8000'),
                "uid": uid,
                "token": token,
                "protocol": 'https' if request.is_secure() else 'http',
            }

            message = render_to_string("account/email/reset_password_email.html", context)

            send_email = EmailMessage(
                mail_subject, 
                message, 
                to=[email]
            )
            # Envia como HTML se necessário
            # send_email.content_subtype = "html" 
            send_email.send(fail_silently=False)

            return 'success', 'Um e-mail de redefinição de senha foi enviado para o seu endereço de e-mail'
        
        except Exception as e:
            # Em produção, deve-se logar o erro
            print(f"Erro ao enviar e-mail: {e}")
            return 'error', f'Erro ao enviar e-mail: {e}'


    @classmethod
    def notification_create_user(cls, request, user):
        """
        Email para notificar usuário de criação de conta e registro de senha
        """
        try:
            current_site = get_current_site(request)
            mail_subject = 'Bem-vindo ao Gestor Sites 3.0 - Nova Conta'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            context = {
                'user': user,
                "domain": current_site.domain if hasattr(current_site, 'domain') else getattr(settings, 'DOMAIN_NAME', 'localhost:8000'),
                "uid": uid,
                "token": token,
                "protocol": 'https' if request.is_secure() else 'http',
            }

            message = render_to_string("account/email/create_user_email.html", context)
            send_email = EmailMessage(
                mail_subject, 
                message, 
                to=[user.email]
            )
            send_email.content_subtype = "html" 
            send_email.send(fail_silently=False)

            return 'success', 'Um e-mail de boas-vindas e definição de senha foi enviado para o usuário.'
        except Exception as e:
            # Em produção, deve-se logar o erro
            print(f"Erro ao enviar e-mail: {e}")
            return 'error', f'Erro ao enviar e-mail: {e}'
