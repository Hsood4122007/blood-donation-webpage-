from django.urls import path
from . import views

urlpatterns = [
    # Frontend pages (no API prefix)
    path('register/', views.donor_registration_view, name='register-page'),
    path('login/', views.login_view, name='login-page'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.donor_search_page, name='donor-search-page'),
    path('profile/', views.profile_page, name='profile-page'),
    path('dashboard/', views.dashboard_page, name='dashboard-page'),

    
    # API endpoints (with api/ prefix in main urls.py)
    path('', views.RegisterView.as_view(), name='register-api'),
    path('profile/', views.ProfileView.as_view(), name='profile-api'),
    path('profile/<int:pk>/', views.PublicProfileView.as_view(), name='public-profile-api'),
    path('profile/update/', views.update_profile, name='update-profile-api'),
    
    # Email verification
    path('verify-email/', views.verify_email, name='verify-email'),
    

]