from django.urls import path, include, re_path
from .views import *

app_name="ehealth"

urlpatterns = [
    path('', index, name='index'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('auth/signup/', sign_up, name='signup'),
    path('auth/medic_signup/', medic_signup, name='medic_signup'),
    path('profile/', profile, name='profile'),
    path('auth/login/', log_in, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('stats/', stats, name='stats'),
    path('logout/', logout_request, name='logout'),

]