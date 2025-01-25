import math

from arepy.bundle.components import Camera2D, RigidBody2D, Transform
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.engine.input import Input
from arepy.engine.renderer.renderer_2d import Renderer2D
from arepy.math import Vec2

from bubbleland.components import KeyboardControlled, Pickable, Weapon


def weapon_follow_player_system(
    weapon_query: Query[Entities, With[Transform, RigidBody2D, Weapon]],
    player_query: Query[Entities, With[Transform, RigidBody2D, KeyboardControlled]],
    input: Input,
    renderer: Renderer2D,
):
    """Weapon follow player and rotate towards the mouse."""
    player_entity = next(iter(player_query.get_entities()), None)

    if not player_entity:
        return

    player_transform = player_entity.get_component(Transform)

    for current_weapon in weapon_query.get_entities():
        weapon_transform = current_weapon.get_component(Transform)

        if (
            current_weapon.has_component(Pickable)
            and not current_weapon.get_component(Pickable).grabbed
        ):
            continue

        weapon_transform.position = player_transform.position
