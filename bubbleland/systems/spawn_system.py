from arepy import ArepyEngine
from arepy.engine.input import Input, MouseButton
from arepy.math import Vec2

from .. import commands


def spawn_system(engine: ArepyEngine, input: Input):
    if input.is_mouse_button_pressed(MouseButton.LEFT):
        mouse_pos = input.get_mouse_position()
        commands.spawn_weapon(engine, Vec2(mouse_pos[0], mouse_pos[1]))
