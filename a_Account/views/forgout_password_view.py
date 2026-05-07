from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


from a_Account.forms import ForgoutPasswordForm, ResetPasswordForm
from a_Account.services import AccountService


def forgot_password(request):
    User = auth.get_user_model()
    form = ForgoutPasswordForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            result, message = AccountService.forgot_password_email(request, user, email)
            if result == 'success':
                messages.success(request, message)
                return redirect('account:login')
            else:
                messages.error(request, message)
        else:
            messages.warning(request, 'Conta não existe.')
            return redirect('account:forgout-password')

    context = {
        'form' : form
    }

    return render(request, 'account/forgout_password.html', context=context)


def resetpassword_validate(request, uidb64=None, token=None):
    try:
        User = auth.get_user_model()
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Redefina sua senha.")
        return redirect("account:reset-password")
    else:
        messages.warning(request, "Este link expirou.")
        return redirect("account:login")
    

def reset_password(request):

    form = ResetPasswordForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        User = auth.get_user_model()
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirmar_password']

        if password == confirm_password:
            uid = request.session.get("uid")
            user = User.objects.get(pk=uid)

            # Aplica validação de senha forte
            try:
                validate_password(password, user)
            except ValidationError as e:
                return render(request, "account/reset_password.html", {'errors': e.messages, 'form': form})

            user.set_password(password)
            user.save()
            messages.success(request, "Redefinição de senha bem-sucedida.")
            # falta remover session uid
            return redirect("account:login")
        else:
            messages.warning(request, "Senha não confere!")
            return redirect("account:reset-password")
    else:
        context = {
            'form' : form
        }
        return render(request, "account/reset_password.html", context=context)