
from typing import List, Optional
from dataclasses import dataclass
from apps.pokemon.constants import PokemonTypes

@dataclass
class PokemonDto:
    pokemon_id: int
    name: str
    description: Optional[str]
    image_link: Optional[str]
    height: Optional[str]
    category: Optional[str]
    weight: Optional[str]
    abilities: Optional[str]

    types: Optional[List[PokemonTypes]]
    weaknesses: Optional[List[PokemonTypes]]