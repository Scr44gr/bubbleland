from arepy import ArepyEngine
from arepy.bundle.components import RigidBody2D, Sprite, Transform
from arepy.ecs import Entity
from arepy.math import Vec2

from bubbleland.components import Collider, EnemyAI, Health


def spawn_enemy(engine: ArepyEngine, position: Vec2) -> Entity:
    world = engine.worlds.get("bubbleland_testing")
    assert world is not None
    entity = (
        world.create_entity()
        .with_component(
            Transform(
                position=position,
                scale=Vec2(4, 4),
                rotation=0.0,
            )
        )
        .with_component(
            RigidBody2D(
                velocity=Vec2(0, 0),
            )
        )
        .with_component(
            Sprite(asset_id="enemy_idle", src_rect=(0, 0, 32, 32), z_index=2)
        )
        .with_component(Collider(width=32, height=32, radius=32))
        .with_component(EnemyAI(speed=25, attack_range=100, amplitude=10))
        .with_component(Health(150))
    ).build()
    return entity
