"""
URL configuration for barangay_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView # <--- ADD THIS IMPORT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('residents/', include('residents.urls')), # Let's assume this is where 'index' for residents is
    path('accounts/login/', auth_views.LoginView.as_view(template_name='residents/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # This will now work

    # ---- ADD THIS LINE ----
    # This will redirect the root path (e.g., http://127.0.0.1:8000/)
    # to your residents app's main page (e.g., http://127.0.0.1:8000/residents/)
    # It assumes your 'residents.urls' has a path named 'index' for its main view,
    # or simply a path '' that points to the residents list.
    # If your main residents page is directly at /residents/ and is named 'index'
    # in your residents/urls.py, this should work.
    # A simpler redirect if your residents app is always at /residents/:
    path('', RedirectView.as_view(url='/residents/', permanent=False), name='home'),
    # ----------------------
]

# barangay_system/urls.py

# ... (your existing imports and urlpatterns) ... # This comment is a bit redundant here now

# Add these lines at the very bottom
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)