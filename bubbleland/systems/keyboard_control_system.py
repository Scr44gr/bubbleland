import math

from arepy.bundle.components import RigidBody2D, Transform
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.engine.input import Input
from arepy.engine.renderer.renderer_2d import Renderer2D
from arepy.math import Vec2

from bubbleland.components import KeyboardControlled, WalkAnimation


def keyboard_control_system(
    query: Query[
        Entities, With[RigidBody2D, Transform, KeyboardControlled, WalkAnimation]
    ],
    input: Input,
    renderer: Renderer2D,
):
    """Moves entities based on keyboard input."""
    delta_time = renderer.get_delta_time()

    for entity in query.get_entities():
        rigid_body = entity.get_component(RigidBody2D)
        keyboard_controlled = entity.get_component(KeyboardControlled)
        transform = entity.get_component(Transform)
        walk_animation = entity.get_component(WalkAnimation)

        target_velocity = Vec2(0, 0)

        if input.is_key_down(keyboard_controlled.up_key):
            target_velocity.y = -1
        elif input.is_key_down(keyboard_controlled.down_key):
            target_velocity.y = 1

        if input.is_key_down(keyboard_controlled.left_key):
            target_velocity.x = -1
        elif input.is_key_down(keyboard_controlled.right_key):
            target_velocity.x = 1

        target_velocity_length = abs(target_velocity)

        if target_velocity_length > 0:
            target_velocity.normalize()

        if target_velocity_length > 0:
            rigid_body.velocity = rigid_body.velocity.lerp(
                target_velocity * rigid_body.max_velocity,
                rigid_body.acceleration * delta_time,
            )

            walk_animation.walk_time += delta_time * walk_animation.walk_speed
            transform.rotation = (
                math.sin(walk_animation.walk_time) * walk_animation.walk_amplitude
            )

        else:
            rigid_body.velocity = rigid_body.velocity.lerp(
                Vec2(0, 0), rigid_body.deceleration * delta_time
            )

            transform.rotation = 0
            walk_animation.walk_time = 0.0
