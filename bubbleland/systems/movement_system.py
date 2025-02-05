from arepy.bundle.components import RigidBody2D, Transform
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.engine.renderer.renderer_2d import Renderer2D

from bubbleland.components import Projectile, Weapon


def movement_system(
    query: Query[Entities, With[Transform, RigidBody2D]],
    renderer: Renderer2D,
):
    delta_time = renderer.get_delta_time()
    entities = query.get_entities()
    for entity in entities:
        if entity.has_component(Weapon):
            continue
        transform = entity.get_component(Transform)
        rigidbody = entity.get_component(RigidBody2D)

        transform.position += rigidbody.velocity * delta_time

        if entity.has_component(Projectile):
            projectile = entity.get_component(Projectile)
            projectile.life_time -= delta_time
            if projectile.life_time <= 0:
                entity.kill()
