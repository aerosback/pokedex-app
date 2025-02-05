
from typing import Dict, List

from apps.pokemon.constants import DAMAGE_RELATIONS, PokemonTypes


def get_weakness_from_all_types() -> Dict[PokemonTypes, List[PokemonTypes]]:

    weaknesses_dict = {}

    for _type, value in DAMAGE_RELATIONS.items():
        weaknesses = value["defense"]["zero"] or value["defense"]["half"] or value["defense"]["double"]

        weaknesses_dict[_type] = [PokemonTypes(weakness) for weakness in weaknesses]

    return weaknesses_dict