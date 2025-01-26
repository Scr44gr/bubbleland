import random

from arepy.bundle.components import Camera2D
from arepy.ecs.entities import Entities
from arepy.ecs.query import Query, With
from arepy.engine.renderer.renderer_2d import Renderer2D


def camera_shaking_system(
    camera_query: Query[Entities, With[Camera2D]],
    renderer: Renderer2D,
):
    """
    Applies camera shake to the camera entity.
    """
    delta_time = renderer.get_delta_time()
    for camera_entity in camera_query.get_entities():
        camera = camera_entity.get_component(Camera2D)

        if camera.shake_timer > 0:
            offset_x = random.uniform(-camera.shake_intensity, camera.shake_intensity)
            offset_y = random.uniform(-camera.shake_intensity, camera.shake_intensity)
            camera.offset.x = camera.original_offset.x + offset_x
            camera.offset.y = camera.original_offset.y + offset_y
            # Decrease the shake timer
            camera.shake_timer -= delta_time
        else:
            camera.offset.x = camera.original_offset.x
            camera.offset.y = camera.original_offset.y
