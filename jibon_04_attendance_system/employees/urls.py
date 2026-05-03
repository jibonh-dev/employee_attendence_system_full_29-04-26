from django.urls import path
from .views import *

urlpatterns = [
    path('', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('change-password/', change_password_view, name='change_password_view'),

    path('dashboard/', dashboard, name='dashboard'),
    
    path('attendance/add/', add_attendance, name='add_attendance'),
    path('attendance/update/<int:pk>/', update_attendance, name='update_attendance'),
    path('attendance/delete/<int:pk>/', delete_attendance, name='delete_attendance'),
]
