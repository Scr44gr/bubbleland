from arepy.asset_store import AssetStore
from arepy.bundle.components import Sprite, Transform
from arepy.ecs.query import Query, With
from arepy.ecs.registry import Entity
from arepy.engine.renderer.renderer_2d import Color, Rect, Renderer2D

from bubbleland import __version__, config
from bubbleland.components import Pickable, SimpleRectangle, Weapon

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
        # if entity has Pickable component and can be grabbed
        if entity.has_component(Pickable):
            pickable_component = entity.get_component(Pickable)
            if pickable_component.can_be_grabbed and not pickable_component.grabbed:
                draw_pickable_text(pickable_component, transform, renderer)

        # if the entity has a SimpleRectangle component, draw a rectangle
        if entity.has_component(SimpleRectangle):
            simple_rectangle = entity.get_component(SimpleRectangle)
            draw_simple_rectangle(simple_rectangle, transform, renderer)
            continue

        draw_sprite(sprite, transform, renderer, asset_store)
    renderer.end_frame()


def draw_pickable_text(
    pickble_component: Pickable,
    transform_component: Transform,
    renderer: Renderer2D,
):
    renderer.draw_text(
        pickble_component.message,
        (transform_component.position.x, transform_component.position.y - 32),
        24,
        color=Color(0, 0, 0, 255),
    )


def draw_simple_rectangle(
    simple_rectangle: SimpleRectangle,
    transform_component: Transform,
    renderer: Renderer2D,
):
    renderer.draw_rectangle_ex(
        Rect(
            transform_component.position.x,
            transform_component.position.y,
            simple_rectangle.width,
            simple_rectangle.height,
        ),
        transform_component.rotation,
        simple_rectangle.color,
    )


def draw_sprite(
    sprite: Sprite,
    transform: Transform,
    renderer: Renderer2D,
    asset_store: AssetStore,
):
    texture = asset_store.get_texture(sprite.asset_id)
    texture_size = texture.get_size()
    dst_rect = Rect(
        transform.position.x,
        transform.position.y,
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
