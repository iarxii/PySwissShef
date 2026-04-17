from django.urls import path
from . import views

app_name = 'scripts'
urlpatterns = [
    path('', views.home, name='home'),
    path('script/<int:script_id>/', views.script_detail, name='script_detail'),
    path('run/<int:script_id>/', views.run_script, name='run_script'),
    path('showcase/Automation/', views.automation_showcase, name='showcase'),
    path('profile/', views.myprofile, name='profile'),
    path('contact/', views.contact, name='contact'),
]