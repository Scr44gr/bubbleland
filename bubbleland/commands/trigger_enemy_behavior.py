from arepy.bundle.components import Camera2D
from arepy.ecs.entities import Entity

from bubbleland.components import Health, Projectile


def decrease_enemy_health(projectile_entity: Entity, enemy: Entity):
    """
    Decreases the health of the enemy by the damage of the projectile.
    """
    if not enemy.has_component(Health):
        return

    health = enemy.get_component(Health)
    projectile = projectile_entity.get_component(Projectile)
    health.current_health -= projectile.damage
    projectile_entity.kill()

    if health.current_health <= 0:
        enemy.kill()
