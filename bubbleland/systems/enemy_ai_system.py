import pyray as pr
from arepy.bundle.components import Camera2D, RigidBody2D, Sprite, Transform
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.engine.display import Display
from arepy.engine.input import Input

from bubbleland.components import EnemyAI, KeyboardControlled, Weapon


def enemy_ai_system(
    player_query: Query[Entities, With[KeyboardControlled, Transform, RigidBody2D]],
    enemy_query: Query[Entities, With[EnemyAI, RigidBody2D, Transform]],
):
    """
    Makes the enemy follow the player and attack when close enough.
    """
    player_entity = next(iter(player_query.get_entities()), None)

    if player_entity is None:
        return

    for enemy_entity in enemy_query.get_entities():

        enemy_transform = enemy_entity.get_component(Transform)
        enemy_rigid_body = enemy_entity.get_component(RigidBody2D)
        enemy_ai = enemy_entity.get_component(EnemyAI)

        player_transform = player_entity.get_component(Transform)
        distance = abs(enemy_transform.position - player_transform.position)

        if distance < enemy_ai.attack_range:
            print("Attack!")

        if enemy_transform.position.x < player_transform.position.x:
            enemy_rigid_body.velocity.x = enemy_ai.walk_speed
        else:
            enemy_rigid_body.velocity.x = -enemy_ai.walk_speed

        if enemy_transform.position.y < player_transform.position.y:
            enemy_rigid_body.velocity.y = enemy_ai.walk_speed
        else:
            enemy_rigid_body.velocity.y = -enemy_ai.walk_speed
