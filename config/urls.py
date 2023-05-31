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
import json
from dataclasses import asdict, dataclass

import requests
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


def filter_by_keys(source: dict, keys: list[str]) -> dict:
    filtered_data = {}

    for key, value in source.items():
        if key in keys:
            filtered_data[key] = value

    return filtered_data


@dataclass
class Pokemon:
    id: int
    name: str
    height: int
    weight: int
    base_experience: int

    @classmethod
    def from_raw_data(cls, raw_data: dict) -> "Pokemon":
        filtered_data = filter_by_keys(
            raw_data,
            cls.__dataclass_fields__.keys(),
        )
        return cls(**filtered_data)


# ============================================
# Simulate the CACHE
# ============================================
POKEMONS: dict[str, Pokemon] = {}


def get_pokemon_from_api(name: str) -> Pokemon:
    url = settings.POKEAPI_BASE_URL + f"/{name}"
    response = requests.get(url)
    raw_data = response.json()

    return Pokemon.from_raw_data(raw_data)


def _get_pokemon(name) -> Pokemon:
    """
    Take pokemon from the cache or
    fetch it from the API and then save it to the cache.
    """

    if name in POKEMONS:
        pokemon = POKEMONS[name]
    else:
        pokemon: Pokemon = get_pokemon_from_api(name)
        POKEMONS[name] = pokemon

    return pokemon


@csrf_exempt
def request_method(request, name: str):
    if request.method == "GET":
        return get_pokemon(name)
    elif request.method == "DELETE":
        return delete_pokemon(name)


def get_pokemon(name: str):
    pokemon: Pokemon = _get_pokemon(name)
    return HttpResponse(
        content_type="application/json",
        content=json.dumps(asdict(pokemon)),
    )


def delete_pokemon(name: str):
    if name in POKEMONS:
        del POKEMONS[name]
        return HttpResponse(f"{name} is removed from the cache")
    else:
        return HttpResponse(f"{name} isn't in the cache")


def get_pokemon_for_mobile(request, name: str):
    pokemon: Pokemon = _get_pokemon(name)
    result = filter_by_keys(
        asdict(pokemon),
        ["id", "name", "base_experience"],
    )
    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )


def get_all_pokemons(request):
    all_pokemons = []
    for value in POKEMONS.values():
        all_pokemons.append(asdict(value))
    if all_pokemons == []:
        all_pokemons = "Cache is empty"

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(all_pokemons),
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/pokemon/<str:name>/", request_method),
    # path("api/pokemon/<str:name>/", delete_pokemon),
    path("api/pokemon/mobile/<str:name>/", get_pokemon_for_mobile),
    path("api/pokemon/", get_all_pokemons),
]
