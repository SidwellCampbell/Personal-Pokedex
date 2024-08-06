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

# print("Which user's pokedex would you like to load?: ")
# for index, user in enumerate(pokemon_data.users, start=1):
#     print(f"{index}: {user}")


#TODO
# Add in checks to avoid overwriting users with same name
# Add in feature to see evolutionary options for pokemon

pokemon_data = PokemonDB()
pokemon_data.load_data()


def main_menu() -> int:
    """Show main menu and return user input"""
    user_choice = pyip.inputNum(prompt=f"Welcome to the Pokedex App. What would you like to do?"
                                       f"\n1. Add user"
                                       f"\n2. Load user"
                                       f"\n3. Delete user"
                                       f"\n4. Close app"
                                       f"\nPlease make a selection: ", min=1, max=4)

    return user_choice


def get_user_info(user_input: int) -> str:
    """Add, delete, or select user. Returns user's name or blank string"""
    if user_input == 1:
        while True:
            new_user = input("What is the user's name: ").title()
            if new_user in pokemon_data.fav_pokemon:
                print("User with that name exists already. Choose another!")
            else:
                pokemon_data.add_user(new_user)
                print(f"Hey {new_user.title()}!")
                break
        return new_user
    elif user_input == 2:
        while True:
            possible_user = input("Which user's pokedex would you like to load?('quit' for main menu): ").title()
            if possible_user == 'Quit':
                return ''
            elif possible_user in pokemon_data.users:
                return possible_user
            print("User not found. Please try again")
    elif user_input == 3:
        while True:
            to_delete = input("Which user would you like to delete?:('quit' for main menu)").title()
            if to_delete == "Quit":
                return ''
            if to_delete in pokemon_data.users:
                pokemon_data.delete_user(to_delete)
                print(f"user {to_delete} has been deleted")
                return ''
            else:
                print("User not found. Try again.")


def user_menu() -> int:
    user_input = pyip.inputNum(prompt=f"What would you like to do next?"
                                      "\n1. Search Pokemon"
                                      "\n2. See Saved Pokemon"
                                      "\n3. Delete Pokemon"
                                      "\n4. Change User"
                                      "\n5. Log out"
                                      "\nPlease make selection: ", min=1, max=5)
    return user_input


def process_user_input(user_choice: int, selected_user: str) -> bool:
    """Process user selection and return True if selection successfully processed"""
    completed = True
    if user_choice == 1:
        save_pending = {}
        while True:
            name = pyip.inputStr(prompt="Enter the name of the Pokemon, 'm' for Previous Menu: ", blank=True)
            if name == 'm' or name == '':
                break
            pokemon = pokemon_data.find_pokemon(name)
            if pokemon is None:
                print("Pokemon not found. Please try again.")
                continue
            pokemon_data.show_details(pokemon)
            save = pyip.inputYesNo(prompt="\nWould you like to save this pokemon?(yes/no): ")
            if save == "yes":
                save_pending[name.title()] = pokemon
            search_more = pyip.inputYesNo(prompt="Search more pokemon?(yes/no): ")
            if search_more != "yes":
                break
        pokemon_data.add_to_faves(save_pending, selected_user)
        print(f"\nThe following pokemon were added:{', '.join(save_pending.keys())}\n")

    if user_choice == 2:
        # Check to see if user has any pokemon saved. If not, send user back to main menu/loop
        if not pokemon_data.fav_pokemon[selected_user]:
            print("No pokemon saved yet!")
            return completed
        print(f"\nThe user has saved the following pokemon: {', '.join(pokemon_data.fav_pokemon[user].keys())}."
              f"\nHere are the details for each pokemon:\n{'*' * 50}")
        # Iterate fav_pokemon dictionary and print detail string for each pokemon
        for pokemon in pokemon_data.fav_pokemon[selected_user].values():
            pokemon_data.show_details(pokemon)
            print('*' * 50)
        print()
        completed = True

    if user_choice == 3:
        while True:
            pokemon_keys = list(pokemon_data.fav_pokemon[selected_user].keys())
            print("The following pokemon are in your pokedex: ")
            for index, pokemon in enumerate(pokemon_keys, 1):
                print(f"{index}: {pokemon}")
            delete_which = pyip.inputNum(prompt="\nWhich pokemon would you like to delete? , '0' to cancel: ", min=0,
                                         max=len(pokemon_keys))
            if delete_which == 0:
                break
            else:
                pokemon_deleted = pokemon_keys[user_choice - 1]
                delete_pokemon(selected_user, pokemon_deleted)
                print(f"{pokemon_deleted} deleted.")
                if pokemon_data.fav_pokemon[selected_user]:
                    delete_more = pyip.inputYesNo(prompt="Delete More?(yes/no): ")
                    if delete_more == 'no':
                        break
                break

    if user_choice == 5:
        print(f"{selected_user} successfully logged out.")
        completed = False
        return completed

    return completed


def delete_pokemon(selected_user: str, pokemon: str):
    del pokemon_data.fav_pokemon[selected_user][pokemon]
    pokemon_data.save_data()


while True:
    main_selection = main_menu()
    if main_selection == 4:
        break
    user = get_user_info(main_selection)
    if user == '':
        continue
    else:
        while True:
            choice = user_menu()
            processed = process_user_input(choice, user)
            if not processed:
                break
            # All selections should take user back to user menu, unless user requests back to main menu.
            # Main menu will represent function returning False. All other values will return True
