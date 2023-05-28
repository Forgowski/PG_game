import pickle
import easygui
from player import Player
from equipment import create_item
from stats import Stats


def save_game(player):
    items_list = []
    for each in player.equipment.items:
        name, amount = each.name, each.amount
        items_list.append((name, amount))
    game_state = {
        "hero_type": player.hero_type,
        "lvl": player.lvl,
        "max_hp": player.stats.max_hp,
        "agility": player.stats.agility,
        "attack": player.stats.attack_power,
        "critical": player.stats.critical_damage_chance,
        "opponents_level": player.opponents_level,
        "upgrade_points": player.stats.upgrade_points,
        'hp': player.hp,
        "exp": player.exp,
        "exp_to_next_level": player.exp_to_next_level,
        "items": items_list
    }

    with open('savegame.dat', 'wb') as file:
        pickle.dump(game_state, file)


def load_game():
    try:
        with open('savegame.dat', 'rb') as file:
            game_state = pickle.load(file)
            player = Player(game_state["hero_type"])
            player.lvl = game_state["lvl"]
            player.stats = Stats(game_state["max_hp"], game_state["attack"], game_state["agility"],
                                 game_state["critical"])
            player.opponents_level = game_state["opponents_level"]
            player.hp = game_state["hp"]
            player.exp = game_state["exp"]
            player.exp_to_next_level = game_state["exp_to_next_level"]
            player.stats.upgrade_points = game_state["upgrade_points"]
            for each in game_state["items"]:
                if each[0] == "gold":
                    player.equipment.add_gold(each[1])
                else:
                    for i in range(each[1]):
                        player.equipment.add_item(create_item(each[0]))

            return 1, player
    except:
        easygui.msgbox("You have not save any game", title="Error")
        return 0, 0
