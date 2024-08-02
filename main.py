import json
from pathlib import Path

import requests

fav_pokemon = {}
def find_pokemon(pokemon: str):
    """Search for Pokemon using string. Return dictionary of request results"""
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    pokemon_dict = response.json()
    return pokemon_dict


def show_details(pokemon_info: dict):
    """Iterate pokemon dictionary for pertinent details"""

    print(f"Pokemon name: {pokemon_info['name'].title()}\n")
    # Create a list with all the types
    types = [type_info['type']['name'].title() for type_info in pokemon_info['types']]
    print(f"Pokemon type(s): ", end="")
    # Print types, seperated by comma
    print(*types, sep=", ", end="\n\n")
    stat_dict = {}
    print("Pokemon abilities: ")
    for ability in pokemon_info['abilities']:
        ability_dict = requests.get(ability['ability']['url']).json()
        name = ability_dict['name'].title()
        desc = None
        for entry in ability_dict['effect_entries']:
            if entry['language']['name'] == "en":
                desc = entry['short_effect']
        print(f"\tname: {name}\n\tdescription: {desc}\n")

        # Add stats to a dictionary and print it
    for stat_info in pokemon_info['stats']:
        stat_dict[stat_info['stat']['name']] = stat_info['base_stat']
    print("Pokemon stats: ", end="")
    for stat, value in stat_dict.items():
        print(f"{stat.title()}:{value}\t", end="")
    print()


def add_to_faves(*poke_to_add):
    for pokemon in poke_to_add:
        fav_pokemon[pokemon['name']] = poke_to_add
    path = Path("fav_pokemon.json")
    path.write_text(json.dumps(fav_pokemon))

def load_favs():
    path = Path("fav_pokemon.json")
    if path.exists():
        fav_pokemon = json.loads(path.read_text())
        return fav_pokemon


pikachu = find_pokemon("pikachu")
ditto = find_pokemon("ditto")
bulba = find_pokemon("bulbasaur")
# show_details(bulba)
add_to_faves(bulba, ditto, pikachu)
favs = load_favs()
print(favs.keys())


