from django.urls import path, include
from .views import UsuariosViewSet
from rest_framework import routers
urlpatterns = [

    path('', UsuariosViewSet, name='lista_usuarios'),
]
# Routers provide an easy way of automatically determining the URL conf.
"""router = routers.DefaultRouter()
router.register(r'users', UsuariosViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'^', include(router.urls)),
    path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]"""