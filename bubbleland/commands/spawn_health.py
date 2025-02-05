from arepy import ArepyEngine
from arepy.bundle.components import RigidBody2D, Sprite, Transform
from arepy.ecs import Entity
from arepy.engine.renderer import Color
from arepy.math import Vec2

from bubbleland.components import Collider, Health, Pickable, PickUp, SimpleRectangle


def spawn_health(engine: ArepyEngine, position: Vec2) -> Entity:
    world = engine.worlds.get("bubbleland_testing")
    assert world is not None
    entity = (
        world.create_entity()
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
        .with_component(Sprite(asset_id="health", src_rect=(0, 0, 16, 10), z_index=2))
        .with_component(
            PickUp(
                name="Health",
            )
        )
        .with_component(Collider(width=16, height=16, radius=(16 + 10) // 2))
        .with_component(Health(max_health=100, current_health=100))
    ).build()

    return entity


def increase_health(player_entity: Entity):
    player_component = player_entity.get_component(Health)
    if player_component:
        player_component.current_health = min(
            player_component.current_health + 25, player_component.max_health
        )
