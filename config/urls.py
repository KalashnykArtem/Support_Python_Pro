"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from core.api import create_user

# import examples.get_pokemon
# import examples.roles

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", create_user),
    # path("api/pokemon/<str:name>/", examples.get_pokemon.request_method),
    # path(
    #     "api/pokemon/mobile/<str:name>/",
    #     examples.get_pokemon.get_pokemon_for_mobile,
    # ),
    # path("api/pokemon/", examples.get_pokemon.get_all_pokemons),
    # path("create-random-user", examples.roles.create_random_user),
]
