import copy
from typing import Optional
from apps.pokemon.dtos.types import PokemonDto
from apps.pokemon.dtos.utils import PokemonDtoConverter
import requests


def get_pokeapi_pokemon(pokemon_name: str) -> Optional[PokemonDto]:
    pokemon_name = pokemon_name.lower()
    url = f"http://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
    try:
        response = requests.request("GET", url)
        json_response = response.json()
    except Exception as error:
        raise error
    dto_object = None
    if json_response:
        dto_object = PokemonDtoConverter.json_response_to_dto(json_response)
        return dto_object
    return None