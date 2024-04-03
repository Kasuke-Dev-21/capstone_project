from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.main, name='home'),
    path('contact_us/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('database/', views.members, name='members'),
    path('database/profile/<int:id>', views.profile, name='profile'),
    path('database/profile/edit/<int:student_id>', views.change, name='change'),
    path('maps/', views.map_view, name='maps'),
    path('maps/report/', views.report, name='report'),
    path('maps/search/', views.search_reports, name='search_reports'),
    path('maps/status/', views.update_status, name='update_status'),
    path('maps/edit/', views.map_edit, name='edit_maps'),
    path('qr_scan/', views.qr_scan, name='check_attendance'),
    path('login/', auth_views.LoginView.as_view(template_name='topnav/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('testing/', views.testing, name='testing'),
]