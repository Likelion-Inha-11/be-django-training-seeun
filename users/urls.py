from django.urls import path
from .views import home, user_login, user_logout, signup, mbti_test, mbti_result

urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('mbti_test/', mbti_test, name='mbti_test'),
    path('mbti_result/', mbti_result, name='mbti_result'),
]
