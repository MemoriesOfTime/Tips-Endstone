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

    pass


class PluginConfig:

    def __init__(self, file):
        with (Path(file).open("r", encoding="utf-8")) as f:
            self._config = tomlkit.load(f)

        from endstone_tips.tips import tips_instance

        theme_name = self._config.get("默认样式", "default")
        self.theme: ThemeConfig = ThemeConfig(f"{tips_instance.data_folder}/theme/{theme_name}.toml")
        pass

    def get_variable(self) -> []:
        return self._config.get("变量显示", [])


if __name__ == "__main__":
    plugin_config = PluginConfig('config.toml')
    print(plugin_config.get_variable()["玩家权限"]["op"])
    print(plugin_config.theme.get_message_set("world"))