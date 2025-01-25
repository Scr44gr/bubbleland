from arepy.asset_store import AssetStore
from arepy.bundle.components import Sprite, Transform
from arepy.ecs.query import Query, With
from arepy.ecs.registry import Entity
from arepy.engine.renderer.renderer_2d import Color, Rect, Renderer2D

from bubbleland import __version__, config
from bubbleland.components import SimpleRectangle
from bubbleland.config import RESOLUTION, WINDOW_TITLE

GAME_DISPLAY_VERSION_TEXT = f"{WINDOW_TITLE} v{__version__}"
GAME_DISPLAY_VERSION_TEXT_SIZE = 20
GAME_DISPLAY_VERSION_TEXT_POSITION = (
    GAME_DISPLAY_VERSION_TEXT_SIZE,
    RESOLUTION[1] - GAME_DISPLAY_VERSION_TEXT_SIZE * 1.5,
)
GAME_DISPLAY_VERSION_TEXT_COLOR = Color(0, 0, 0, 255)
WHITE_COLOR = Color(255, 255, 255, 255)


def render_system(
    query: Query[Entity, With[Transform, Sprite]],
    renderer: Renderer2D,
    asset_store: AssetStore,
):
    renderer.start_frame()
    renderer.clear(color=config.CLEAR_COLOR)

    for entity in query.get_entities():
        transform = entity.get_component(Transform)
        position = transform.position
        sprite = entity.get_component(Sprite)

        # if the entity has a SimpleRectangle component, draw a rectangle
        if entity.has_component(SimpleRectangle):
            simple_rectangle = entity.get_component(SimpleRectangle)
            renderer.draw_rectangle_ex(
                Rect(
                    position.x,
                    position.y,
                    simple_rectangle.width,
                    simple_rectangle.height,
                ),
                transform.rotation,
                simple_rectangle.color,
            )
            continue

        # Otherwise, draw a sprite
        texture = asset_store.get_texture(sprite.asset_id)
        texture_size = texture.get_size()
        dst_rect = Rect(
            position.x,
            position.y,
            int(texture_size[0]),
            int(texture_size[1]),
        )
        src_rect = Rect(
            float(sprite.src_rect[0]),
            float(sprite.src_rect[1]),
            int(sprite.src_rect[2]),
            int(sprite.src_rect[3]),
        )
        renderer.draw_texture_ex(
            texture,
            src_rect,
            dst_rect,
            rotation=transform.rotation,
            color=WHITE_COLOR,
        )
    renderer.draw_fps(
        position=(GAME_DISPLAY_VERSION_TEXT_SIZE, GAME_DISPLAY_VERSION_TEXT_SIZE)
    )
    renderer.draw_text(
        GAME_DISPLAY_VERSION_TEXT,
        position=GAME_DISPLAY_VERSION_TEXT_POSITION,
        font_size=GAME_DISPLAY_VERSION_TEXT_SIZE,
        color=GAME_DISPLAY_VERSION_TEXT_COLOR,
    )
    renderer.end_frame()
