import pyray as pr
from arepy.asset_store import AssetStore
from arepy.bundle.components import Camera2D, Sprite, Transform
from arepy.ecs.query import Query, With
from arepy.ecs.registry import Entity
from arepy.engine.renderer.renderer_2d import Color, Rect, Renderer2D

from bubbleland import commands, config
from bubbleland.components import Health, Pickable, SimpleRectangle, Weapon

WHITE_COLOR = Color(255, 255, 255, 255)
BLACK_COLOR = Color(0, 0, 0, 255)


def render_weapon_ui(renderer: Renderer2D, weapon_component: Weapon):
    # draw at bottom rigth corner
    renderer.draw_text(
        f"Current weapon: {weapon_component.name}",
        (20, pr.get_screen_height() - 50),
        34,
        color=WHITE_COLOR,
    )
    renderer.draw_text(
        f"Ammo: {weapon_component.current_bullet_count}/{weapon_component.max_bullet_count}",
        (20, pr.get_screen_height() - 90),
        34,
        color=(
            WHITE_COLOR
            if weapon_component.current_bullet_count > 0
            else Color(255, 0, 0, 255)
        ),
    )


def render_system(
    query: Query[Entity, With[Transform, Sprite]],
    camera_query: Query[Entity, With[Camera2D]],
    renderer: Renderer2D,
    asset_store: AssetStore,
):
    camera = next(iter(camera_query.get_entities()), None)

    renderer.start_frame()
    renderer.clear(color=config.CLEAR_COLOR)
    if camera:
        camera_component = camera.get_component(Camera2D)
        camera_component.target = camera.get_component(Transform).position / 2
        renderer.update_camera(camera.get_component(Camera2D))
        renderer.begin_camera_mode(camera.get_component(Camera2D))
    commands.render_generated_map(renderer, asset_store)

    ordered_entities = sorted(
        query.get_entities(), key=lambda entity: entity.get_component(Sprite).z_index
    )
    active_weapons = [
        entity
        for entity in ordered_entities
        if entity.has_component(Pickable) and entity.get_component(Pickable).grabbed
    ]

    for entity in ordered_entities:
        transform = entity.get_component(Transform)
        sprite = entity.get_component(Sprite)

        if entity.has_component(Pickable):
            pickable_component = entity.get_component(Pickable)
            if pickable_component.can_be_grabbed and not pickable_component.grabbed:
                draw_pickable_text(pickable_component, transform, renderer, 14)

        # if the entity has a health component, draw a health bar
        if entity.has_component(Health):
            health_component = entity.get_component(Health)
            draw_health_bar(
                sprite,
                transform,
                renderer,
                health_component.current_health,
                health_component.max_health,
                25,
                5,
            )

        # if the entity has a SimpleRectangle component, draw a rectangle
        if entity.has_component(SimpleRectangle):
            simple_rectangle = entity.get_component(SimpleRectangle)
            draw_simple_rectangle(simple_rectangle, transform, renderer)
            continue

        draw_sprite(sprite, transform, renderer, asset_store)
    if camera:
        renderer.end_camera_mode()
    if active_weapons:
        render_weapon_ui(renderer, active_weapons[0].get_component(Weapon))
    renderer.end_frame()


import pyray


def draw_pickable_text(
    pickble_component: Pickable,
    transform_component: Transform,
    renderer: Renderer2D,
    font_size: int,
    font_spacing: float = 1.0,
):
    text_size: pyray.Vector2 = pyray.measure_text_ex(
        pyray.get_font_default(), pickble_component.message, font_size, font_spacing
    )

    renderer.draw_rectangle(
        Rect(
            transform_component.position.x,
            transform_component.position.y - text_size.y - 16,
            int(text_size.x),
            int(text_size.y),
        ),
        color=Color(0, 0, 0, 200),
    )

    renderer.draw_text(
        pickble_component.message,
        (
            transform_component.position.x,
            transform_component.position.y - text_size.y - 16,
        ),
        font_size,
        color=config.WHITE_COLOR,
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


def draw_health_bar(
    sprite: Sprite,
    transform: Transform,
    renderer: Renderer2D,
    health: int,
    max_health: int,
    width: int,
    height: int,
    h_offset: int = 5,
):
    health_percentage = health / max_health
    health_bar_width = health_percentage * width
    health_bar_color = Color(
        int(255 * (1 - health_percentage)), int(255 * health_percentage), 0, 255
    )

    renderer.draw_rectangle(
        Rect(
            transform.position.x - width,
            transform.position.y - height - sprite.src_rect[3] - h_offset,
            width,
            height,
        ),
        color=BLACK_COLOR,
    )

    renderer.draw_rectangle(
        Rect(
            transform.position.x - width,
            transform.position.y - height - sprite.src_rect[3] - h_offset,
            int(health_bar_width),
            height,
        ),
        color=health_bar_color,
    )
