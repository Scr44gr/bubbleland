from arepy import ArepyEngine
from arepy.ecs.systems import SystemPipeline
from arepy.math import Vec2

from bubbleland import commands, config
from bubbleland.systems import (
    collision_system,
    keyboard_control_system,
    movement_system,
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
    asset_store.load_texture(game.renderer, "bunny", f"{config.ASSET_PATH}/bunny.png")
    # Spawn a weapon in a random position
    # commands.spawn_weapon(game, Vec2(512, 255))

    game.add_system(SystemPipeline.RENDER, render_system)
    game.add_system(SystemPipeline.INPUT, keyboard_control_system)
    game.add_system(SystemPipeline.UPDATE, movement_system)
    game.add_system(SystemPipeline.UPDATE, collision_system)
    game.add_system(
        SystemPipeline.UPDATE,
        weapon_follow_player_system,
    )
    game.add_system(
        SystemPipeline.RENDER_UI,
        ui_debug_system,
    )

    game.run()
