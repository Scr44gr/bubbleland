from arepy import ArepyEngine
from arepy.ecs.systems import SystemPipeline

from bubbleland import config
from bubbleland.systems import (
    keyboard_control_system,
    movement_system,
    render_system,
    spawn_system,
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

    game.add_system(SystemPipeline.RENDER, render_system)
    game.add_system(SystemPipeline.INPUT, spawn_system)
    game.add_system(SystemPipeline.INPUT, keyboard_control_system)
    game.add_system(SystemPipeline.UPDATE, movement_system)
    game.run()
