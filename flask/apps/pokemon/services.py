from apps.pokemon import db
from apps.pokemon.dtos.types import PokemonDto
from apps.pokemon.dtos.utils import PokemonDtoConverter
from apps.pokemon.exceptions import NotFoundInstanceError
from apps.pokemon.models import Pokemon, Weakness, Type

def delete_pokemon(pokemon_id: int) -> None:
        found_pokemon = Pokemon.query.filter(
            Pokemon.pokemon_id == pokemon_id
        ).first()

        if found_pokemon is not None:

            for pokemon_type in found_pokemon.types.all():
                db.session.delete(pokemon_type)

            for pokemon_weakness in found_pokemon.weaknesses.all():
                db.session.delete(pokemon_weakness)

            db.session.delete(found_pokemon)
            db.session.commit()
        else:
            raise NotFoundInstanceError(f'not found instance for pokemon id:{pokemon_id}')


def save_pokemon(dto_instance: PokemonDto) -> None:

    exists_model, pokemon_model = PokemonDtoConverter.dto_to_model(dto_instance)

    if not exists_model:
        db.session.add(pokemon_model)

    if exists_model:
        pokemon_types = Type.query.filter(
            Type.pokemon_id == dto_instance.pokemon_id
        ).all()
        
        pokemon_weakness = Weakness.query.filter(
            Weakness.pokemon_id == dto_instance.pokemon_id
        ).all()

        for pokemon_type in pokemon_types:
            db.session.delete(pokemon_type)
        for pokemon_weakness in pokemon_weakness:
            db.session.delete(pokemon_weakness)

    for pokemon_type in dto_instance.types:
        db.session.add(
            Type(
                pokemon_id=dto_instance.pokemon_id,
                type=f"{pokemon_type}"
            )
        )

    for pokemon_weakness in dto_instance.weaknesses:
        db.session.add(
            Weakness(
                pokemon_id=dto_instance.pokemon_id,
                weakness=f"{pokemon_weakness}"
            )
        )

    db.session.commit()
