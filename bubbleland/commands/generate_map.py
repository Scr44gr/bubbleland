from arepy.asset_store import AssetStore
from arepy.engine.renderer.renderer_2d import Color, Rect, Renderer2D

from bubbleland import config

MAP_WIDTH = 1000
MAP_HEIGHT = 1000
TILE_SIZE = 32
SCREEN_SIZE = (config.RESOLUTION[0], config.RESOLUTION[1])
WALL_WIDTH = 32
WALL_HEIGHT = 32


def generate_map(renderer: Renderer2D, asset_store: AssetStore):
    render_texture = asset_store.create_render_texture(
        renderer, "procedural_lvl", MAP_WIDTH, MAP_HEIGHT
    )
    renderer.bind_render_texture(render_texture)
    renderer.clear(config.CLEAR_COLOR)

    wall_texture = asset_store.get_texture("wall_horizontal")

    ground_texture = asset_store.get_texture("ground")
    texture_color = Color(255, 255, 255, 255)

    for y in range(0, MAP_HEIGHT, TILE_SIZE):
        for x in range(0, MAP_WIDTH, TILE_SIZE):
            renderer.draw_texture(
                ground_texture,
                Rect(0, 0, TILE_SIZE, TILE_SIZE),
                Rect(x, y, TILE_SIZE, TILE_SIZE),
                texture_color,
            )

    for x in range(0, MAP_WIDTH, WALL_WIDTH):
        renderer.draw_texture(
            wall_texture,
            Rect(0, 0, WALL_WIDTH, WALL_HEIGHT),
            Rect(x, 0, WALL_WIDTH, WALL_HEIGHT),
            texture_color,
        )

    renderer.unbind_render_texture()
    return render_texture


def render_generated_map(
    renderer: Renderer2D,
    asset_store: AssetStore,
):
    render_texture = asset_store.get_texture("procedural_lvl")

    renderer.draw_texture(
        render_texture,
        Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]),
        Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]),
        config.WHITE_COLOR,
    )
