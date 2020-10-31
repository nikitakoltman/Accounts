#from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
#from django.views.generic import TemplateView

#from lavaccount import settings

urlpatterns = [
    path('', include('home.urls')),
    path('support/', include('support.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('', include('api.urls')),
    #path('auth/', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),
    #path('auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls), ### path('JHFJ#&F(9348chf8/', admin.site.urls),
    #path('sw.js', (TemplateView.as_view(template_name="workers/sw.js", content_type='application/javascript')), name='service_worker_url'),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
