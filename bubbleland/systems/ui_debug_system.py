# type: ignore
from random import randint

from arepy import ArepyEngine
from arepy.arepy_imgui.imgui_repository import Imgui
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.ecs.systems import SystemState
from arepy.math import Vec2
from imgui_bundle import ImVec2, ImVec4

from bubbleland import commands, config
from bubbleland.components import Pickable, Weapon

can_show_system_manager = False


def ui_debug_system(
    engine: ArepyEngine, imgui: Imgui, query: Query[Entities, With[Weapon, Pickable]]
):
    global can_show_system_manager
    imgui.new_frame()
    show_debug_window(engine, imgui)
    show_spawn_window(engine, imgui, list(query.get_entities()))
    # system view can be task expensive
    # so we only show it if the user wants to
    if can_show_system_manager:
        show_system_view(engine, imgui)
    imgui.render()


def show_debug_window(engine: ArepyEngine, imgui: Imgui):
    global can_show_system_manager
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
    imgui.text(f"Systems: {ecs_registry.number_of_systems}")
    # change world
    worlds = engine.worlds.keys()
    imgui.text("Change world:")
    for world in worlds:
        if imgui.button(world):
            if world != current_world.name:
                engine.set_current_world(world)

    imgui.separator()
    imgui.text("Controls:")
    imgui.text("WASD to move")
    imgui.text("E to grab weapon")
    imgui.text("Space to shoot")
    imgui.separator()
    if imgui.button(
        f"{'Show' if not can_show_system_manager else 'Hide'} System Manager"
    ):
        can_show_system_manager = not can_show_system_manager
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


def show_system_view(engine: ArepyEngine, imgui: Imgui):
    imgui.begin("System Manager", True)

    current_world = engine.get_current_world()
    ecs_registry = current_world.get_registry()

    for pipeline in ecs_registry.systems.keys():
        imgui.text_colored(ImVec4(0.2, 0.6, 1.0, 1.0), f"Pipeline: {pipeline.name}")

        current_pipeline = ecs_registry.systems[pipeline]
        systems = sorted(
            {
                (state, system)
                for state in current_pipeline
                for system in current_pipeline[state]
            },
            key=lambda x: x[1].__name__,
        )
        imgui.indent(5)
        for state, system in systems:
            imgui.begin_group()
            if imgui.button(f"{system.__name__}", ImVec2(200, 20)):
                new_state = SystemState(not state.value)
                current_world.set_system_state(pipeline, system, new_state)
            imgui.same_line()
            if state == SystemState.ON:
                imgui.text_colored(ImVec4(0.0, 1.0, 0.0, 1.0), "ON")
            else:
                imgui.text_colored(ImVec4(1.0, 0.0, 0.0, 1.0), "OFF")
            imgui.end_group()
        imgui.unindent(5)
        imgui.separator()

    imgui.end()
