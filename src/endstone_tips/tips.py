from endstone.plugin import Plugin

from endstone_tips.config import PluginConfig
from endstone_tips.utils.api import register_variable
from endstone_tips.utils.plugin_listener import OnListener
from endstone_tips.utils.variables.default_variable import DefaultVariable

tips_instance = None

class Tips(Plugin):

    prefix = "Tips"
    version = "0.0.1"
    api_version = "0.5"

    description = "Tips plugin for Endstone."

    def __init__(self):
        super().__init__()
        global tips_instance
        tips_instance = self

        self.plugin_config = None

    def on_load(self):
        if not self.data_folder.exists():
            self.data_folder.mkdir()
            self.save_resources("Tips变量.txt")
            self.save_resources("config.toml")
            self.save_resources("theme/default.toml")

    def on_enable(self):
        #加载插件配置
        self.plugin_config = PluginConfig(f"{self.data_folder}/config.toml")

        # 注册变量
        register_variable("default", DefaultVariable)

        # 注册事件
        self.register_events(OnListener())

        self.logger.info("插件加载完成~")
        pass

    def on_disable(self):

        pass

    @property
    def plugin_loader(self):
        return self.plugin_loader