from arepy import ArepyEngine
from arepy.asset_store import AssetStore

from bubbleland import config


# Graphics loading functions
def load_player_graphics(game: ArepyEngine, asset_store: AssetStore):
    asset_store.load_texture(
        game.renderer,
        "player_idle",
        f"{config.ASSET_PATH}/sprites/player/player_idle.png",
    )
    asset_store.load_texture(
        game.renderer,
        "player_attack",
        f"{config.ASSET_PATH}/sprites/player/player_attack.png",
    )
    asset_store.load_texture(
        game.renderer,
        "player_damaged",
        f"{config.ASSET_PATH}/sprites/player/player_damaged.png",
    )


def load_enemy_graphics(game: ArepyEngine, asset_store: AssetStore):
    asset_store.load_texture(
        game.renderer,
        "enemy_idle",
        f"{config.ASSET_PATH}/sprites/enemies/basic_enemy_idle.png",
    )

    asset_store.load_texture(
        game.renderer,
        "enemy_damaged",
        f"{config.ASSET_PATH}/sprites/enemies/basic_enemy_damaged.png",
    )


def load_weapon_graphics(game: ArepyEngine, asset_store: AssetStore):
    asset_store.load_texture(
        game.renderer,
        "ak48",
        f"{config.ASSET_PATH}/sprites/weapons/ak48.png",
    )
    asset_store.load_texture(
        game.renderer,
        "shotgun",
        f"{config.ASSET_PATH}/sprites/weapons/shotgun.png",
    )
    asset_store.load_texture(
        game.renderer,
        "sheriff",
        f"{config.ASSET_PATH}/sprites/weapons/sheriff.png",
    )


def load_bullet_graphics(game: ArepyEngine, asset_store: AssetStore):
    asset_store.load_texture(
        game.renderer,
        "red_bullet",
        f"{config.ASSET_PATH}/sprites/bullets/red_bullet.png",
    )
    asset_store.load_texture(
        game.renderer,
        "yellow_bullet",
        f"{config.ASSET_PATH}/sprites/bullets/yellow_bullet.png",
    )


def load_item_graphics(game: ArepyEngine, asset_store: AssetStore):
    asset_store.load_texture(
        game.renderer,
        "ammo",
        f"{config.ASSET_PATH}/sprites/items/ammo.png",
    )
    asset_store.load_texture(
        game.renderer,
        "health",
        f"{config.ASSET_PATH}/sprites/items/health.png",
    )


def load_tilemap_graphics(game: ArepyEngine, asset_store: AssetStore):
    asset_store.load_texture(
        game.renderer,
        "ground",
        f"{config.ASSET_PATH}/tilemap/bathroom_floor_tilemap.png",
    )
    asset_store.load_texture(
        game.renderer,
        "wall_horizontal",
        f"{config.ASSET_PATH}/tilemap/bathroom_walls_tilemap.png",
    )
    asset_store.load_texture(
        game.renderer,
        "wall_vertical",
        f"{config.ASSET_PATH}/tilemap/bathroom_wall_borders_tilemap.png",
    )
    asset_store.load_texture(
        game.renderer,
        "ground_2",
        f"{config.ASSET_PATH}/tilemap/bathroom_foor_basic.png",
    )


# Sound loading functions


def load_shoot_sounds(game: ArepyEngine, asset_store: AssetStore):
    asset_store.load_sound(
        game.audio_device,
        "shoot",
        f"{config.ASSET_PATH}/sounds/simple_shoot.ogg",
    )
    asset_store.load_sound(
        game.audio_device,
        "no_ammo",
        f"{config.ASSET_PATH}/sounds/no_ammo.ogg",
    )
    asset_store.load_sound(
        game.audio_device,
        "reload",
        f"{config.ASSET_PATH}/sounds/reload.ogg",
    )
