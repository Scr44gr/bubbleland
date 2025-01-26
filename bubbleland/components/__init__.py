from arepy.ecs.components import Component
from arepy.engine.input import Key, MouseButton
from arepy.engine.renderer import Color
from arepy.math import Vec2


class Health(Component):
    def __init__(self, max_health: int = 100, current_health: int = 100):
        self.max_health = max_health
        self.current_health = current_health


class EnemyAI(Component):
    def __init__(
        self, speed: float = 25.0, amplitude: float = 8.0, attack_range: float = 0.0
    ):
        self.walk_time = 0.0
        self.walk_speed = speed
        self.walk_amplitude = amplitude
        self.attack_range = attack_range


class Collider(Component):
    def __init__(self, width: int, height: int, radius: int = 0):
        self.width = width
        self.height = height
        self.radius = radius


class Pickable(Component):
    def __init__(
        self, name: str = "default", grabbed: bool = False, can_be_grabbed: bool = False
    ):
        self.name = name
        self.can_be_grabbed = can_be_grabbed
        self.grabbed = grabbed
        self.message = f"Press E to pick up {name}"


class PickUp(Component):
    def __init__(self, name: str = "default"):
        self.name = name
        self.message = f"+24 {name}"


class SimpleRectangle(Component):
    def __init__(self, width: int, height: int, color: Color = Color(10, 10, 10, 255)):
        self.width = width
        self.height = height
        self.color = color


class KeyboardControlled(Component):
    def __init__(
        self,
        up_key: Key = Key.W,
        down_key: Key = Key.S,
        left_key: Key = Key.A,
        right_key: Key = Key.D,
        shoot_key: MouseButton = MouseButton.LEFT,
        space_key: Key = Key.SPACE,
        interact_key: Key = Key.E,
    ):
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key
        self.space_key = space_key
        self.shoot_key = shoot_key
        self.interact_key = interact_key


class WalkAnimation(Component):
    def __init__(self, speed: float = 25.0, amplitude: float = 8.0):
        self.walk_time = 0.0
        self.walk_speed = speed
        self.walk_amplitude = amplitude


# Weapon components
class Projectile(Component):
    def __init__(
        self,
        direction: Vec2,
        speed: float = 100.0,
        damage: int = 1,
        life_time: float = 1.0,
    ):
        self.direction = direction
        self.speed = speed
        self.life_time = life_time
        self.damage = damage


class Weapon(Component):
    def __init__(
        self,
        name: str = "default",
        fire_rate: float = 0.2,
        cooldown: float = 0.0,
        shake_intensity: float = 1.5,
        shake_duration: float = 0.1,
        dispersion_angle: float = 0.0,
        current_bullet_count: int = 0,
        max_bullet_count: int = 0,
    ):
        self.name = name
        self.fire_rate = fire_rate
        self.cooldown = cooldown
        self.shake_intensity = shake_intensity
        self.shake_duration = shake_duration
        self.dispersion_angle = dispersion_angle
        self.direction = Vec2(0, 0)
        self.current_bullet_count = current_bullet_count
        self.max_bullet_count = max_bullet_count
