import pyray as pr
from arepy.bundle.components import Camera2D, Sprite, Transform
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.engine.display import Display
from arepy.engine.input import Input

from bubbleland import commands
from bubbleland.components import Collider, EnemyAI, Pickable, Projectile


def bullet_collision_system(
    bullet_query: Query[Entities, With[Transform, Collider, Projectile]],
    enemy_query: Query[Entities, With[Transform, Collider, EnemyAI]],
):
    """Detects collisions between bullets and enemies."""
    for bullet in bullet_query.get_entities():
        bullet_transform = bullet.get_component(Transform)
        for enemy in enemy_query.get_entities():
            enemy_transform = enemy.get_component(Transform)

            distance = abs(bullet_transform.position - enemy_transform.position)
            if (
                distance
                < enemy.get_component(Collider).radius
                + bullet.get_component(Collider).radius
            ):
                commands.decrease_enemy_health(bullet, enemy)
