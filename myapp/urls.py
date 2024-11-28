from django.urls import path
from . import views  # Make sure views is imported here

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('stock/', views.stock_view, name='stock'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    # Add other URL patterns as needed
]
