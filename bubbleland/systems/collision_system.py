import pyray as pr
from arepy.bundle.components import Camera2D, Sprite, Transform
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.engine.display import Display
from arepy.engine.input import Input

from bubbleland.commands.spawn_ammo import increase_bullet_count
from bubbleland.components import Collider, KeyboardControlled, Pickable, PickUp


def collision_system(
    player_query: Query[Entities, With[Transform, Collider, KeyboardControlled]],
    pickup_query: Query[Entities, With[Transform, Collider, Pickable]],
    ammo_query: Query[Entities, With[Transform, Collider, PickUp]],
    input: Input,
):
    """Detects collisions between the player and pickup entities."""
    player_entity = next(iter(player_query.get_entities()), None)
    screen_width = pr.get_screen_width()
    screen_height = pr.get_screen_height()
    if player_entity is None:
        return

    player_transform = player_entity.get_component(Transform)
    player_collider = player_entity.get_component(Collider)
    player_sprite = player_entity.get_component(Sprite)
    e_was_pressed = input.is_key_pressed(
        player_entity.get_component(KeyboardControlled).interact_key
    )

    # Hardcoded boundaries
    player_collider_x_offset = player_sprite.src_rect[2]
    player_collider_y_offset = player_sprite.src_rect[3]
    if player_transform.position.x < player_collider_x_offset:
        player_transform.position.x = player_collider_x_offset
    if player_transform.position.y < player_collider_y_offset:
        player_transform.position.y = player_collider_y_offset

    right_boundary_limit = (screen_width / 1.2) + player_collider_x_offset
    if player_transform.position.x >= right_boundary_limit:
        player_transform.position.x = right_boundary_limit

    lower_boundary_limit = screen_height / 1.2 - player_collider_y_offset
    if player_transform.position.y >= lower_boundary_limit:
        player_transform.position.y = lower_boundary_limit

    current_player_weapon = [
        weapon
        for weapon in pickup_query.get_entities()
        if weapon.get_component(Pickable).grabbed
    ]

    for ammo in ammo_query.get_entities():
        ammo_transform = ammo.get_component(Transform)
        ammo_collider = ammo.get_component(Collider)
        pick_up = ammo.get_component(PickUp)

        distance = abs(player_transform.position - ammo_transform.position)
        if distance < (player_collider.radius + ammo_collider.radius):
            increase_bullet_count(current_player_weapon[0])
            ammo.kill()

    for weapon in pickup_query.get_entities():
        pickup_transform = weapon.get_component(Transform)
        pickup_collider = weapon.get_component(Collider)
        pickup = weapon.get_component(Pickable)

        if e_was_pressed and pickup.can_be_grabbed:
            for current_weapon in current_player_weapon:
                current_weapon.get_component(Pickable).grabbed = False
                current_weapon.get_component(Pickable).can_be_grabbed = False

            pickup.grabbed = True
            continue

        distance = abs(player_transform.position - pickup_transform.position)
        pickup.can_be_grabbed = distance < (
            player_collider.radius + pickup_collider.radius
        )
