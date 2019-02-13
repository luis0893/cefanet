"""facerecog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

urlpatterns = [
    #path('recog/', include('recog.urls')),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('api/v1/', include('recog.api_urls')),
    path('api/v1/auth/', include('rest_auth.urls')),
    path('api/v1/auth/registration/', include('rest_auth.registration.urls')),
    path('__debug__', include(debug_toolbar.urls)),

    #path('api/v1/', include(urlpatterns)),#otra forma
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#djangorestframework [required: >=3.1.3, installed: 3.8.2] Django [required: >=1.8.0, installed: 2.0.7]


# admin /
# api / v1 / users / list / [name = 'users-list']
# api / v1 / users / add / [name = 'users-add']
# api / v1 / users / < int: id > / edit / [name = 'users-editar']
# api / v1 / users / < int: id > / delete / [name = 'users-delete']
# api / v1 / users / < int: id > / [name = 'users-detalle-id']
# api / v1 / users / < email > / < int: id > / [name = 'users-detalle-email']
# api / v1 / users / auth / login /
# api / v1 / users / auth / logout /
# api / v1 / password / reset / [name = 'rest_password_reset']
# api / v1 / password / reset / confirm / [name = 'rest_password_reset_confirm']
# api / v1 / login / [name = 'rest_login']
# api / v1 / logout / [name = 'rest_logout']
# api / v1 / user / [name = 'rest_user_details']
# api / v1 / password / change / [name = 'rest_password_change']
# api / v1 / person / list / [name = 'person-list']
# api / v1 / person / add / [name = 'person-create']
# api / v1 / person / < int: id > / edit / [name = 'person-update']
# api / v1 / person / < int: id > / delete / [name = 'person-delete']
# api / v1 / auth / ^ password / reset /$ [name = 'rest_password_reset']
# api / v1 / auth / ^ password / reset / confirm /$ [name = 'rest_password_reset_confirm']
# api / v1 / auth / ^ login /$ [name = 'rest_login']
# api / v1 / auth / ^ logout /$ [name = 'rest_logout']
# api / v1 / auth / ^ user /$ [name = 'rest_user_details']
# api / v1 / auth / ^ password / change /$ [name = 'rest_password_change']
# api / v1 / auth / registration / ^$ [name = 'rest_register']
# api / v1 / auth / registration / ^ verify - email /$ [name = 'rest_verify_email']
# api / v1 / auth / registration / ^ account - confirm - email / (?P < key >[-:\w]+) /$ [name = 'account_confirm_email']
