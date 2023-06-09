import json
from dataclasses import asdict, dataclass

import requests
from django.conf import settings
from django.http import HttpResponse
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
