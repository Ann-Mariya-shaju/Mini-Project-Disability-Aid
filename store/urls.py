from django.contrib.auth import views as auth_views
from django.urls import path
from .import views

urlpatterns = [
   
   path('',views.index,name="index"),
   path('doctor.html', views.doctor, name='doctor'),
   path('doctor_view.html', views.doctor_view, name='doctor_view'),
   path('profile_update.html', views.profile_update,name='profile_update'),
   
   path('index.html',views.index,name="registration"),
   path('registration.html',views.registration,name="registration"),
   path('login.html',views.login,name="login"),
   path('index',views.index,name="index"),
   path('dashboard',views.dashboard,name="dashboard"),
   path('panchayat',views.panchayat,name="panchayat"),
   path('admindashboard',views.admindashboard, name='admindashboard'),
   path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   
   

   #path('admin_index/', views.admin_index, name='admin_index'),
   path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
   path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
   path('my_profile',views.my_profile,name="my_profile"),

   
   #path('accounts/login/', views.login, name='login'),
   path('logout/',views.logout,name="logout"),



   path('edit/<int:doctor_id>/', views.edit, name='edit'),
   path('delete/<int:doctor_id>/', views.delete, name='delete'),
  
]

