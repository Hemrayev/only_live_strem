from django.urls import path

from .views import *
urlpatterns = [
    path('', index, name='home'),

    path('esasy-shypa/', homepage, name="home_page"),
    path('1-kamera/', camera1, name="camera-1"),

    path('kamera-1/', livefe, name="live_camera"),
    path('kamera-2/', livefe_2, name="live_camera_2"),

    path('ulgama-giris/', admin_login, name='login'),
    # path('ulgama-yazylmak', signup, name='signup'),
    path('gizlin-kody-calyslamak/<token>/', ChangePassword, name='change-password'),
    path('gizlin-kody-yitirmek/', reset_password, name='reset_password'),
    path('ulgamdan_cykys/', admin_logout, name='logout'),
]


handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
handler403 = 'core.views.error_403'
handler400 = 'core.views.error_400'
