from arepy import ArepyEngine
from arepy.bundle.components import RigidBody2D, Sprite, Transform
from arepy.ecs import Entity
from arepy.engine.renderer import Color
from arepy.math import Vec2

from bubbleland.components import Collider, Pickable, SimpleRectangle, Weapon


def spawn_ak48(engine: ArepyEngine, position: Vec2) -> Entity:
    entity = (
        engine.create_entity()
        .with_component(
            Transform(
                position=position,
                scale=Vec2(1, 1),
                rotation=0.0,
            )
        )
        .with_component(RigidBody2D())
        .with_component(Sprite(asset_id="ak48", src_rect=(0, 0, 34, 12), z_index=2))
        .with_component(
            Weapon(
                name="AK-48",
                fire_rate=0.1,
                cooldown=1.0,
                shake_intensity=1.5,
                shake_duration=0.1,
                dispersion_angle=25,
                max_bullet_count=48,
                current_bullet_count=48,
            )
        )
        .with_component(
            Pickable(
                name="AK-48",
            )
        )
        .with_component(Collider(width=34, height=16, radius=(34 + 16) // 2))
    ).build()

    return entity


def spawn_shotgun(engine: ArepyEngine, position: Vec2) -> Entity:
    entity = (
        engine.create_entity()
        .with_component(
            Transform(
                position=position,
                scale=Vec2(1, 1),
                rotation=0.0,
            )
        )
        .with_component(RigidBody2D())
        .with_component(Sprite(asset_id="shotgun", src_rect=(0, 0, 34, 9), z_index=2))
        .with_component(
            Weapon(
                name="Shotgun",
                fire_rate=0.5,
                cooldown=1.0,
                shake_intensity=1.7,
                shake_duration=0.1,
                dispersion_angle=15,
                max_bullet_count=8,
                current_bullet_count=8,
            )
        )
        .with_component(
            Pickable(
                name="Shotgun",
            )
        )
        .with_component(Collider(width=34, height=9, radius=(34 + -9) // 2))
    ).build()

    return entity


def spawn_sheriff(engine: ArepyEngine, position: Vec2) -> Entity:
    entity = (
        engine.create_entity()
        .with_component(
            Transform(
                position=position,
                scale=Vec2(1, 1),
                rotation=0.0,
            )
        )
        .with_component(RigidBody2D())
        .with_component(Sprite(asset_id="sheriff", src_rect=(0, 0, 20, 11), z_index=2))
        .with_component(
            Weapon(
                name="Sheriff",
                fire_rate=0.3,
                cooldown=1.0,
                shake_intensity=1.2,
                shake_duration=0.1,
                dispersion_angle=12.5,
                max_bullet_count=12,
                current_bullet_count=12,
            )
        )
        .with_component(
            Pickable(
                name="Sheriff",
            )
        )
        .with_component(Collider(width=20, height=11, radius=(20 + 11) // 2))
    ).build()

    return entity
