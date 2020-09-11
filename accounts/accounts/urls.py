from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import include, path

from accounts import settings

urlpatterns = [
    path('', include('account.urls')),
    path('support/', include('support.urls')),
    #path('', include('api.urls')),
    #path('auth/', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),
    #path('auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(), name='login_url'),
    path('logout/', views.LogoutView.as_view(), name='logout_url'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
