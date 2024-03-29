"""Contains schemas and utilities for game configs."""

from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger
from omegaconf import MISSING, OmegaConf


@dataclass
class AssetsConf:
    """Schema for assets path config."""

    _path: Path = MISSING
    fonts_path: Path = MISSING
    frames_path: Path = MISSING
    img_path: Path = MISSING
    sound_path: Path = MISSING


@dataclass
class WindowConf:
    """Schema for main window settings config."""

    fps: int = 60
    screen_width: int = 432
    screen_height: int = 468
    caption: str = MISSING
    icon_path: Path = MISSING


@dataclass
class FontsConf:
    """Schema for fonts settings config."""

    color: tuple[int, int, int] = (235, 221, 190)
    score_font: Path = MISSING
    score_font_size: int = MISSING
    text_font: Path = MISSING
    text_font_size: int = MISSING


@dataclass
class MainSceneAssetsConf:
    """Schema for main scene settings config."""

    bird_aframes: tuple[Path, Path, Path] = MISSING
    bird_jump_sound: Path = MISSING
    bird_size: tuple[int, int] = (50, 35)
    bg_img: Path = MISSING
    bg_music: Path = MISSING
    road_texture: Path = MISSING
    pipe_img: Path = MISSING
    start_button_img: Path = MISSING
    restart_button_img: Path = MISSING
    music_button_img: Path = MISSING
    reskin_button_img: Path = MISSING
    redress_button_img: Path = MISSING
    disappointed_girl_img: Path = MISSING


@dataclass
class MainConfig:
    """Schema for main config."""

    assets: AssetsConf = field(default_factory=lambda: AssetsConf())
    window: WindowConf = field(default_factory=lambda: WindowConf())
    fonts: FontsConf = field(default_factory=lambda: FontsConf())
    main_scene: MainSceneAssetsConf = field(
        default_factory=lambda: MainSceneAssetsConf()
    )


def load_config(path: str) -> MainConfig:
    """Load OmegaConf structured config from file."""
    r_path = Path(path).resolve()
    logger.info("Loading config from {}", r_path)

    conf_s: MainConfig = OmegaConf.structured(MainConfig)
    conf_f = OmegaConf.load(r_path)
    conf: MainConfig = OmegaConf.merge(conf_s, conf_f)  # type: ignore
    return conf


def _debug_load() -> None:
    conf_s: MainConfig = OmegaConf.structured(MainConfig)
    conf_f = OmegaConf.load("./conf/config.yaml")
    conf: MainConfig = OmegaConf.merge(conf_s, conf_f)  # type: ignore
    print(OmegaConf.to_yaml(conf))
    # noinspection PyProtectedMember
    print(conf.assets._path.resolve())


if __name__ == "__main__":
    _debug_load()
