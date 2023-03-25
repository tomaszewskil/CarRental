import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, UpdateUserForm, PasswordChangeForm, PasswordResetForm
from .tokens import account_activation_token
from cars.models import RentHistory


# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password incorrect")

    context = {}
    return render(request, "login.html", context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been confirmed")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid")
    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = "Activate you user account"
    message = render_to_string('activate_email.html',
                               {'user': user.username,
                                'domain': get_current_site(request).domain,
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'token': account_activation_token.make_token(user),
                                'protocol': 'https' if request.is_secure() else 'http'
                                }
                               )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.info(request, "You need to verify your email.")
    else:
        messages.error(request, "Problem with sending email")


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')

    context = {'form': form}
    return render(request, "register.html", context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def profilePage(request, username):
    if request.user.get_username() != username:
        return redirect('home')
    if request.method == 'POST':
        user = request.user
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, 'Update successful')
            return redirect("profile", user_form.username)
        for error in list(form.errors.values()):
            messages.error(request, error)

    User = get_user_model()
    user = User.objects.filter(username=username).first()
    if user:
        form = UpdateUserForm(instance=user)
        context = {'form': form}
        return render(request, 'profile.html', context)
    return redirect('home')


@login_required(login_url='login')
def passwordChange(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed")
            return redirect('login')
        for error in list(form.errors.values()):
            messages.error(request, error)

    form = PasswordChangeForm(user)
    context = {'form': form}
    return render(request, 'password_change.html', context)


def passwordReset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get('email')
            user = get_user_model().objects.filter(Q(email=to_email)).first()
            if user:
                subject = "Password Reset"
                message = render_to_string('reset_email.html',
                                           {'user': user,
                                            'domain': get_current_site(request).domain,
                                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token': account_activation_token.make_token(user),
                                            'protocol': 'https' if request.is_secure() else 'http'
                                            }
                                           )
                email = EmailMessage(subject, message, to=[to_email])
                if email.send():
                    messages.info(request, "Password reset mail has been send")
                else:
                    messages.error(request, "Problem with sending email")
                return redirect('home')
            else:
                messages.error(request, 'No user with such email')
                return redirect('password_reset')
    form = PasswordResetForm()
    context = {'form': form}
    return render(request, 'password_reset.html', context)


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password changed")
                return redirect('home')
            for error in list(form.errors.values()):
                messages.error(request, error)

        form = SetPasswordForm(user)
        context = {'form': form}
        return render(request, 'password_reset_confirm.html', context)
    else:
        messages.error(request, "Reset link is invalid")

    return redirect('home')


@login_required(login_url='login')
def rentHistoryPage(request, username):
    if request.user.get_username() != username:
        return redirect('home')
    User = get_user_model()
    user = User.objects.filter(username=username).first()
    history = RentHistory.objects.filter(user=user).order_by('-end_date')
    # history = serializers.serialize('xml', history)
    context = {'history': history,
               'date': datetime.date.today()}
    return render(request, 'rent_history.html', context)
