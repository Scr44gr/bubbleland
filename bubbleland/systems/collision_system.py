import pyray as pr
from arepy import ArepyEngine
from arepy.bundle.components import Sprite, Transform
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.engine.input import Input

from bubbleland.commands.spawn_ammo import increase_bullet_count
from bubbleland.commands.spawn_health import increase_health
from bubbleland.components import (
    Collider,
    Health,
    KeyboardControlled,
    Pickable,
    PickUp,
    Weapon,
)


def pickeable_system(
    player_query: Query[Entities, With[Transform, Collider, KeyboardControlled]],
    pickeable_items_query: Query[Entities, With[Transform, Collider, Pickable]],
    input: Input,
):
    """
    Detects collisions between the player and pickeable entities.
    """
    player_entity = next(iter(player_query.get_entities()), None)
    if player_entity is None:
        return

    player_transform = player_entity.get_component(Transform)
    player_collider = player_entity.get_component(Collider)
    e_was_pressed = input.is_key_pressed(
        player_entity.get_component(KeyboardControlled).interact_key
    )

    grabbed_items = [
        item
        for item in pickeable_items_query.get_entities()
        if item.get_component(Pickable).grabbed
    ]

    for pickeable_item in pickeable_items_query.get_entities():
        pickup_transform = pickeable_item.get_component(Transform)
        pickup_collider = pickeable_item.get_component(Collider)
        pickup = pickeable_item.get_component(Pickable)

        if e_was_pressed and pickup.can_be_grabbed:
            for current_weapon in grabbed_items:
                current_weapon.get_component(Pickable).grabbed = False
                current_weapon.get_component(Pickable).can_be_grabbed = False
            pickup.grabbed = True
            continue

        distance = abs(player_transform.position - pickup_transform.position)
        pickup.can_be_grabbed = distance < (
            player_collider.radius + pickup_collider.radius
        )


def recolectable_system(
    player_query: Query[Entities, With[Transform, Collider, KeyboardControlled]],
    recolectable_items_query: Query[Entities, With[Transform, Collider, PickUp]],
    weapon_query: Query[Entities, With[Weapon, Pickable]],
    engine: ArepyEngine,
):
    """
    Detects collisions between the player and recolectable entities.
    """
    player_entity = next(iter(player_query.get_entities()), None)
    if player_entity is None:
        return

    player_transform = player_entity.get_component(Transform)
    player_collider = player_entity.get_component(Collider)

    for recolectable_item in recolectable_items_query.get_entities():
        recolectable_transform = recolectable_item.get_component(Transform)
        recolectable_collider = recolectable_item.get_component(Collider)

        # If we have a health item
        if recolectable_item.has_component(Health):
            distance = abs(player_transform.position - recolectable_transform.position)
            if distance < (player_collider.radius + recolectable_collider.radius):
                increase_health(player_entity)
                recolectable_item.kill()
                return

        # If we have a weapon and the collectable item is ammo
        activate_weapons = [
            weapon
            for weapon in weapon_query.get_entities()
            if weapon.has_component(Pickable) and weapon.get_component(Pickable).grabbed
        ]

        if recolectable_item.has_component(PickUp) and activate_weapons:
            distance = abs(player_transform.position - recolectable_transform.position)
            if distance < (player_collider.radius + recolectable_collider.radius):
                reload_sound = engine.get_asset_store().sounds.get("reload")
                if reload_sound:
                    engine.audio_device.play_sound(reload_sound)

                increase_bullet_count(activate_weapons[0])
                recolectable_item.kill()


def collision_system(
    player_query: Query[Entities, With[Transform, Collider, KeyboardControlled]],
):
    """Detects collisions between the player and the screen boundaries."""
    player_entity = next(iter(player_query.get_entities()), None)
    screen_width = pr.get_screen_width()
    screen_height = pr.get_screen_height()
    if player_entity is None:
        return

    player_transform = player_entity.get_component(Transform)
    player_sprite = player_entity.get_component(Sprite)

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
