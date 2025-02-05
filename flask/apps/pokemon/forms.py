from flask_wtf import  FlaskForm
from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length

from apps.pokemon.queries import exists_pokemon_with_name, exists_pokemon_with_pokemon_id


class AddPokemonForm(FlaskForm):
    pokemon_id = IntegerField(label='Pokedox_ID', validators=[DataRequired()])
    name = StringField(label="Name", validators=[DataRequired(), Length(min=2, max=20)])
    image_link = StringField(label="Image Link")
    description = StringField(label="Description")
    height = StringField(label="Height", validators=[Length(max=20)])
    weight = StringField(label="Weight", validators=[Length(max=20)])
    category = StringField(label="Category", validators=[Length(max=20)])
    ability = StringField(label="Ability", validators=[Length(max=20)])

    def validate_name(form, field):
        if exists_pokemon_with_name(field.data):
            raise ValidationError('Already exists pokemon with such a name.')
        
    def validate_pokemon_id(form, field):
        pokemon_id = int(field.data)
        if exists_pokemon_with_pokemon_id(pokemon_id=pokemon_id):
            raise ValidationError('Already exists pokemon with such a pokemon_id.')
        

class EditPokemonForm(FlaskForm):
    pokemon_id = IntegerField(label='Pokedox_ID', validators=[DataRequired()])
    name = StringField(label="Name", validators=[DataRequired(), Length(min=2, max=20)])
    image_link = StringField(label="Image Link")
    description = StringField(label="Description")
    height = StringField(label="Height", validators=[Length(max=20)])
    weight = StringField(label="Weight", validators=[Length(max=20)])
    category = StringField(label="Category", validators=[Length(max=20)])
    ability = StringField(label="Ability", validators=[Length(max=20)])

    def __init__(self, pokemon_pk, formdata=..., **kwargs):
        self.pokemon_pk = pokemon_pk
        super().__init__(formdata, **kwargs)

    def validate_name(form, field):
        if exists_pokemon_with_name(field.data, pokemon_pk=form.pokemon_pk):
            raise ValidationError('Already exists pokemon with such a name.')
        
    def validate_pokemon_id(form, field):
        pokemon_id = int(field.data)
        if exists_pokemon_with_pokemon_id(pokemon_id, pokemon_pk=form.pokemon_pk):
            raise ValidationError('Already exists pokemon with such a pokemon_id.')



