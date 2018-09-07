from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from django.views.generic import RedirectView

apiurlpatterns = [
#    path('activity/', include("apps.activity.urls")),
    path('inter/', include('apps.interpreter.urls')),
    path('docs/', include_docs_urls(title='API Documentaion')),
#    path('dp/', include('apps.digital_profile.urls'))
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