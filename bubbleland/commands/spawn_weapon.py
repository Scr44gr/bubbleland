from arepy import ArepyEngine
from arepy.bundle.components import RigidBody2D, Sprite, Transform
from arepy.ecs import Entity
from arepy.engine.renderer import Color
from arepy.math import Vec2

from bubbleland.components import Collider, Pickable, SimpleRectangle, Weapon


def spawn_weapon(engine: ArepyEngine, mouse_pos: Vec2) -> Entity:
    entity = (
        engine.create_entity()
        .with_component(
            Transform(
                position=mouse_pos,
                scale=Vec2(4, 4),
                rotation=0.0,
            )
        )
        .with_component(RigidBody2D())
        .with_component(
            Sprite(asset_id="bunny", src_rect=(0, 0, 32, 32), z_index=0)
        )  # TODO: Change asset_id
        .with_component(
            SimpleRectangle(width=14, height=8, color=Color(255, 0, 0, 255))
        )
        .with_component(Weapon(name="Weapon", fire_rate=0.5, cooldown=1.0))
        .with_component(
            Pickable(
                name="Gun",
            )
        )
        .with_component(Collider(width=14, height=8, radius=7))
    ).build()

    return entity
