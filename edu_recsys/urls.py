from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework.documentation import include_docs_urls

apiurlpatterns = [
    path('', include("apps.activity.urls")),
    path('', include('apps.networking.urls')),
    path('docs/', include_docs_urls(title='API Documentaion')),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v0/', include(apiurlpatterns)),
]

urlpatterns += [
    path('', RedirectView.as_view(url='api/v0/docs/'))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
