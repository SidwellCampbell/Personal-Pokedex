import requests


def find_pokemon(pokemon: str):
    """Search for Pokemon using string. Return dictionary of request results"""
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    pokemon_dict = response.json()
    return pokemon_dict


def show_pokemon(pokemon_info: dict):
    """Iterate pokemon dictionary for pertinent details"""
    print(f"Pokemon name: {pokemon_info['name'].title()}")
    # Create a list with all the types
    types = [type_info['type']['name'].title() for type_info in pokemon_info['types']]
    print(types)


pokemon = find_pokemon("bulbasaur")
show_pokemon(pokemon)
