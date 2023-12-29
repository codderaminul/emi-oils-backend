
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from emi import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('accounts/', include('account.urls')),
    path('form-builder/', include('form_builder.urls')),
    path('', include('tbm.urls')),
    path('', include('social_django.urls', namespace='social')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=False)