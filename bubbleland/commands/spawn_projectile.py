from arepy import ArepyEngine
from arepy.bundle.components import Camera2D, RigidBody2D, Sprite, Transform
from arepy.ecs import Entity
from arepy.engine.renderer import Color
from arepy.math import Vec2

from bubbleland.components import Collider, Projectile, SimpleRectangle


def shoot_projectile(
    engine: ArepyEngine, position: Vec2, angle: float, direction: Vec2
) -> Entity:
    world = engine.worlds.get("bubbleland_testing")
    assert world is not None
    entity = (
        world.create_entity()
        .with_component(
            Transform(
                position=position,
                scale=Vec2(4, 4),
                rotation=angle,
            )
        )
        .with_component(
            RigidBody2D(
                velocity=Vec2(direction.x, direction.y) * 500,
                max_velocity=500,
                acceleration=250,
            )
        )
        .with_component(
            Sprite(asset_id="yellow_bullet", src_rect=(0, 0, 4, 4), z_index=0)
        )
        .with_component(Collider(width=4, height=4, radius=2))
        .with_component(Projectile(direction=direction, life_time=2, damage=10))
    ).build()
    return entity
