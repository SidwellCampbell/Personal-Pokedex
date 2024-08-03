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
favs = pokemon_data.load_favs()
print(favs.keys())

while True:
    user_choice = int(input(f"Welcome to the pokedex App. What would you like to do?"
                        "\n1. Search Pokemon"
                        "\n2. See Saved Pokemon"
                        "\n3. Change User"
                        "\n4. Log out"
                        "\nPlease make selection: "))

    if user_choice == 1:
        save_pending = {}
        while True:
            name = input("Enter the name of the Pokemon, 'm' for Main Menu: ")
            if name == 'm':
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
                    pokemon_data.add_to_faves(save_pending)
                    print(f"The following pokemon were added:{', '.join(save_pending.keys())}")
                    break
            else:
                break









