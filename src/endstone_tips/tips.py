from pathlib import Path

from endstone.plugin import Plugin

from endstone_tips.config import PluginConfig
from endstone_tips.tasks.boss_bar_task import BossBarTask
from endstone_tips.tasks.scoreboard_task import ScoreBoardTask
from endstone_tips.tasks.tip_task import TipTask
from endstone_tips.utils.api import register_variable
from endstone_tips.utils.plugin_listener import OnListener
from endstone_tips.utils.variables.default_variable import DefaultVariable

tips_instance = None

BOSS_BAR_TYPE = 0
CHAT_MESSAGE_TYPE = 1
NAME_TAG_TYPE = 2
SCOREBOARD_TYPE = 3
TIP_MESSAGE_TYPE = 4
BROAD_CAST_TYPE = 5

class Tips(Plugin):

    prefix = "Tips"
    version = "0.0.7"
    api_version = "0.5"

    description = "Tips plugin for Endstone."

    def __init__(self):
        super().__init__()
        global tips_instance
        tips_instance = self

        self.plugin_config = None
        self.tasks = {}

    def on_load(self):
        if not self.data_folder.exists():
            self.data_folder.mkdir()
        self.save_default_config()
        if not (Path(self.data_folder) / "theme/default.toml").exists():
            self.save_resources("theme/default.toml")
        self.save_resources("Tips变量.txt", replace=True)
        pass

    def on_enable(self):
        # 加载插件配置
        self.plugin_config = PluginConfig(f"{self.data_folder}/config.toml")

        # 注册变量
        register_variable("default", DefaultVariable)

        # 注册事件
        self.register_events(OnListener())

        # 注册Task
        self.tasks[BOSS_BAR_TYPE] = BossBarTask()
        self.tasks[SCOREBOARD_TYPE] = ScoreBoardTask()
        self.tasks[TIP_MESSAGE_TYPE] = TipTask()

        self.server.scheduler.run_task(self, self.tasks[BOSS_BAR_TYPE].on_update, 0, self.plugin_config.get_refresh_set()["Boss血条"])
        self.server.scheduler.run_task(self, self.tasks[SCOREBOARD_TYPE].on_update, 0, self.plugin_config.get_refresh_set()["计分板"])
        self.server.scheduler.run_task(self, self.tasks[TIP_MESSAGE_TYPE].on_update, 0, self.plugin_config.get_refresh_set()["底部"])

        self.logger.info("插件加载完成~")
        pass

    def on_disable(self):

        pass

    @property
    def plugin_loader(self):
        return self.plugin_loader