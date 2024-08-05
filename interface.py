import pyinputplus as pyip

from pokemon_db import PokemonDB

HEADER = r"""                                  ,'\
    _.----.        ____         ,'  _\   ___    ___     ____
_,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`.
\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  |
 \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  |
   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |
    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     |
     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    |
      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   |
       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   |
        \_.-'       |__|    `-._ |              '-.|     '-.| |   |
                                `'                            '-._| """
pokemon_data = PokemonDB()
pokemon_data.load_data()
while True:
    try:
        user_choice = int(input(f"Welcome to the pokedex App. What would you like to do?"
                                "\n1. Search Pokemon"
                                "\n2. See Saved Pokemon"
                                "\n3. Delete Pokemon"
                                "\n4. Change User"
                                "\n5. Log out"
                                "\nPlease make selection: "))
        print()
    except ValueError:
        print("Invalid input. Try again\n")
        continue
    else:

        if user_choice == 1:
            save_pending = {}
            while True:
                name = input("Enter the name of the Pokemon, 'm' for Main Menu: ")
                if name == 'm' or name == '':
                    break
                pokemon = pokemon_data.find_pokemon(name)
                if pokemon is None:
                    print("Pokemon not found. Please try again.")
                    continue
                pokemon_data.show_details(pokemon)
                user_choice = input("\nWould you like to save this pokemon?(Y/N): ")
                if user_choice.upper() == "Y":
                    save_pending[name.title()] = pokemon
                    user_choice = input("Search more pokemon?(Y/N): ")
                    if user_choice.upper() != "Y":
                        break
                else:
                    break
            pokemon_data.add_to_faves(save_pending)
            pokemon_data.save_data()
            print(f"\nThe following pokemon were added:{', '.join(save_pending.keys())}\n")

        if user_choice == 2:
            # Check to see if user has any pokemon saved. If not, send user back to main menu/loop
            if not pokemon_data.fav_pokemon:
                print("No pokemon saved yet!")
                continue
            print(f"\nThe user has saved the following pokemon: {', '.join(pokemon_data.fav_pokemon.keys())}."
                  f"\nHere are the details for each pokemon:\n{'*' * 50}")
            # Iterate fav_pokemon dictionary and print detail string for each pokemon
            for pokemon in pokemon_data.fav_pokemon.values():
                pokemon_data.show_details(pokemon)
                print('*' * 50)
            print()

        if user_choice == 3:
            while True:
                pokemon_keys = list(pokemon_data.fav_pokemon.keys())
                print("The following pokemon are in your pokedex: ")
                for index, pokemon in enumerate(pokemon_keys, 1):
                    print(f"{index}: {pokemon}")
                user_choice = pyip.inputNum(prompt="\nWhich pokemon would you like to delete? , '0' to cancel: ", min=0, max=len(pokemon_keys))
                if user_choice == 0:
                    break
                else:
                    del pokemon_data.fav_pokemon[pokemon_keys[user_choice - 1]]
                    print(f"{pokemon_keys[user_choice - 1]} deleted.")
                    pokemon_data.save_data()
                    if not pokemon_data.fav_pokemon:
                        break
                    else:
                        user_choice = pyip.inputYesNo(prompt="Delete More?(yes/no): ")
                        if user_choice == "no":
                            break

