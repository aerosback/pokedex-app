from apps.pokemon import app
from flask import render_template, redirect, url_for, abort, request, jsonify
from apps.pokemon.constants import PokemonTypes
from apps.pokemon.dtos.utils import (
    PokemonDtoConverter,
    types_from_request,
    weaknesses_from_request,
)
from apps.pokemon.forms import AddPokemonForm, EditPokemonForm
from apps.pokemon.queries import (
    get_all_pokemon_types,
    get_pokemon_by_name,
    get_pokemon_pk_by_id,
    get_types_from_pokemon,
    get_weaknesses_from_pokemon,
    list_all_pokemon_entries,
    get_pokemon_by_id,
)
from apps.pokemon.services import save_pokemon, delete_pokemon as delete_pokemon_service

import requests
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/list')
def list_view():
    pokemon_entries = list_all_pokemon_entries()
    return render_template('list.html', pokemon_entries=pokemon_entries)


@app.route('/detail', methods=["GET"])
def detail_view():
    pokemon_id = request.args.get("q")

    if pokemon_id:
        found, pokemon_instance = get_pokemon_by_id(pokemon_id)
        if not found:
            return render_template("error.html",
                        message=f"Requested {pokemon_id} doesn't exist")
        return redirect(
            url_for('pokedox', pokemon_name=pokemon_instance.name))

    return abort(404)


@app.route('/remote_search', methods=["GET"])
def remote_search():
    pokemon_name = request.args.get("name")
    result = {
        'ok': False,
        'error_msg': 'not found name parameter',
        'entries': []
    }

    if pokemon_name:
        
        json_response = None
        pokemon_name = pokemon_name.lower()
        url = f"http://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
        try:
            response = requests.request("GET", url)
            json_response = response.json()
        except Exception as error:
            logger.error(f"error: {error}")

        dto_object = None
        if json_response:
            dto_object = PokemonDtoConverter.json_response_to_dto(json_response)
        
        if dto_object:
            result['ok'] = True
            result['error_msg'] = ''
            result['entries'] = [ dto_object ]
        else:
            result['error_msg'] = f'[pokemon not found] error parsing json for pokemon: {pokemon_name}'

    return jsonify(result)


@app.route('/delete_pokemon')
def delete_pokemon():

    if request.method == "GET":
        pokemon_id = int(request.args.get("q").strip())
        found, pokemon_instance = get_pokemon_by_id(pokemon_id)

        if found:
            delete_pokemon_service(pokemon_id)
            
            return render_template(
                "success.html",
                name=pokemon_instance.name,
                operation="deleted")

        return render_template("error.html",
                               message=f"Requested {pokemon_id} doesn't exist")

    return f"Request method {request.method} not allowed"


@app.route('/edit_pokemon', methods=["GET", "POST"])
def edit_pokemon():

    pokemon_id = request.args.get("q")

    if not pokemon_id:
        return render_template("error.html",
                        message="Empty Pokemon ID passed")

    found_pokemon, pokemon_pk = get_pokemon_pk_by_id(pokemon_id)

    if not found_pokemon:
        return render_template("error.html",
                        message=f"Requested {pokemon_id} doesn't exist")

    form = EditPokemonForm(pokemon_pk, formdata=request.form)

    pokemon_id = int(pokemon_id.strip())

    _, pokemon_instance = get_pokemon_by_id(pokemon_id)

    
    if request.method == "POST":
        if form.validate_on_submit():

            types = types_from_request(request)
            weaknesses = weaknesses_from_request(request)
            pokemon_dto = PokemonDtoConverter.request_to_dto(request, types=types, weaknesses=weaknesses)

            save_pokemon(pokemon_dto)

            return render_template("success.html", name=pokemon_instance.name,
                                operation="updated")
        return render_template("error.html",
                                message=f"Validation not passed for pokemon: {form.errors}")

    if request.method == "GET":

        name = pokemon_instance.name
        description = pokemon_instance.description
        height = pokemon_instance.height
        weight = pokemon_instance.weight
        image_link = pokemon_instance.image_link
        category = pokemon_instance.category
        abilities = pokemon_instance.abilities

        pokemon_types = get_types_from_pokemon(pokemon_id)
        pokemon_types = [pokemon_type.value for pokemon_type in pokemon_types]
        
        pokemon_weaknesses = get_weaknesses_from_pokemon(pokemon_id)
        pokemon_weaknesses = [pokemon_type.value for pokemon_type in pokemon_weaknesses]

        """
            Set checkboxes for queried pokemon type
        """

        pk_type_flag = [0] * len(PokemonTypes)

        for i, pokemon_type_entry in enumerate(PokemonTypes):
            if pokemon_type_entry.value in pokemon_types:
                pk_type_flag[i] = 1

        """
            Set checkboxes for queried pokemon weaknesses
        """

        pk_weakness_flag = [0] * len(PokemonTypes)

        for i, pokemon_type_entry in enumerate(PokemonTypes):
            if pokemon_type_entry.value in pokemon_weaknesses:
                pk_weakness_flag[i] = 1

        all_pokemon_types = get_all_pokemon_types()
        all_pokemon_types = [enum_val.value for enum_val in all_pokemon_types]

        return render_template(
            "edit_pokemon.html",
            form=form,
            name=name,
            pokemon_id=pokemon_id,
            image_link=image_link,
            description=description,
            height=height,
            weight=weight,
            category=category,
            abilities=abilities,
            pk_type_flag=pk_type_flag,
            pk_weakness_flag=pk_weakness_flag,
            pokemon_types=all_pokemon_types,
            is_edit_form=True,
        )

    return f"Request method {request.method} not allowed"


@app.route('/add_pokemon', methods=["GET", "POST"])
def add_pokemon():
    form = AddPokemonForm()

    if request.method == "POST":
        if form.validate_on_submit():

            pokemon_id = request.form.get("pokemon_id")
            name = request.form.get("name")

            if pokemon_id is not None and name is not None:
                pokemon_id = int(pokemon_id.strip())

                types = types_from_request(request)
                weaknesses = weaknesses_from_request(request)

                print(f"{types=}")
                print(f"{weaknesses=}")

                pokemon_dto = PokemonDtoConverter.request_to_dto(
                    request,
                    types=types,
                    weaknesses=weaknesses,
                )

                save_pokemon(pokemon_dto)

                return render_template("success.html", name=name, operation="added")

            return render_template("error.html",
                                message=f"Requested {pokemon_id} doesn't exist")
        
        return render_template("error.html",
                                message=f"Validation not passed for pokemon: {form.errors}")

    if request.method == "GET":
        
        all_pokemon_types = get_all_pokemon_types()
        all_pokemon_types = [enum_val.value for enum_val in all_pokemon_types]
        
        return render_template(
            "add_pokemon.html",
            form=form,
            pokemon_types=all_pokemon_types,
            is_edit_form=False,
        )
    return f"Request method {request.method} not allowed"


@app.route('/pokedox/<string:pokemon_name>')
def pokedox(pokemon_name):
    found, pokemon_instance = get_pokemon_by_name(pokemon_name)
    if found:
        name = pokemon_instance.name
        image_link = pokemon_instance.image_link
        description = pokemon_instance.description
        height = pokemon_instance.height
        weight = pokemon_instance.weight
        abilities = pokemon_instance.abilities

        pokemon_types = get_types_from_pokemon(pokemon_instance.pokemon_id)
        pokemon_weaknesses = get_weaknesses_from_pokemon(pokemon_instance.pokemon_id)

        return render_template(
            "detail.html",
            name=name,
            image_link=image_link,
            description=description, height=height,
            weight=weight,
            pokemon_types=pokemon_types,
            abilities=abilities,
            weakness=pokemon_weaknesses,
        )

    return abort(404)
