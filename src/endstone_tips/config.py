from pathlib import Path

import tomlkit


class ThemeConfig:

    def __init__(self, file):
        with (Path(file).open("r", encoding="utf-8")) as f:
            self._config = tomlkit.load(f)

    def _get_config(self, section: str, world: str, default_key: str = "default"):
        """通用配置获取方法"""
        config = self._config.get(section, {})
        if world in config:
            return config[world]
        return config.get(default_key, {})

    def get_message_set(self, world: str) -> dict:
        """获取聊天消息配置"""
        return self._get_config("聊天", world)

    def get_scoreboard_set(self, world: str) -> dict:
        """获取计分板配置"""
        return self._get_config("计分板", world)

    def get_boss_bar_set(self, world: str) -> dict:
        """获取Boss血条配置"""
        return self._get_config("Boss血条", world)

    def get_tip_set(self, world: str) -> dict:
        """获取底部显示配置"""
        return self._get_config("底部", world)

    def get_nametag_set(self, world: str) -> dict:
        """获取头顶显示配置"""
        return self._get_config("头部", world)

    def get_broadcast_set(self, world: str) -> dict:
        """获取聊天栏公告配置"""
        return self._get_config("聊天栏公告", world)


class PluginConfig:

    def __init__(self, file):
        with (Path(file).open("r", encoding="utf-8")) as f:
            self._config = tomlkit.load(f)

        from endstone_tips.tips import tips_instance

        # 加载模板
        theme_name = self._config.get("默认样式", "default")
        self.theme: ThemeConfig = ThemeConfig(f"{tips_instance.data_folder}/theme/{theme_name}.toml")

    def get_variable(self) -> dict:
        """获取变量显示配置"""
        return self._config.get("变量显示", {})

    def get_motd_set(self) -> dict:
        """获取MOTD配置"""
        return self._config.get("自定义MOTD", {})

    def get_refresh_set(self) -> dict:
        """获取刷新刻度配置"""
        return self._config.get("自定义刷新刻度", {})
