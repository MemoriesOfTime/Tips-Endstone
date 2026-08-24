from pathlib import Path

from endstone.command import Command, CommandSender
from endstone.plugin import Plugin

from endstone_tips.commands import handle_tips_command
from endstone_tips.config import PluginConfig
from endstone_tips.tasks.boss_bar_task import BossBarTask
from endstone_tips.tasks.broadcast_task import BroadcastTask
from endstone_tips.tasks.nametag_task import NameTagTask
from endstone_tips.tasks.scoreboard_task import ScoreBoardTask
from endstone_tips.tasks.tip_task import TipTask
from endstone_tips.utils.api import register_variable
from endstone_tips.utils.economy import EconomyManager
from endstone_tips.utils.player_config import PlayerConfig
from endstone_tips.utils.plugin_listener import OnListener
from endstone_tips.utils.theme_manager import ThemeManager
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
    version = "0.1.1"
    api_version = "0.10"

    description = "Tips plugin for Endstone."

    # 命令注册
    commands = {
        "tips": {
            "description": "Tips 插件主命令",
            "usages": [
                "/tips",
                "/tips reload",
                "/tips send <player: player> <type: string> <message: message>",
                "/tips theme [name: string]",
                "/tips gui",
                "/tips help",
            ],
            "aliases": ["tip"],
            "permissions": ["tips.command"],
        }
    }

    # 权限注册
    permissions = {
        "tips.command": {
            "description": "允许使用 /tips 命令",
            "default": True,
        },
        "tips.admin": {
            "description": "允许使用 /tips 管理命令 (reload, send)",
            "default": "op",
        },
    }

    def __init__(self):
        super().__init__()
        global tips_instance
        tips_instance = self

        self.plugin_config = None
        self.player_config = None
        self.theme_manager = None
        self.economy_manager = None
        self.tasks = {}

    def on_load(self):
        if not self.data_folder.exists():
            self.data_folder.mkdir()
        self.save_default_config()
        if not (Path(self.data_folder) / "theme/default.toml").exists():
            self.save_resources("theme/default.toml")
        # 注意: 资源文件名必须为 ASCII，部分服务器环境 (如 Docker 默认 locale) 的
        # 文件系统编码为 ASCII，非 ASCII 文件名会导致 save_resources 抛出 UnicodeEncodeError
        self.save_resources("tips_variables.txt", replace=True)

    def on_enable(self):
        # 加载插件配置
        self.plugin_config = PluginConfig(f"{self.data_folder}/config.toml")
        
        # 初始化玩家配置管理器
        self.player_config = PlayerConfig(Path(self.data_folder))
        
        # 初始化主题管理器
        self.theme_manager = ThemeManager(Path(self.data_folder))
        
        # 初始化经济管理器 (软依赖)
        self.economy_manager = EconomyManager(self.server)
        if self.economy_manager.is_available():
            self.logger.info("已检测到经济插件，{money} 变量可用")
        else:
            self.logger.info("未检测到经济插件，{money} 变量将显示 N/A")

        # 注册变量
        register_variable("default", DefaultVariable)

        # 注册事件
        self.register_events(OnListener())

        # 注册Task
        refresh_set = self.plugin_config.get_refresh_set()
        
        self.tasks[BOSS_BAR_TYPE] = BossBarTask()
        self.tasks[SCOREBOARD_TYPE] = ScoreBoardTask()
        self.tasks[TIP_MESSAGE_TYPE] = TipTask()
        self.tasks[NAME_TAG_TYPE] = NameTagTask()
        self.tasks[BROAD_CAST_TYPE] = BroadcastTask()

        # 启动定时任务
        self.server.scheduler.run_task(
            self, self.tasks[BOSS_BAR_TYPE].on_update, 
            0, refresh_set.get("Boss血条", 20)
        )
        self.server.scheduler.run_task(
            self, self.tasks[SCOREBOARD_TYPE].on_update, 
            0, refresh_set.get("计分板", 20)
        )
        self.server.scheduler.run_task(
            self, self.tasks[TIP_MESSAGE_TYPE].on_update, 
            0, refresh_set.get("底部", 20)
        )
        self.server.scheduler.run_task(
            self, self.tasks[NAME_TAG_TYPE].on_update, 
            0, refresh_set.get("头部", 20)
        )
        # 广播任务使用较短间隔检查，实际间隔在任务内部控制
        self.server.scheduler.run_task(
            self, self.tasks[BROAD_CAST_TYPE].on_update, 
            0, 20  # 每秒检查一次
        )

        self.logger.info("Tips 插件加载完成~")

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        """处理命令"""
        if command.name == "tips":
            return handle_tips_command(self, sender, command, args)
        return False

    def on_disable(self):
        pass
    
    def get_player_theme(self, player_name: str):
        """获取玩家的主题配置"""
        return self.theme_manager.get_player_theme(player_name)
