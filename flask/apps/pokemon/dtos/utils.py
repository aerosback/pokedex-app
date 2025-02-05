
from typing import List, Optional, Tuple
from apps.pokemon.constants import PokemonTypes
from apps.pokemon.dtos.types import PokemonDto
from apps.pokemon.models import Pokemon
from apps.pokemon.utils import get_weakness_from_all_types
import itertools

class PokemonDtoConverter:
    
    @staticmethod
    def model_to_dto(instance: Pokemon, **kwargs) -> PokemonDto:
        pokemon_num = instance.pokemon_id
        name = instance.name
        description = instance.description
        image_url = instance.image_link
        category = instance.category
        height = instance.height
        weight = instance.weight
        abilities = instance.abilities

        types = kwargs.get('types', [])
        weaknesses = kwargs.get('weaknesses', [])

        dto_instance = PokemonDto(
            pokemon_id=pokemon_num,
            name=name,
            description=description,
            image_link=image_url,
            height=height,
            category=category,
            weight=weight,
            types=types,
            weaknesses=weaknesses,
            abilities=abilities,
        )
        return dto_instance

    @staticmethod
    def request_to_dto(request, **kwargs) -> PokemonDto:

        pokemon_id = int(request.form.get("pokemon_id"))
        pokemon_name = request.form.get("name").strip().lower()
        types = kwargs.get('types', [])
        weaknesses = kwargs.get('weaknesses', [])

        pokemon_dto = PokemonDto(
            pokemon_id=pokemon_id,
            name=pokemon_name,
            description=request.form.get("description"),
            image_link=request.form.get("image_link"),
            height=request.form.get("height"),
            weight=request.form.get("weight"),
            category=request.form.get("category"),
            abilities=request.form.get("ability"),
            types=types,
            weaknesses=weaknesses,
        )
        return pokemon_dto
    
    @staticmethod
    def json_response_to_dto(response) -> Optional[PokemonDto]:

        weaknesses_dict = get_weakness_from_all_types()
        pokemon_id = int(response["id"])
        pokemon_name = response["name"].strip().lower()

        types = [PokemonTypes(entry["type"]["name"]) for entry in response["types"]]
        weaknesses = set([inner_entry.value for entry in types for inner_entry in weaknesses_dict[entry.value]])
        weaknesses = [PokemonTypes(entry) for entry in weaknesses]

        abilities = ','.join([ability["ability"]["name"] for ability in response["abilities"]])

        pokemon_dto = PokemonDto(
            pokemon_id=pokemon_id,
            name=pokemon_name,
            description='',
            image_link=response["sprites"]["other"]["home"]["front_default"],
            height=str(response["height"]),
            weight=str(response["weight"]),
            category='',
            abilities=abilities,
            types=types,
            weaknesses=weaknesses,
        )
        return pokemon_dto
    
    @staticmethod
    def dto_to_model(dto_instance: PokemonDto) -> Tuple[bool, Pokemon]:

        pokemon_model = Pokemon.query.filter(
            Pokemon.pokemon_id == dto_instance.pokemon_id
        ).first()

        pokemon_exists = pokemon_model is not None

        if pokemon_exists:
            pokemon_model.pokemon_id = dto_instance.pokemon_id
            pokemon_model.name = dto_instance.name
            pokemon_model.description = dto_instance.description
            pokemon_model.image_link = dto_instance.image_link
            pokemon_model.height = dto_instance.height
            pokemon_model.weight = dto_instance.weight
            pokemon_model.category = dto_instance.category
            pokemon_model.abilities = dto_instance.abilities
        else:
            pokemon_model = Pokemon(
                pokemon_id=dto_instance.pokemon_id,
                image_link=dto_instance.image_link,
                name=dto_instance.name,
                description=dto_instance.description,
                height=dto_instance.height,
                category=dto_instance.category,
                weight=dto_instance.weight,
                abilities=dto_instance.abilities,
            )

        return pokemon_exists, pokemon_model

    

def types_from_request(request) -> List[PokemonTypes]:
    result_list = []
    for enum_entry in PokemonTypes:
        if request.form.get(f"t_{enum_entry.value}") == "on":
            result_list.append(enum_entry.value)
    return result_list


def weaknesses_from_request(request) -> List[PokemonTypes]:
    result_list = []
    for enum_entry in PokemonTypes:
        if request.form.get(f"w_{enum_entry.value}") == "on":
            result_list.append(enum_entry.value)
    return result_list


