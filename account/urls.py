from django.urls import path
from .views import *

urlpatterns = [
    path('login_user/', login_user, name='login_user'),
    path('reg/', reg, name='reg'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('logout/', logout, name='logout'),
    path('Forget_pass/', Forget_pass, name='Forget_pass'),
    path('verify_otp_forget/', verify_otp_forget, name='verify_otp_forget'),
    path('user_deshboard/', user_deshboard, name='user_deshboard'),
    # path('update_profile/<int:id>/', update_profile, name='update_profile'),
]