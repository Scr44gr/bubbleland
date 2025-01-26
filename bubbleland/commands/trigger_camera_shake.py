from arepy.bundle.components import Camera2D
from arepy.ecs.entities import Entity


def trigger_camera_shake(player: Entity, intensity: float = 1.0, duration: float = 0.1):
    """
    Triggers a camera shake effect on the given camera entity.
    """
    if not player.has_component(Camera2D):
        return

    camera = player.get_component(Camera2D)
    camera.shake_intensity = intensity
    camera.shake_duration = duration
    camera.shake_timer = duration
