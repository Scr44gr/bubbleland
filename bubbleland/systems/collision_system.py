from arepy.bundle.components import Transform
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.engine.input import Input

from bubbleland.components import Collider, KeyboardControlled, Pickable


def collision_system(
    player_query: Query[Entities, With[Transform, Collider, KeyboardControlled]],
    pickup_query: Query[Entities, With[Transform, Collider, Pickable]],
    input: Input,
):
    """Detects collisions between the player and pickup entities."""
    player_entity = next(iter(player_query.get_entities()), None)
    if player_entity is None:
        return

    player_transform = player_entity.get_component(Transform)
    player_collider = player_entity.get_component(Collider)
    e_was_pressed = input.is_key_pressed(
        player_entity.get_component(KeyboardControlled).interact_key
    )

    # Hardcoded boundaries
    if player_transform.position.x < 32:
        player_transform.position.x = 32
    if player_transform.position.y < 32:
        player_transform.position.y = 32

    if player_transform.position.x >= 1500:
        player_transform.position.x = 1500
    if player_transform.position.y >= 900:
        player_transform.position.y = 900

    for weapon in pickup_query.get_entities():
        pickup_transform = weapon.get_component(Transform)
        pickup_collider = weapon.get_component(Collider)
        pickup = weapon.get_component(Pickable)

        if e_was_pressed and pickup.can_be_grabbed:
            pickup.grabbed = True
            continue

        distance = abs(player_transform.position - pickup_transform.position)
        pickup.can_be_grabbed = distance < (
            player_collider.radius + pickup_collider.radius
        )
