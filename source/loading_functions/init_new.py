"""
Name: Initialize New
Function: Generates a new game state, used for creating new floors and new games
Notes:
"""

from source.data_banks.equipment_slots import EquipmentSlots
from source.data_banks.game_states import GameStates
from source.data_banks.render_order import RenderOrder
from source.game_entities.components.combat_data import CombatData
from source.game_entities.components.crosshair import Crosshair
from source.game_entities.components.equipment import Equipment
from source.game_entities.components.equippable import Equippable
from source.game_entities.components.inventory import Inventory
from source.game_entities.components.level import Level
from source.game_entities.entity import Entity
from source.map_engine.game_map import GameMap
from source.rendering_files.user_interface.console import Console


def get_constants():
    window_title = 'Depths_Game'

    screen_size = (1280, 768)
    font_size = 26
    map_width = 40
    map_height = 40

    max_room_size = 8
    min_room_size = 6
    max_rooms = 10

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    max_items_per_room = 2

    constants = {
        'window_title': window_title,
        'screen_size': screen_size,
        'font_size': font_size,
        'map_width': map_width,
        'map_height': map_height,
        'max_room_size': max_room_size,
        'min_room_size': min_room_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
    }

    return constants


def get_game_variables(constants):
    fighter_component = CombatData(hp=100, defense=1, attack=2)
    inventory_component = Inventory(36)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, 'player', 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    combat_data=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component)

    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, attack_bonus=2)

    crosshair_component = Crosshair(player)
    crosshair = Entity(player.x, player.y, 'crosshair', 'Crosshair', blocks=False, render_order=RenderOrder.CROSSHAIR,
                       crosshair=crosshair_component)

    dagger = Entity(0, 0, 'dagger', 'Dagger', equippable=equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    entities = [player, crosshair]

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.generate_map(constants['max_rooms'], constants['min_room_size'], constants['max_room_size'],
                          constants['map_width'], constants['map_height'], player, entities)

    console = Console(constants['font_size'], player)

    game_state = GameStates.PLAYERS_TURN

    return player, entities, crosshair, game_map, game_state, console
