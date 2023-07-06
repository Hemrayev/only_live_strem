import uuid

from django.core.mail import EmailMessage, send_mail
from django.utils.translation import gettext

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth, User
from django.http.response import StreamingHttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from django.conf import settings
from .models import Profile
from .camera import VideoCamera, VideoCamera_2, gen


def index(request):
    return render(request, 'lock_screen.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home_page')
        else:
            messages.info(request, gettext('Maglumatlaryňyzy ýalnyş girizdiňiz!'))
            return redirect('login')
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        mail = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=mail).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=mail, password=password)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()

                email = EmailMessage(
                    f'Siz ulgama doly girdiniz!',
                    f'Gutlayaryn!',
                    settings.EMAIL_HOST_USER,
                    [mail],
                )
                email.fail_silently = True
                email.send()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                return redirect('home_page')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'Munun yaly ulanyjy yok!')
            return redirect('reset_password')

        user_obj = User.objects.get(username=username)
        token = str(uuid.uuid4())
        profile = Profile.objects.get(user=user_obj)
        profile.forget_password_token = token
        profile.save()
        subject = 'Sizin kodunyzy uytgetme yoly!'
        msg = f'Salam su ssylka basyp kodunyzy uytgedip bilersiniz! http://127.0.0.1:8000/gizlin-kody-calyslamak/{token}/'
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [user_obj.email])
        messages.success(request, 'Poctanyza ugradyldy!')
        return redirect('reset_password')
    else:
        return render(request, 'password_reset.html')


def ChangePassword(request, token):
    profile_obj = Profile.objects.filter(forget_password_token=token).first()
    if request.method == 'POST':
        new_passwd = request.POST.get('new_passwd')
        confirm_passwd = request.POST.get('confirm_passwd')
        user_id = request.POST.get('user_id')
        if user_id is None:
            messages.success(request, 'Beyle ulanyjy yok.')
            return redirect('change-password{token}')
        if new_passwd != confirm_passwd:
            messages.info(request, 'Kodlar den gelenok.')
            return redirect('change-password{token}')
        user_obj = User.objects.get(id=user_id)
        user_obj.set_password(new_passwd)
        user_obj.save()
        profile_obj.forget_password_token = str(uuid.uuid4())
        profile_obj.save()
        return redirect('login')
    try:
        context = {'user_id': profile_obj.user.id}
    except:
        raise Http404()
    return render(request, 'change-password.html', context)


@login_required(login_url='login')
def homepage(request):
    return render(request, 'index.html')


def camera1(request):
    return render(request, '1 camera.html')


def livefe(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')


def livefe_2(request):
    return StreamingHttpResponse(gen(VideoCamera_2()), content_type='multipart/x-mixed-replace; boundary=frame')


def admin_logout(request):
    auth.logout(request)
    return redirect('/')


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_500(exception):
    data = {}
    return render('500.html', data)


def error_403(request, exception):
    data = {}
    return render(request, '403.html', data)


def error_400(request, exception):
    data = {}
    return render(request, '400.html', data)
