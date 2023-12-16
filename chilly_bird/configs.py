from dataclasses import dataclass, field
from pathlib import Path

from omegaconf import MISSING, OmegaConf


@dataclass
class AssetsConf:
    _path: Path = MISSING
    fonts_path: Path = MISSING
    img_path: Path = MISSING
    sound_path: Path = MISSING


@dataclass(frozen=True)
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
    pipe_img: Path = MISSING
    restart_button_img: Path = MISSING
    disappointed_girl_img: Path = MISSING
    bg_music: Path = MISSING


@dataclass
class MainConfig:
    assets: AssetsConf = field(default_factory=lambda: AssetsConf())
    window: Window = field(default_factory=lambda: Window())
    fonts: Fonts = field(default_factory=lambda: Fonts())
    main_scene: MainSceneAssets = field(default_factory=lambda: MainSceneAssets())


def load_config(path: str = "./conf/config.yaml") -> MainConfig:
    conf_s: MainConfig = OmegaConf.structured(MainConfig)
    conf_f = OmegaConf.load("./conf/config.yaml")
    conf: MainConfig = OmegaConf.merge(conf_s, conf_f)  # type: ignore
    return conf


if __name__ == "__main__":
    conf_s: MainConfig = OmegaConf.structured(MainConfig)
    conf_f = OmegaConf.load("./conf/config.yaml")
    conf: MainConfig = OmegaConf.merge(conf_s, conf_f)  # type: ignore
    # print(OmegaConf.to_yaml(conf_s))
    # print(OmegaConf.to_yaml(conf_f))
    print(OmegaConf.to_yaml(conf))
    print(conf.assets._path.resolve())
