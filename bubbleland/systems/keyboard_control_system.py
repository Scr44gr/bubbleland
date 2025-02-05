import math
import random
from time import time

from arepy import ArepyEngine
from arepy.bundle.components import Camera2D, RigidBody2D, Transform
from arepy.ecs.entities import Entities, Entity
from arepy.ecs.query import Query, With
from arepy.engine.input import Input, MouseButton
from arepy.engine.renderer.renderer_2d import Renderer2D
from arepy.math import Vec2

from bubbleland import commands
from bubbleland.components import KeyboardControlled, Pickable, WalkAnimation, Weapon

last_shoot_direction = Vec2(0, 0)


def keyboard_control_system(
    query: Query[
        Entities, With[RigidBody2D, Transform, KeyboardControlled, WalkAnimation]
    ],
    weapon_query: Query[Entities, With[Weapon, Pickable]],
    input: Input,
    renderer: Renderer2D,
    engine: ArepyEngine,
):
    """Handles player movement and shooting input."""

    delta_time = renderer.get_delta_time()
    player = next(iter(query.get_entities()), None)
    if player is None:
        return

    weapon = [
        entity
        for entity in weapon_query.get_entities()
        if entity.get_component(Pickable).grabbed
    ]

    if weapon:
        handle_player_shooting_input(player, weapon[0], engine, input)

    handle_player_movement_input(player, input, delta_time)


def handle_player_shooting_input(
    player: Entity, weapon: Entity, engine: ArepyEngine, input: Input
):
    global last_shoot_direction
    transform = weapon.get_component(Transform)
    rigid_body = player.get_component(RigidBody2D)
    weapon_component = weapon.get_component(Weapon)

    if input.is_mouse_button_released(MouseButton.LEFT):
        last_shoot_direction = Vec2(0, 0)

    # If the player tries to shoot without ammo, play a sound of no ammo
    if (
        input.is_mouse_button_pressed(MouseButton.LEFT)
        and weapon_component.current_bullet_count == 0
    ):
        no_ammo_sound = engine.get_asset_store().sounds.get("no_ammo")
        if no_ammo_sound:
            engine.audio_device.play_sound(no_ammo_sound)
        return

    if (
        input.is_mouse_button_down(MouseButton.LEFT)
        and weapon_component.current_bullet_count > 0
    ):
        current_time = time()
        if current_time - weapon_component.cooldown <= weapon_component.fire_rate:
            return

        if last_shoot_direction == Vec2(0, 0):
            mouse_screen_pos = input.get_mouse_position()
            mouse_world_pos = engine.renderer.screen_to_world(
                mouse_screen_pos, player.get_component(Camera2D)
            )
            last_shoot_direction = (
                Vec2(mouse_world_pos[0], mouse_world_pos[1]) - transform.position
            ).normalize()

        player_speed = abs(rigid_body.velocity)
        max_dispersion_angle = math.radians(weapon_component.dispersion_angle)
        dispersion_angle = max_dispersion_angle * (
            player_speed / rigid_body.max_velocity
        )

        random_angle = random.uniform(-dispersion_angle, dispersion_angle)
        direction = last_shoot_direction.rotate(random_angle)

        commands.trigger_camera_shake(
            player, weapon_component.shake_intensity, weapon_component.shake_duration
        )
        commands.shoot_projectile(
            engine,
            transform.position,
            direction=direction,
            angle=transform.rotation,
        )
        shoot_sound = engine.get_asset_store().sounds.get("shoot")
        if shoot_sound:
            engine.audio_device.play_sound(shoot_sound)
        weapon_component.cooldown = current_time
        weapon_component.current_bullet_count -= 1


def handle_player_movement_input(entity, input, delta_time):
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
