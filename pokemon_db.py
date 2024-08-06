import json
import os.path
from pathlib import Path

import requests


class PokemonDB:

    def __init__(self):
        self.fav_pokemon = {}
        self.users = []


    def find_pokemon(self, pokemon: str):
        """Search for Pokemon using string. Return dictionary of request results"""
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        if not response:
            return None
        pokemon_dict = response.json()
        return pokemon_dict

    def show_details(self, pokemon_info: dict):
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

    def add_to_faves(self, poke_to_add: dict, user: str):
        """Iterate pokemon and add to fav pokemon dictionary."""
        if poke_to_add:
            for poke_name, poke_info in poke_to_add.items():
                # Key = Pokemon Name, Value = Pokemon info dictionary
                self.fav_pokemon[user][poke_name] = poke_info
            self.save_data()
    def load_data(self):
        """Loads favorite pokemon from saved file if it exists, if not, create file."""
        path = Path("fav_pokemon.json")
        # Check to see if file exists, and whether it's empty
        if path.exists() and os.path.getsize(path) != 0:
            self.fav_pokemon = json.loads(path.read_text())
        else:
            path.touch()
        return self.fav_pokemon


    def save_data(self):
        path = Path("fav_pokemon.json")
        # Convert fav_pokemon dictionary to json and save
        path.write_text(json.dumps(self.fav_pokemon))

    def add_user(self, username: str):
        self.users.append(username)
        self.fav_pokemon[username] = {}
        self.save_data()

    def delete_user(self, to_delete:str):
        """Delete user specified from pokemon dictionary"""
        del self.fav_pokemon[to_delete]
        self.save_data()

