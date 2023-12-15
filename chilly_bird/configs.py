from dataclasses import dataclass, field
from pathlib import Path

from omegaconf import MISSING, OmegaConf


@dataclass
class Window:
    fps: int = 60
    screen_width: int = 432
    screen_height: int = 468
    caption: str = MISSING
    icon_path: Path = MISSING


@dataclass
class Fonts:
    color: tuple[int, int, int] = (235, 221, 190)
    score_font: Path = MISSING
    score_font_size: int = MISSING
    text_font: Path = MISSING
    text_font_size: int = MISSING


@dataclass
class MainSceneAssets:
    bg_img: Path = MISSING
    road_texture: Path = MISSING
    restart_button_img: Path = MISSING
    disappointed_girl_img: Path = MISSING
    bg_music: Path = MISSING


@dataclass
class MainConfig:
    window: Window = field(default_factory=lambda: Window())
    fonts: Fonts = field(default_factory=lambda: Fonts())
    main_scene: MainSceneAssets = field(default_factory=lambda: MainSceneAssets())


if __name__ == "__main__":
    conf: MainConfig = OmegaConf.structured(MainConfig)
    print(OmegaConf.to_yaml(conf))
