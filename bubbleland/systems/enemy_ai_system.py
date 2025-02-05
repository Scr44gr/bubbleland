from arepy.bundle.components import RigidBody2D, Transform
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With

from bubbleland.components import EnemyAI, Health, KeyboardControlled, Weapon


def enemy_ai_system(
    query: Query[Entities, With[Health, Transform, RigidBody2D]],
):
    """
    Makes the enemy follow the player and attack when close enough.
    """
    player_entity = [
        entity
        for entity in query.get_entities()
        if entity.has_component(KeyboardControlled)
    ]
    if not player_entity:
        return

    player_entity = player_entity[0]
    player_transform = player_entity.get_component(Transform)

    for enemy_entity in query.get_entities():
        if not enemy_entity.has_component(EnemyAI):
            continue

        enemy_transform = enemy_entity.get_component(Transform)
        enemy_rigid_body = enemy_entity.get_component(RigidBody2D)
        enemy_ai = enemy_entity.get_component(EnemyAI)

        distance = abs(enemy_transform.position - player_transform.position)

        if distance < enemy_ai.attack_range:
            ...
        if enemy_transform.position.x < player_transform.position.x:
            enemy_rigid_body.velocity.x = enemy_ai.walk_speed
        else:
            enemy_rigid_body.velocity.x = -enemy_ai.walk_speed

        if enemy_transform.position.y < player_transform.position.y:
            enemy_rigid_body.velocity.y = enemy_ai.walk_speed
        else:
            enemy_rigid_body.velocity.y = -enemy_ai.walk_speed
