# type: ignore
from random import randint

from arepy import ArepyEngine
from arepy.arepy_imgui.imgui_repository import Imgui
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.math import Vec2
from imgui_bundle import ImVec2

from bubbleland import commands, config
from bubbleland.components import Pickable, PickUp, Weapon


def ui_debug_system(
    engine: ArepyEngine, imgui: Imgui, query: Query[Entities, With[Weapon, Pickable]]
):
    # draw a debug overlay at bottom left corner
    imgui.new_frame()
    show_debug_window(engine, imgui)
    show_spawn_window(engine, imgui, list(query.get_entities()))
    imgui.render()


def show_debug_window(engine: ArepyEngine, imgui: Imgui):
    current_world = engine.get_current_world()
    ecs_registry = current_world.get_registry()
    imgui.set_next_window_pos(ImVec2(10, 10))
    window_flags = (
        imgui.WindowFlags_.no_decoration
        | imgui.WindowFlags_.no_resize
        | imgui.WindowFlags_.no_move
        | imgui.WindowFlags_.always_auto_resize
    )
    imgui.begin("Debug", True, window_flags)
    imgui.text(f"Current world: {current_world.name}")
    imgui.separator()
    imgui.text(f"FPS: {engine.renderer.get_framerate()}")
    imgui.text(f"Entities: {ecs_registry.number_of_entities}")
    imgui.text(f"Queries: {len(ecs_registry.queries)}")
    imgui.separator()
    imgui.text("Controls:")
    imgui.text("WASD to move")
    imgui.text("Space to shoot")
    imgui.separator()
    imgui.end()


def show_spawn_window(engine: ArepyEngine, imgui: Imgui, weapons: Entities):

    imgui.begin("Spawn", True)
    imgui.text("Spawn in random position")
    if imgui.button("Spawn a ak48"):
        commands.spawn_ak48(
            engine,
            Vec2(randint(0, config.RESOLUTION[0]), randint(0, config.RESOLUTION[1])),
        )
    if imgui.button("Spawn a shotgun"):
        commands.spawn_shotgun(
            engine,
            Vec2(randint(0, config.RESOLUTION[0]), randint(0, config.RESOLUTION[1])),
        )

    if imgui.button("Spawn a sheriff"):
        commands.spawn_sheriff(
            engine,
            Vec2(randint(0, config.RESOLUTION[0]), randint(0, config.RESOLUTION[1])),
        )
    if imgui.button("Spawn a player"):
        commands.spawn_player(
            engine,
            Vec2(500, 500),
        )
    if imgui.button("Spawn a enemy"):
        commands.spawn_enemy(
            engine,
            Vec2(randint(0, config.RESOLUTION[0]), randint(0, config.RESOLUTION[1])),
        )
    if imgui.button("Spawn ammo"):
        commands.spawn_ammo(
            engine,
            Vec2(randint(0, config.RESOLUTION[0]), randint(0, config.RESOLUTION[1])),
        )
    if imgui.button("Spawn health"):
        commands.spawn_health(
            engine,
            Vec2(randint(0, config.RESOLUTION[0]), randint(0, config.RESOLUTION[1])),
        )
    imgui.separator()
    imgui.text(f"Weapons in scene: {len(weapons)}")
    imgui.text(
        f"Current weapon grabbed: {[weapon.get_id() for weapon in weapons if weapon.has_component(Pickable) and weapon.get_component(Pickable).grabbed]}"
    )
    imgui.end()
