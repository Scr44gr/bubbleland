from arepy import ArepyEngine
from arepy.bundle.components import RigidBody2D, Sprite, Transform
from arepy.ecs import Entity
from arepy.engine.renderer import Color
from arepy.math import Vec2

from bubbleland.components import Collider, Pickable, PickUp, SimpleRectangle, Weapon


def spawn_ammo(engine: ArepyEngine, position: Vec2) -> Entity:
    entity = (
        engine.create_entity()
        .with_component(
            Transform(
                position=position,
                scale=Vec2(1, 1),
                rotation=0.0,
            )
        )
        .with_component(
            RigidBody2D(
                velocity=Vec2(0, 0),
            )
        )
        .with_component(Sprite(asset_id="ammo", src_rect=(0, 0, 16, -16), z_index=2))
        .with_component(
            PickUp(
                name="Ammo",
            )
        )
        .with_component(Collider(width=16, height=16, radius=(16 + 16) // 2))
    ).build()

    return entity


def increase_bullet_count(weapon_entity: Entity):
    weapon_component = weapon_entity.get_component(Weapon)
    if weapon_component:
        weapon_component.current_bullet_count = min(
            weapon_component.current_bullet_count + 24,
            weapon_component.max_bullet_count,
        )
