from typing import List, Optional, Tuple
from apps.pokemon.constants import PokemonTypes
from apps.pokemon.dtos.types import PokemonDto
from apps.pokemon.dtos.utils import PokemonDtoConverter
from apps.pokemon.models import Pokemon, Type, Weakness

def list_all_pokemon_entries() -> List[PokemonDto]:
    pokemons = Pokemon.query.all()
    result_pokemons = []

    for pokemon in pokemons:
        types = pokemon.types.all()
        types = [pk_type.type for pk_type in types]

        weaknesses = pokemon.weaknesses.all()
        weaknesses = [weakness.weakness for weakness in weaknesses]

        pokemon_dto = PokemonDtoConverter.model_to_dto(pokemon, types=types, weaknesses=weaknesses)
        result_pokemons.append(pokemon_dto)
        
    return result_pokemons

def get_all_pokemon_types() -> List[PokemonTypes]:
    return [enum_value for enum_value in PokemonTypes]

def get_pokemon_by_id(pokemon_id: int) -> Tuple[bool, Optional[PokemonDto]]:
    pokemon_found = Pokemon.query.filter(
        Pokemon.pokemon_id == pokemon_id
    ).first()
    return pokemon_found is not None, pokemon_found

def get_pokemon_pk_by_id(pokemon_id: int) -> Tuple[bool, Optional[int]]:
    pokemon_found = Pokemon.query.filter(
        Pokemon.pokemon_id == pokemon_id
    ).first()
    return pokemon_found is not None, pokemon_found.id

def get_pokemon_by_name(name: str) -> Tuple[bool, Optional[PokemonDto]]:
    pokemon_found = Pokemon.query.filter(
        Pokemon.name == name
    ).first()
    return pokemon_found is not None, pokemon_found


def get_types_from_pokemon(pokemon_id: int) -> List[PokemonTypes]:
    types = Type.query.filter(
        Type.pokemon_id == pokemon_id
    ).all()
    types = [PokemonTypes(pokemon_type.type) for pokemon_type in types]
    return types

def get_weaknesses_from_pokemon(pokemon_id: int) -> List[PokemonTypes]:
    weaknesses = Weakness.query.filter(
        Weakness.pokemon_id == pokemon_id
    ).all()
    weaknesses = [PokemonTypes(pokemon_type.weakness) for pokemon_type in weaknesses]
    return weaknesses


def exists_pokemon_with_name(pokemon_name: str, **kwargs) -> bool:
    pokemon_pk = kwargs.get('pokemon_pk', None)
    pokemon_found = Pokemon.query.filter(
        Pokemon.name == pokemon_name
    ).first()
    if pokemon_pk and pokemon_found:
        return pokemon_found.id != pokemon_pk
    return pokemon_found is not None

def exists_pokemon_with_pokemon_id(pokemon_id: int, **kwargs) -> bool:
    pokemon_pk = kwargs.get('pokemon_pk', None)
    pokemon_found = Pokemon.query.filter(
        Pokemon.pokemon_id == pokemon_id
    ).first()
    if pokemon_pk and pokemon_found:
        return pokemon_found.id != pokemon_pk
    return pokemon_found is not None