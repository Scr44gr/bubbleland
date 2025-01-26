import math

from arepy.bundle.components import Camera2D, RigidBody2D, Sprite, Transform
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.engine.input import Input
from arepy.engine.renderer.renderer_2d import Renderer2D
from arepy.math import Vec2

from bubbleland.components import KeyboardControlled, Pickable, Weapon

WEAPON_Y_OFFSET = 15
WEAPON_X_OFFSET = 5
ROTATION_OFFSET = 10


def weapon_follow_player_system(
    weapon_query: Query[Entities, With[Transform, RigidBody2D, Weapon]],
    player_query: Query[Entities, With[Transform, RigidBody2D, KeyboardControlled]],
    input: Input,
    renderer: Renderer2D,
):
    """
    Makes the weapon follow the player and rotate towards the mouse position.
    """
    player_entity = next(iter(player_query.get_entities()), None)
    if not player_entity:
        return

    player_transform = player_entity.get_component(Transform)
    player_camera = player_entity.get_component(Camera2D)
    player_sprite = player_entity.get_component(Sprite)

    mouse_screen_pos = input.get_mouse_position()
    mouse_world_pos = renderer.screen_to_world(mouse_screen_pos, player_camera)

    for weapon_entity in weapon_query.get_entities():
        if (
            weapon_entity.has_component(Pickable)
            and not weapon_entity.get_component(Pickable).grabbed
        ):
            continue

        weapon_transform = weapon_entity.get_component(Transform)
        weapon_sprite = weapon_entity.get_component(Sprite)

        weapon_transform.position.x = (
            player_transform.position.x
            - WEAPON_X_OFFSET
            - (weapon_sprite.src_rect[2] / 2)
            if weapon_sprite.flipped
            else player_transform.position.x - WEAPON_X_OFFSET
        )
        weapon_transform.position.y = (
            player_transform.position.y - WEAPON_Y_OFFSET
            if weapon_sprite.flipped
            else player_transform.position.y
            - WEAPON_Y_OFFSET
            + weapon_sprite.src_rect[3]
        )
        direction = (
            weapon_transform.position
            - Vec2(
                mouse_world_pos[0],
                (
                    mouse_world_pos[1] - WEAPON_Y_OFFSET
                    if weapon_sprite.flipped
                    else mouse_world_pos[1] + WEAPON_Y_OFFSET
                ),
            )
        ).normalize()

        angle = math.atan2(direction.y, direction.x)
        angle_degrees = math.degrees(angle)
        weapon_transform.rotation = angle_degrees

        if abs(angle_degrees) > 90:
            if not weapon_sprite.flipped:
                weapon_sprite.src_rect = (
                    weapon_sprite.src_rect[0],
                    weapon_sprite.src_rect[1],
                    weapon_sprite.src_rect[2],
                    -weapon_sprite.src_rect[3],
                )
                weapon_sprite.flipped = True
                player_sprite.src_rect = (
                    player_sprite.src_rect[0],
                    player_sprite.src_rect[1],
                    abs(player_sprite.src_rect[2]),
                    player_sprite.src_rect[3],
                )
                player_sprite.flipped = True

        else:
            if weapon_sprite.flipped:
                weapon_sprite.src_rect = (
                    weapon_sprite.src_rect[0],
                    weapon_sprite.src_rect[1],
                    weapon_sprite.src_rect[2],
                    abs(weapon_sprite.src_rect[3]),
                )
                weapon_sprite.flipped = False
                player_sprite.src_rect = (
                    player_sprite.src_rect[0],
                    player_sprite.src_rect[1],
                    -player_sprite.src_rect[2],
                    player_sprite.src_rect[3],
                )
                player_sprite.flipped = False
