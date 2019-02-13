from django.urls import path, include
from .views import *
from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView,
)
#router = routers.SimpleRouter()
#router.register('', UsuarioListarAPIView)

#router.register('userscreate/', UsuariosCreate)


urlpatterns = [
#Usuarios-----------------------------------
    path('users/list/', UsuarioListarAPIView.as_view(),name='users-list'),
    path('users/profile/', ProfileAPIView.as_view(),name='profile-list'),
    #path('createuser/', UsuarioCrearAPIView.as_view(), name='lista_usuarios'),
    #path('moduser/<int:id>/', UsuarioUpDel.as_view(), name='crud_usuarios'),
    path('users/add/', UsuarioCrearAPIView.as_view(), name='users-add'),
    path('users/<int:id>/edit/', UsuarioEditarAPIView.as_view(), name = 'users-editar'),
    path('users/<int:id>/delete/', UsuarioEliminarAPIView.as_view(), name = 'users-delete'),
    path('users/<int:id>/', UsuarioDetalleByIdAPIView.as_view(), name = 'users-detalle-id'),
    path('users/<email>/<int:id>/', UserByEmail.as_view(), name = 'users-detalle-email'),

    path('users/auth/login/',LoginVieew.as_view()),
    path('users/auth/logout/',LogoutVieew.as_view()),

#Auth
    path('password/reset/', PasswordResetView.as_view(),
        name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    path('login/', LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('password/change/', PasswordChangeView.as_view(),
    name='rest_password_change'),
# User Registration with activation
# Login/Logout
# Retrieve/Update the Django User model
# Password change
# Password reset via e-mail

#Personas--------------------------------------------------------------------
    path('person/list/', PersonaListarAPI.as_view(), name='person-list'),
    path('person/add/', PersonaCreateAPI.as_view(), name='person-create'),
    path('person/añadir/', PerAPIView.as_view(), name='person-crear'),
    path('person/<int:id>/edit/', PersonaEditAPIView.as_view(), name='person-update'),
    path('person/<int:id>/delete/', PersonaDeleteAPIView.as_view(), name='person-delete'),
]
"""""

python manage.py runserver

The new path() syntax in Django 2.0 does not use regular expressions. You want something like:
from django.urls import path, re_path

path('<int:album_id>/', views.detail, name='detail'),
path('<str:car_name>/', views.detail, name='detail'),
path('navigator/<str:search_term>', views.GhNavigator, name='navigator'),

If you want to use a regular expression, you can use re_path().

re_path(r'^(?P<album_id>[0-9])/$', views.detail, name='detail'),

The old url() still works and is now an alias to re_path, but it is likely to be deprecated in future.

url(r'^(?P<album_id>[0-9])/$', views.detail, name='detail'),

path('articles/2003/', views.special_case_2003),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),

luiis potrojurado

"""""