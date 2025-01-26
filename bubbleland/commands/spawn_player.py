from arepy import ArepyEngine
from arepy.bundle.components import Camera2D, RigidBody2D, Sprite, Transform
from arepy.ecs import Entity
from arepy.math import Vec2

from bubbleland.components import (
    Collider,
    KeyboardControlled,
    SimpleRectangle,
    WalkAnimation,
)


def spawn_player(engine: ArepyEngine, mouse_pos: Vec2) -> Entity:
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
        .with_component(Sprite(asset_id="bunny", src_rect=(0, 0, 32, 32), z_index=0))
        .with_component(SimpleRectangle(width=16, height=32))
        .with_component(KeyboardControlled())
        .with_component(WalkAnimation())
        .with_component(Collider(width=32, height=32, radius=16))
        .with_component(
            Camera2D(
                offset=Vec2(0, 0),
                zoom=1.2,
                rotation=0.0,
                target=Vec2(0, 0),
            )
        )
    ).build()
    # add a camera to the renderer
    engine.renderer.add_camera(entity.get_component(Camera2D))
    return entity
