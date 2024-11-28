from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='signup/', permanent=False)),  # Redirect root URL to signup
    path('', include('myapp.urls')),  # Include all myapp URLs without a prefix
]
