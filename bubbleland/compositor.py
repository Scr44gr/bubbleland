from arepy import ArepyEngine
from arepy.ecs.systems import SystemPipeline

from bubbleland import asset_loader, commands, config
from bubbleland.systems import (
    bullet_collision_system,
    camera_shaking_system,
    collision_system,
    enemy_ai_system,
    keyboard_control_system,
    movement_system,
    pickeable_system,
    recolectable_system,
    render_system,
    ui_debug_system,
    weapon_follow_player_system,
)


def main():
    game = ArepyEngine()
    game.window_width = config.RESOLUTION[0]
    game.window_height = config.RESOLUTION[1]
    game.title = config.WINDOW_TITLE
    game.max_frame_rate = config.MAX_FRAME_RATE
    game.fullscreen = config.FULLSCREEN
    game.vsync = config.VSYNC
    game.init()

    # load assets
    asset_store = game.get_asset_store()
    asset_loader.load_player_graphics(game, asset_store)
    asset_loader.load_enemy_graphics(game, asset_store)
    asset_loader.load_weapon_graphics(game, asset_store)
    asset_loader.load_bullet_graphics(game, asset_store)
    asset_loader.load_tilemap_graphics(game, asset_store)
    asset_loader.load_item_graphics(game, asset_store)
    asset_loader.load_shoot_sounds(game, asset_store)

    # generate map
    commands.generate_map(game.renderer, game.get_asset_store())
    world = game.create_world("bubbleland_testing")

    world.add_system(SystemPipeline.RENDER, render_system)
    world.add_system(SystemPipeline.INPUT, keyboard_control_system)
    world.add_system(SystemPipeline.UPDATE, movement_system)
    world.add_system(SystemPipeline.UPDATE, collision_system)
    world.add_system(SystemPipeline.UPDATE, camera_shaking_system)
    world.add_system(SystemPipeline.UPDATE, bullet_collision_system)
    world.add_system(SystemPipeline.UPDATE, enemy_ai_system)
    world.add_system(SystemPipeline.UPDATE, pickeable_system)
    world.add_system(SystemPipeline.UPDATE, recolectable_system)

    world.add_system(
        SystemPipeline.UPDATE,
        weapon_follow_player_system,
    )
    world.add_system(
        SystemPipeline.RENDER_UI,
        ui_debug_system,
    )

    game.set_current_world("bubbleland_testing")

    game.run()
