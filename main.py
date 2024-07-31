import requests


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
        ability_name = ability['ability']['name']
        ability_desc = None
        ability_lookup = requests.get(f"https://pokeapi.co/api/v2/ability/{ability_name}/")
        ability_dict = ability_lookup.json()
        for entry in ability_dict['effect_entries']:
            if entry['language']['name'] == "en":
                ability_desc = entry['short_effect']
        print(f"\tname: {ability_name}\n\tdescription: {ability_desc}\n")

        # Add stats to a dictionary and print it
    for stat_info in pokemon_info['stats']:
        stat_dict[stat_info['stat']['name']] = stat_info['base_stat']
    print("Pokemon stats: ", end="")
    for stat, value in stat_dict.items():
        print(f"{stat.title()}:{value}\t", end="")
    print()







pokemon = find_pokemon("bulbasaur")
show_details(pokemon)
