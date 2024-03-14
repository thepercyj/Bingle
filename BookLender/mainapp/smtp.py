import smtplib
import ssl
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.shortcuts import render


def password_reset_confirm(request, uidb64, token):
    return auth_views.PasswordResetConfirmView.as_view()(request, uidb64=uidb64, token=token,
                                                         template_name='reset.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return render(request, 'forgot.html', {'error_message': 'User with this email does not exist.'})

        # Generate password reset token
    token = default_token_generator.make_token(user)

    # Construct the reset password link
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = reverse('password_reset_confirm', args=[uid, token])
    reset_link = request.build_absolute_uri(reset_url)

    # Compose the email
    subject = 'Reset your password'
    message = f'Hi {user.username},\n\nPlease click on the following link to reset your password:\n\n{reset_link}\n\nBest regards,\nYour Website Team'

    # Send email
    try:
        with smtplib.SMTP('', ) as server:
            server.starttls()
            server.login('', '')
            server.sendmail('', [email], message)
    except Exception as e:
        return render(request, 'forgot.html', {'error_message': f'Failed to send email: {e}'})

    return render(request, 'forgot.html', {'success_message': 'Password reset link has been sent to your email.'})

