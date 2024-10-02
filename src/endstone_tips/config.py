from pathlib import Path

import tomlkit


class ThemeConfig:

    def __init__(self, file):
        with (Path(file).open("r", encoding="utf-8")) as f:
            self._config = tomlkit.load(f)
        pass

    def get_message_set(self, world: str) -> []:
        config = self._config.get("聊天", [])
        if world in config:
            return config[world]
        return config["default"]

    def get_scoreboard_set(self, world: str) -> []:
        config = self._config.get("计分板", [])
        if world in config:
            return config[world]
        return config["default"]

    pass


class PluginConfig:

    def __init__(self, file):
        with (Path(file).open("r", encoding="utf-8")) as f:
            self._config = tomlkit.load(f)

        from endstone_tips.tips import tips_instance

        # 加载模板
        theme_name = self._config.get("默认样式", "default")
        self.theme: ThemeConfig = ThemeConfig(f"{tips_instance.data_folder}/theme/{theme_name}.toml")
        pass

    def get_variable(self) -> []:
        return self._config.get("变量显示", [])

    def get_motd_set(self) -> []:
        return self._config.get("自定义MOTD", [])

    def get_refresh_set(self) -> []:
        return self._config.get("自定义刷新刻度", [])