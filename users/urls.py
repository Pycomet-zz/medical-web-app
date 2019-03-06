from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [

    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path("signup/", views.signup, name='signup'),

    path("regular/register/", views.regular_register.as_view(), name="register-regular"),
    path("regular/profile/info/", views.medical_info, name="info"),
    path("regular/profile/", views.regular_profile, name="r_profile"),
    path("regular/profile/update/", views.update_profile, name="update"),
    
    path("practitioner/register/", views.practitioner_register.as_view(), name="register-practitioner"),
    path("practitioner/profile/", views.practitioner_profile, name="p_profile"),
    path("practitioner/table/", views.table, name='table'),
    url(r'^api/data/$', views.get_data, name='api-data')

]
