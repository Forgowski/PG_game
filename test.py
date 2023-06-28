import pytest
from player import Player
from enemy import Enemy


def test_player_update():
    player = Player("knight")
    player.update()
    assert player.counter == 2


def test_player_update_hp():
    player = Player("knight")
    player.hp = 100
    player.update_hp(50)
    assert player.hp == 50


def test_player_update_exp_bar():
    player = Player("knight")
    player.exp = 50
    player.exp_to_next_level = 100
    player.update_exp_bar(25)
    assert player.exp == 75
    assert player.lvl == 1


def test_player_change_position():
    player = Player("knight")
    player.change_position(100, 200)
    assert player.rect.x == 100
    assert player.rect.y == 200


def test_player_is_player_moved():
    player = Player("knight")
    assert player.is_player_moved(0, 0, 0, 0) == False
    assert player.is_player_moved(10, 10, 0, 0) == True


def test_player_update_hp_bar():
    player = Player("knight")
    player.stats.max_hp = 100
    player.hp = 50
    player.update_hp_bar()
    assert player.hp_bar.width == 50


def test_player_death_animation():
    player = Player("knight")
    player.is_alive = False
    player.death_animation()
    assert player.current_death_image == 1
    assert player.image == player.death_images[0]


def test_player_revive():
    player = Player("knight")
    player.is_alive = False
    player.hp = 0
    player.revive()
    assert player.is_alive == True
    assert player.hp == 1


def test_player_fight_simulation():
    player = Player("knight")
    enemy = Enemy(1)
    player.fight_simulation(enemy)
    assert player.is_alive == False or enemy.is_alive == False


# Dodaj inne testy dla pozostałych funkcji i metod w klasie Player

if __name__ == '__main__':
    pytest.main()
