from django.conf.urls import url
from django.urls import path
from dappx import views

# SET THE NAMESPACE!
app_name = 'dappx'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^create_appointment/$', views.create_appointment, name='create_appointment'),
    url(r'^list_appointment/$', views.list_appointment, name='list_appointment'),
    url(r'^get_appointment/$', views.get_appointment, name='get_appointment'),
    path('update/<int:id>/', views.appointment_book, name='appointment_update'),
]
